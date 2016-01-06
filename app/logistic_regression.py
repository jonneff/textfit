"""
This script performs logistic regression on selected subreddit comments within the Reddit
corpus.  The script cleans and prepares comments and trains a model to predict whether a
comment will be voted up or down.  See section 0.0 Import to configure Spark source and
add PySpark and afinn to path.  See 1.0 Read data to configure input file for comment data.

Usage:  spark-submit logistic_regression.py

NOTE:  Certain PEP8 conventions are not followed here as they conflict with standard
PySpark usage, e.g., sc for SparkContext constant.  When continuing chained RDD transformations
and actions, continuing line is indented to line up method calls on "."
"""
# coding: utf-8

# # 0.0 Import packages and set up Spark context, SQL context and Hive context.
import os
import sys

from pyspark import SparkContext, StorageLevel #, SparkConf
from pyspark.sql import SQLContext, HiveContext
from pyspark.sql.types import StructType
from pyspark.mllib.classification import LogisticRegressionWithSGD

from helpers.helpers import * # Import helper functions

os.environ['SPARK_HOME'] = "/usr/local/spark" # Path for spark source folder
sys.path.append("/usr/local/spark/python") # Append pyspark to Python Path
sys.path.append("/usr/local/lib/python2.7/dist-packages/afinn") # Append afinn to Python Path
sys.path.append("/usr/local/lib/python2.7/dist-packages")

sc = SparkContext() # not needed in IPython notebook.
sqlContext = SQLContext(sc)
hiveContext = HiveContext(sc)

# # 1.0 Read data
# fields defines json schema to speed up reading json files on S3 (about 2x improvement)
# Project used 908 GB in "s3n://reddit-comments/*" restricted to Insight.  Instead, use 2007 data.
df = hiveContext.read.json("../data/*", StructType(fields))

# Filter down to subreddits of interest
subreddits = [u'leagueoflegends', u'GirlGamers', u'pics', u'politics']
df2 = (df.filter((df.subreddit == u'leagueoflegends')|(df.subreddit == u'GirlGamers')|
                 (df.subreddit == u'pics')|(df.subreddit == u'politics'))
         .persist(StorageLevel.MEMORY_AND_DISK_SER))
df2.count() # Forces read in df, execute df2 BEFORE coalesce().
is_in_data = {key: True for key in subreddits}

# # 2.0 Filter to include only extreme up and down votes (top/bottom 3% of subreddit)
# Reduces dataset for all subsequent processing.
subreddit_digest = create_sr_dict(df2, subreddits, is_in_data, hiveContext)
sr_digest_r = {key : (round(subreddit_digest[key][0]), round(subreddit_digest[key][1]))
               for key in subreddit_digest.keys()}

# Put Dataframe into vanilla RDD
r_rdd = (df2.map(lambda r: (r.id, (r.body, int(r.created_utc), r.link_id, r.parent_id, int(r.score),
                                   r.subreddit, r.subreddit_id))))

r_rdd_extreme = (r_rdd.filter(lambda (k, v): v[4] < sr_digest_r[v[5]][0] or
                                             v[4] > sr_digest_r[v[5]][1])
                      .coalesce(400)
                      .setName("r_rdd_extreme")
                      .persist(StorageLevel.MEMORY_AND_DISK_SER))
r_rdd_extreme.count() # force evaluation of RDD to reduce partitions (coalesce), prepare for join.

# # 3.0 Find minimum comment timestamp for each post using HiveQL percentile UDF.
# This is a proxy for the post timestamp, which was unavailable at the time this project was done.
r_rdd_extreme_links = r_rdd_extreme.map(lambda (k, v): [v[2]])
df_extreme = sqlContext.createDataFrame(r_rdd_extreme_links, ["xlink_id"]).distinct()

# Find minimum time comments for each post and register as table
hsql = "select link_id, min(cast (created_utc as int)) as min_utc from rcomments group by link_id"
min_time_df = hiveContext.sql(hsql)

# Create dataframe with min time utc for ONLY link_id's in top/bottom 3% using Dataframe join.
min_time_df_x = (df_extreme.join(min_time_df, df_extreme.xlink_id == min_time_df.link_id, 'inner')
                           .drop('xlink_id'))

# Create minimum time dictionary and broadcast to workers
min_time_dict = dict(min_time_df_x.collect())
min_time_br = sc.broadcast(min_time_dict)

# # 4.0  Calculate timeSince
# Calculate time since post was created based on created_utc and min_created_utc from pair RDD.
# Broadcast variable avoids another join.
# Map RDD, get post link_id as key, subtract minTime, get timeSince.  Pull link_id as key.
r_rdd_x_ts = (
             r_rdd_extreme.map(lambda (k, v): (v[2], (k, v[0], v[1], v[2], v[3], v[4], v[5], v[6])))
                          .map(lambda (link_id, (x)): (x[0], (x[1], x[2]-min_time_br.value[link_id],
                                                       x[5], x[6])))
             )

# # 5.0  Clean up body and calculate commentLength
r_rdd_x_tscl = (r_rdd_x_ts.map(lambda (id, (body, timeSince, score, subreddit)):
                              (id, (cleanup(body), timeSince, score, subreddit)))
                          .map(lambda (id, (body, timeSince, score, subreddit)):
                              (id, (len(body.split()), body, timeSince, score, subreddit))))

# # 6.0 (Filter out exclusions; skip for now, will take time to explore data, categorize outliers)

# # 7.0 Run sentiment analysis and calculate posNegDiff using AFINN model
r_rdd_tscls = (r_rdd_x_tscl.map(lambda (id, (commentLength, body, timeSince, score, subreddit)):
                               (id, (commentLength, sentiment(body), timeSince, score, subreddit))))

# # 8.0 Set up logistic regression inputs with OHE features for categorical variable subredddit
raw_data = (r_rdd_tscls.map(lambda (id, (commentLength, posNegDiff, timeSince, score, subreddit)):
                                   (label(score, subreddit, sr_digest_r), (0, commentLength),
                                   (1, posNegDiff), (2, timeSince), subreddit)))

# Use randomSplit with weights and seed
raw_train_data, raw_val_data, raw_test_data = raw_data.randomSplit([.8, .1, .1], 42)

# Create one hot encoding mapping, format LabeledPoint, and set up training data.
ohe_train_data = (raw_train_data.map(lambda (label, t1, t2, t3, sr):
                                            (label, t1, t2, t3, create_ohe_map(sr)))
                                .map(lambda point: create_labeled_point(point, 6))
                                .setName("ohe_train_data")
                                .persist(StorageLevel.MEMORY_AND_DISK_SER))

# # 9.0 Run logistic regression
# Train model
model0 = LogisticRegressionWithSGD.train(ohe_train_data, iterations=50, step=1., regParam=1e-6,
                                         regType='l2', intercept=True, validateData=False)

# Print results
print model0.weights, model0.intercept
correct = ohe_train_data.map(lambda point: 1 if model0.predict(point.features) == point.label
                             else 0).sum()
count = ohe_train_data.count()
print "Accuracy on training set: ", float(correct) / float(count)
sc.stop()
