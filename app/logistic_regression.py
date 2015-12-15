# coding: utf-8

# # 0.0 Import packages and set up Spark context, SQL context and Hive context.
import os
import sys
os.environ['SPARK_HOME'] = "/usr/local/spark" # Path for spark source folder
sys.path.append("/usr/local/spark/python") # Append pyspark to Python Path
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, HiveContext
sc = SparkContext() # not needed in IPython notebook.
sqlContext = SQLContext(sc)
hiveContext = HiveContext(sc)
sys.path.append("/usr/local/lib/python2.7/dist-packages/afinn") # Append afinn to Python Path
from afinn import Afinn # import afinn, used for sentiment analysis
from pyspark.mllib.regression import LabeledPoint # Stuff for logistic regression
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.linalg import SparseVector
from pyspark.sql.types import StructField, BooleanType, StringType, LongType, StructType # For json schema for read
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import fcns # Import helper functions for textfitXL

# # 1.0 Read data
# fields (fields.py in fcns package) defines json schema to speed up reading json files on S3 (about 2x improvement)
# Project used 908 GB data in "s3n://reddit-comments/*" but this is restricted to Insight.  Instead, use 2007 data only.
df = hiveContext.read.json("../data/*", StructType(fields))

# Filter down to subreddits of interest
subreddits = [u'leagueoflegends', u'GirlGamers', u'pics', u'politics']
df2 = (df.filter((df.subreddit==u'leagueoflegends')|(df.subreddit==u'GirlGamers')|(df.subreddit==u'pics')|(df.subreddit==u'politics') )
           .persist(StorageLevel.MEMORY_AND_DISK_SER))
df2.count() # Forces read in df, execute df2 BEFORE coalesce().
isInData = {key: True for key in subreddits}

# # 2.0 Filter to include only extreme up and down votes (top/bottom 3% of subreddit)
# Reduces dataset for all subsequent processing.
subredditDigest = createsrDict(df2, subreddits, isInData) 
srDigestR = {key : (round(subredditDigest[key][0]), round(subredditDigest[key][1]) ) for key in subredditDigest.keys()}  

# Put Dataframe into vanilla RDD
rRDD = (df2.map(lambda r: (r.id, (r.body, int(r.created_utc), r.link_id, r.parent_id, int(r.score), r.subreddit, r.subreddit_id))))

rRDDExtreme = (rRDD.filter(lambda (k,v): v[4] < srDigestR[v[5]][0] or v[4] > srDigestR[v[5]][1])
                  .coalesce(400)
                  .setName("rRDDExtreme")
                  .persist(StorageLevel.MEMORY_AND_DISK_SER) )
rRDDExtreme.count() # force evaluation of this RDD to reduce partitions (coalesce) in preparation for join.

# # 3.0 Find minimum comment timestamp for each post using HiveQL percentile UDF.  
# This is a proxy for the post timestamp, which was unavailable at the time this project was done.
rRDDExtremeLinks = rRDDExtreme.map(lambda (k,v): [v[2]])
dfExtreme = sqlContext.createDataFrame(rRDDExtremeLinks,["xlink_id"]).distinct()

# Find minimum time comments for each post and register as table
minTimeDF = hiveContext.sql("select link_id, min(cast (created_utc as int)) as min_utc from rcomments group by link_id")

# Create new dataframe with min time utc for ONLY link_id's referenced in top/bottom 3% using Dataframe join.
minTimeDFX = dfExtreme.join(minTimeDF, dfExtreme.xlink_id == minTimeDF.link_id, 'inner').drop('xlink_id')

# Create minimum time dictionary and broadcast to workers
minTimeDict = dict(minTimeDFX.collect())
minTimeBR = sc.broadcast(minTimeDict)

# # 4.0  Calculate timeSince
# Calculate time since post was created based on created_utc and min_created_utc from pair RDD. 
# Broadcast variable avoids another join.  Map RDD to get post link_id as key, subtract minTime to get timeSince.
rRDDXts = (rRDDExtreme.map(lambda (k,v):  (v[2],(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6])))  # pull link_id as key
                      .map(lambda (link_id,(x)):  (x[0], (x[1],x[2]-minTimeBR.value[link_id],x[5],x[6]))))

# # 5.0  Clean up body and calculate commentLength
rRDDXtscl = (rRDDXts.map(lambda (id,(body,timeSince,score,subreddit)): (id,(cleanup(body),timeSince,score,subreddit)))
                    .map(lambda (id,(body,timeSince,score,subreddit)): (id,(len(body.split()),body,timeSince,score,subreddit)))) 

# # 6.0 (Filter out exclusions; skip for now, as this will take time to explore data and categorize outliers)

# # 7.0 Run sentiment analysis and calculate posNegDiff using AFINN model
rRDDtscls = (rRDDXtscl.map(lambda (id,(commentLength,body,timeSince,score,subreddit)):  
                        (id,(commentLength,sentiment(body),timeSince,score,subreddit))))

# # 8.0 Set up logistic regression inputs with OHE features for categorical variable subredddit
rawData = (rRDDtscls.map(lambda (id,(commentLength,posNegDiff,timeSince,score,subreddit)):  
                    (label(score,subreddit,srDigestR), (0,commentLength), (1,posNegDiff), (2,timeSince), subreddit)))    

# Use randomSplit with weights and seed
rawTrainData, rawValData, rawTestData = rawData.randomSplit([.8, .1, .1], 42)

# Create one hot encoding mapping, format LabeledPoint, and set up training data.
OHETrainData = (rawTrainData.map(lambda (label, t1, t2, t3, sr):
                                       (label, t1, t2, t3, createOHEMap(sr) ))
                            .map(lambda point:  createLabeledPoint(point, 6))
                            .setName("OHETrainData")
                            .persist(StorageLevel.MEMORY_AND_DISK_SER))

# # 9.0 Run logistic regression
# Train model
model0 = LogisticRegressionWithSGD.train(OHETrainData, iterations=50, step=1.,regParam=1e-6,regType='l2',
                                        intercept = True, validateData = False)

# Print results
print model0.weights, model0.intercept 
print OHETrainData.map(lambda point:  1 if model0.predict(point.features) == point.label else 0).sum()
print OHETrainData.count()
print "Accuracy on training set: ", float(model0TotalCorrect) / float(OHETrainDataCount) 