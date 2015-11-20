
# coding: utf-8

# # 0.0 Import packages and set up Spark context, SQL context and Hive context.


import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os
import sys
import re
import numpy as np
import time
import datetime
 
# Path for spark source folder
os.environ['SPARK_HOME'] = "/usr/local/spark"

# Append pyspark to Python Path
sys.path.append("/usr/local/spark/python")
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext

sc = SparkContext() # not needed in IPython notebook.
sqlContext = SQLContext(sc)
hiveContext = HiveContext(sc)

# Append afinn to Python Path and import afinn, used for sentiment analysis.
sys.path.append("/usr/local/lib/python2.7/dist-packages/afinn")
from afinn import Afinn

# Stuff for logistic regression
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.linalg import SparseVector
from pyspark.sql.types import StructField, BooleanType, StringType, LongType, StructType
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from numpy.random import random
from operator import add


# # 1.0 Read data
# Define json schema to speed up reading json files on S3 (about 2x improvement)


fields = [StructField("archived", BooleanType(), True),
        StructField("author", StringType(), True),
        StructField("author_flair_css_class", StringType(), True),
        StructField("body", StringType(), True),
        StructField("controversiality", LongType(), True),
        StructField("created_utc", StringType(), True),
        StructField("distinguished", StringType(), True),
        StructField("downs", LongType(), True),
        StructField("edited", StringType(), True),
        StructField("gilded", LongType(), True),
        StructField("id", StringType(), True),
        StructField("link_id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("parent_id", StringType(), True),
        StructField("retrieved_on", LongType(), True),
        StructField("score", LongType(), True),
        StructField("score_hidden", BooleanType(), True),
        StructField("subreddit", StringType(), True),
        StructField("subreddit_id", StringType(), True),
        StructField("ups", LongType(), True)]
df = hiveContext.read.json("s3n://reddit-comments/*", StructType(fields))

# Filter down to subreddits of interest

subreddits = [u'leagueoflegends', u'GirlGamers', u'pics', u'politics']
df2 = (df.filter(  (df.subreddit == u'leagueoflegends') 
                 | (df.subreddit == u'GirlGamers')
                 | (df.subreddit == u'pics')
                 | (df.subreddit == u'politics') )
           .persist(StorageLevel.MEMORY_AND_DISK_SER)
           )
df2.count() # Forces read in df, execute df2 BEFORE coalesce().

isInData = {key: True for key in subreddits}


# # 2.0 Filter to include only extreme up and down votes (top/bottom 3% of subreddit)


# Reduces dataset for all subsequent processing.

def createsrDict(df, srList, isIn):
    hiveContext.registerDataFrameAsTable(df, "rcomments")
    srDigest = {}
    for key in srList:
        if isIn[key]:  # if the subreddit is in the input data set 
            SQL = "select percentile(score, array(0.03,0.97)) from rcomments where subreddit=="+"'" + key + "'"
            srDigest[key] = hiveContext.sql(SQL).collect()[0][0]
    return srDigest

subredditDigest = createsrDict(df2, subreddits, isInData) 

srDigestR = {key : (round(subredditDigest[key][0]), 
                    round(subredditDigest[key][1]) ) 
             for key in subredditDigest.keys()}  

# Put Dataframe into vanilla RDD

rRDD = (df2.map(lambda r: (r.id, (r.body, int(r.created_utc), r.link_id, r.parent_id, int(r.score), r.subreddit, r.subreddit_id)))
       )

rRDDExtreme = (rRDD.filter(lambda (k,v): v[4] < srDigestR[v[5]][0] or v[4] > srDigestR[v[5]][1])
                  .coalesce(400)
                  .setName("rRDDExtreme")
                  .persist(StorageLevel.MEMORY_AND_DISK_SER)
               )
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
# Using broadcast variable avoids  having to do another join.  
# Map RDD to get post link_id as key, then subtract minTime to get timeSince.

rRDDXts = (rRDDExtreme.map(lambda (k,v):  (v[2],(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6])))  # pull link_id as key
                      .map(lambda (link_id,(x)):  (x[0], (x[1],x[2]-minTimeBR.value[link_id],x[5],x[6])))
          )


# # 5.0  Calculate commentLength


# Clean up body using regular expressions before calculating length.

def cleanup(body):

	# Recode HTML codes
	body = re.sub("&gt;", ">", body)
	body = re.sub("&lt;", "<", body)
	body = re.sub("&amp;", "&", body)
	body = re.sub("&nbsp;", " ", body)

	# Remove deleted
	body = re.sub("^[deleted]$", "", body)

	# Remove URL
	body = re.sub("http[[:alnum:][:punct:]]*", " ", body) # url

	# Remove /r/subreddit, /u/user
	body = re.sub("/r/[[:alnum:]]+|/u/[[:alnum:]]+", " ", body)

	# Remove quoted comments
	body = re.sub("(>.*?\\n\\n)+", " ", body)

	# Remove control characters (\n, \b)
	body = re.sub("[[:cntrl:]]", " ", body)

	# Remove single quotation marks (contractions)
	body = re.sub("'", "", body)

	# Remove punctuation
	body = re.sub("[[:punct:]]", " ", body)

	# Replace multiple spaces with single space
	body = re.sub("\\s+", " ", body) # Multiple spaces
	body = body.strip()

	# Lower case
	body = body.lower()

	# Return comment length (number of words) and body (cleaned up text)
	return body

rRDDXtscl = (rRDDXts.map(lambda (id,(body,timeSince,score,subreddit)): (id,(cleanup(body),timeSince,score,subreddit)))
                    .map(lambda (id,(body,timeSince,score,subreddit)): (id,(len(body.split()),body,timeSince,score,subreddit)))
             ) 


# # 6.0 (Filter out exclusions; skip for now, as this will take time to explore data and categorize outliers)


# # 7.0 Run sentiment analysis and calculate posNegDiff using AFINN model


def sentiment(body):
    afinn = Afinn()
    return afinn.score(body)

rRDDtscls = (rRDDXtscl.map(lambda (id,(commentLength,body,timeSince,score,subreddit)):  
                        (id,(commentLength,sentiment(body),timeSince,score,subreddit)))
             )


# # 8.0 Set up logistic regression inputs with OHE features for categorical variable subredddit


def label(score, subreddit, percentMap):
    if score <= percentMap[subreddit][0]: return 0
    else: return 1
    
rawData = (rRDDtscls.map(lambda (id,(commentLength,posNegDiff,timeSince,score,subreddit)):  
                    (label(score,subreddit,srDigestR), (0,commentLength), (1,posNegDiff), (2,timeSince), subreddit))
          )    

weights = [.8, .1, .1]
seed = 42

# Use randomSplit with weights and seed

rawTrainData, rawValData, rawTestData = rawData.randomSplit(weights, seed)

# Create one hot encoding mapping, format LabeledPoint, and set up training data.

def createOHEMap(sr):
    if sr == u'leagueoflegends': return (3,1)
    elif sr == u'pics' : return (4,1)
    elif sr == u'politics' : return (5,1)
    else: return (5,0)
    
def createLabeledPoint(point,numFeats):
    label = point[0]
    feats = point[1:]
    sv = SparseVector(numFeats, feats)
    return LabeledPoint(label, sv)

numFeats = 6
OHETrainData = (rawTrainData.map(lambda (label, t1, t2, t3, sr):
                                       (label, t1, t2, t3, createOHEMap(sr) ))
                            .map(lambda point:  createLabeledPoint(point, numFeats))
                            .setName("OHETrainData")
                            .persist(StorageLevel.MEMORY_AND_DISK_SER)
                )


# (Create OHEValData and OHETestData; skip for now)


# # 9.0 Run logistic regression


# Set up hyperparameters

numIters = 50
stepSize = 1.
regParam = 1e-6
regType = 'l2'
includeIntercept = True
validateData = False

# Train model

model0 = LogisticRegressionWithSGD.train(OHETrainData, iterations = numIters, step = stepSize,
                                        regParam = regParam, regType = regType,
                                        intercept = includeIntercept, validateData = validateData)

# Print results

print model0.weights, model0.intercept
model0TotalCorrect = OHETrainData.map(lambda point:  1 if model0.predict(point.features) == point.label else 0).sum()
print model0TotalCorrect
OHETrainDataCount = OHETrainData.count()
print OHETrainDataCount
print "Accuracy on training set:" 
print float(model0TotalCorrect) / float(OHETrainDataCount)