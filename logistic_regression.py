
# coding: utf-8

# In[1]:

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
# Load in the testing code and check to see if your answer is correct
# If incorrect it will report back '1 test failed' for each failed test
# Make sure to rerun any cell you change before trying the test again
# from test_helper import Test
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
# sc = SparkContext() # not needed in IPython notebook.
sqlContext = SQLContext(sc)
hiveContext = HiveContext(sc)

# Append afinn to Python Path and import afinn.  Used for pulling data from percentiles.
sys.path.append("/usr/local/lib/python2.7/dist-packages/afinn")
from afinn import Afinn

# Stuff for logistic regression
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.linalg import SparseVector
from pyspark.sql.types import StructField, BooleanType, StringType, LongType, StructType
sys.path.append("/usr/local/lib/python2.7/dist-packages")
# from tdigest import TDigest
from numpy.random import random
from operator import add


# # 1.0 Read data

# Read using json schema.  If you don't use schema on read, Spark reads ENTIRE FILE to infer schema BEFORE actually reading in data.

# In[ ]:

# Define json schema to speed up reading json files in S3

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
# df.take(5)

# Refactor later to filter based on subreddits list. You can't do "in list" with SQL but maybe dataframe DSL. 
# Filter down to subreddits of interest
subreddits = [u'leagueoflegends', u'GirlGamers', u'pics', u'politics']
df2 = (df.filter(  (df.subreddit == u'leagueoflegends') 
                 | (df.subreddit == u'GirlGamers')
                 | (df.subreddit == u'pics')
                 | (df.subreddit == u'politics') )
           # .coalesce(400) Can't coalesce here with 1 TB input.  If you do, it coalesces prematurely and read fails.
           .persist(StorageLevel.MEMORY_AND_DISK_SER)
           )
df2.count() # Forces read in df, execute df2 BEFORE coalesce().

# df2.coalesce(400)  # Now coalesce after read.  THIS DOESN'T WORK.  IGNORES coalesce()

isInData = {key: True for key in subreddits}


# # 2.0 Filter to include only extreme up and down votes (top 3% of subreddit)

# Filter to retain only records that are top or bottom 3% in comment score (upvotes-downvotes) of their subreddit.  Reduces dataset for all subsequent processing.

# ALTERNATIVE calculation of 3 and 97 percentiles using SQL and HiveQL percentile estimate.

# In[ ]:

def createsrDict(df, srList, isIn):
    hiveContext.registerDataFrameAsTable(df, "rcomments")
    srDigest = {}
    for key in srList:
        if isIn[key]:  # if the subreddit is in the input data set 
            # not sure if percentile() [integers] or percentile_approx() [double] runs faster.
            SQL = "select percentile(score, array(0.03,0.97)) from rcomments where subreddit=="+"'" + key + "'"
            srDigest[key] = hiveContext.sql(SQL).collect()[0][0]
    return srDigest

subredditDigest = createsrDict(df2, subreddits, isInData) 

srDigestR = {key : (round(subredditDigest[key][0]), 
                    round(subredditDigest[key][1]) ) 
             for key in subredditDigest.keys()}
print srDigestR  

# Put Dataframe into vanilla RDD

rRDD = (df2.map(lambda r: (r.id, (r.body, int(r.created_utc), r.link_id, r.parent_id, int(r.score), r.subreddit, r.subreddit_id)))
          # .setName("rRDD")
          # .persist(StorageLevel.MEMORY_AND_DISK_SER) # Do not persist.  Not used after rRDDExtreme.
       )
# rRDD.take(5)

rRDDExtreme = (rRDD.filter(lambda (k,v): v[4] < srDigestR[v[5]][0] or v[4] > srDigestR[v[5]][1])
                  .coalesce(400)
                  .setName("rRDDExtreme")
                  .persist(StorageLevel.MEMORY_AND_DISK_SER)
               )
rRDDExtreme.count() # force evaluation of this RDD


# # 1.0 Find minimum comment timestamp for each post

# Turn rRDDExtreme into dataframe of just link_id.   Format of rRDD and rRDDExtreme:  
# (r.id, (r.body, int(r.created_utc), r.link_id, r.parent_id, int(r.score), r.subreddit, r.subreddit_id))

# Find min time comments for 100% of subreddits of interest using HiveQL.  

# In[ ]:

rRDDExtremeLinks = rRDDExtreme.map(lambda (k,v): [v[2]])
dfExtreme = sqlContext.createDataFrame(rRDDExtremeLinks,["xlink_id"]).distinct()
# sqlContext.registerDataFrameAsTable(dfExtreme, "xtable")

# Find minimum time comments for each post and register as table

minTimeDF = hiveContext.sql("select link_id, min(cast (created_utc as int)) as min_utc from rcomments group by link_id")
    
# sqlContext.registerDataFrameAsTable(minTimeDF, "mintable")

# Create new dataframe with min time utc for ONLY link_id's referenced in top/bottom 3%.

minTimeDFX = dfExtreme.join(minTimeDF, dfExtreme.xlink_id == minTimeDF.link_id, 'inner').drop('xlink_id')
# SQL = "select link_id, min_utc from mintable inner join xtable on mintable.link_id = xtable.link_id"
# minTimeDFX = sqlContext.sql(SQL)
minTimeDict = dict(minTimeDFX.collect())
minTimeBR = sc.broadcast(minTimeDict)
len(minTimeDict)


# minTimeDFX.columns are ['link_id', 'min_utc']

# Example row of minTimeDFX:  Row(link_id=u't3_31j8f1', link_id=u't3_31j8f1', min_utc=1428253005)

# # 3.0  Calculate timeSince

# Calculate time since post was created based on created_utc and min_created_utc from pair RDD.  In Alyssa's IPython notebook this is called timeSince.  In her R code it's called recency.  
# 
# Using broadcast variable avoids  having to do a join.  
# 
# Map RDD to get post link_id as key, then subtract minTime to get timeSince.
# 
# Format of output RDD is (id,(body,timeSince,score,subreddit))

# In[7]:

# Calculate timeSince

rRDDXts = (rRDDExtreme.map(lambda (k,v):  (v[2],(k,v[0],v[1],v[2],v[3],v[4],v[5],v[6])))  # pull link_id as key
                      .map(lambda (link_id,(x)):  (x[0], (x[1],x[2]-minTimeBR.value[link_id],x[5],x[6])))
                      # .setName("rRDDXts")
                      # .persist(StorageLevel.MEMORY_AND_DISK_SER)
          )


# # 4.0  Calculate commentLength

# Clean comment body and calculate commentLength.
# 
# R gsub:
# gsub(pattern, replacement, x, ignore.case = FALSE, perl = FALSE, fixed = FALSE, useBytes = FALSE)
# 
# Python re:
# re.sub(pattern, repl, string, count=0, flags=0).  Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement repl.
# 
# NOTE:  ALYSSA REMOVED QUOTED COMMENTS.  I REMOVING THEM ALSO BUT IN MY FIRST EXAMPLE I FOUND A "MADE UP" QUOTE THAT ISN'T REALLY QUOTING SOMEONE ELSE'S POST.  

# In[8]:

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
             ) # .setName("rRDDXtscl").persist(StorageLevel.MEMORY_AND_DISK_SER)


# Current format of RDD:  (id,(body,timeSince,score,subreddit))
# Format of rRDDXtscl:  (id,(commentLength,body,timeSince,score,subreddit))

# # 5.0 (Filter out exclusions if necessary; skip for now)

# Filter out exclusions.  Further reduces dataset.

# <b>NOTE:  THIS MIGHT BE RESPONSIBLE FOR POOR ACCURACY; I'M NOT GETTING RID OF OUTLIERS.

# # 6.0 Run sentiment analysis and calculate posNegDiff

# Use AFINN model to do sentiment analysis.
# 
# Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs" , Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors) 

# In[9]:

def sentiment(body):
    afinn = Afinn()
    return afinn.score(body)

rRDDtscls = (rRDDXtscl.map(lambda (id,(commentLength,body,timeSince,score,subreddit)):  
                        (id,(commentLength,sentiment(body),timeSince,score,subreddit)))
                      # .setName("rRDDtscls")
                      # .persist(StorageLevel.MEMORY_AND_DISK_SER)
             )


# # 7.0 Set up logistic regression inputs with OHE features for categorical variable subredddit

# Calculate label from score using srDigestR and create rawData RDD in proper format:  (label, non-categorical variables, categorical variable)

# Format of rRDDtscls:  (id,(commentLength,posNegDiff,timeSince,score,subreddit)))
# 
# Format of rawData is a tuple:  (label, (0,commentLength), (1,posNegDiff), (2,timeSince), subreddit))

# In[10]:

def label(score, subreddit, percentMap):
    if score <= percentMap[subreddit][0]: return 0
    else: return 1
    
rawData = (rRDDtscls.map(lambda (id,(commentLength,posNegDiff,timeSince,score,subreddit)):  
                    (label(score,subreddit,srDigestR), (0,commentLength), (1,posNegDiff), (2,timeSince), subreddit))
                    # .setName("rawData")
                    # .persist(StorageLevel.MEMORY_AND_DISK_SER)
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
    # print sv
    return LabeledPoint(label, sv)

# numFeats = len(OHEdict)+3
numFeats = 6
OHETrainData = (rawTrainData.map(lambda (label, t1, t2, t3, sr):
                                       (label, t1, t2, t3, createOHEMap(sr) ))
                            .map(lambda point:  createLabeledPoint(point, numFeats))
                            .setName("OHETrainData")
                            .persist(StorageLevel.MEMORY_AND_DISK_SER)
                )


# (Create OHEValData and OHETestData; skip for now)

# OHEValData = (rawValData.map(lambda (label, t1, t2, t3, sr):
#                                        (label, t1, t2, t3, (OHEdict[(0,sr)], 1) ))
#                             .map(lambda point:  createLabeledPoint(point, numFeats))
#                 )

# OHETestData = (rawTestData.map(lambda (label, t1, t2, t3, sr):
#                                        (label, t1, t2, t3, (OHEdict[(0,sr)], 1) ))
#                             .map(lambda point:  createLabeledPoint(point, numFeats))
#                 )

# # 8.0 Run logistic regression

# Set up hyperparameters

# In[ ]:

# fixed hyperparameters
numIters = 50
stepSize = 1.
regParam = 1e-6
regType = 'l2'
includeIntercept = True
validateData = False

model0 = LogisticRegressionWithSGD.train(OHETrainData, iterations = numIters, step = stepSize,
                                        regParam = regParam, regType = regType,
                                        intercept = includeIntercept, validateData = validateData)

print model0.weights, model0.intercept
model0TotalCorrect = OHETrainData.map(lambda point:  1 if model0.predict(point.features) == point.label else 0).sum()
print model0TotalCorrect
OHETrainDataCount = OHETrainData.count()
print OHETrainDataCount
print "Accuracy on training set:" 
print float(model0TotalCorrect) / float(OHETrainDataCount)


# In[12]:

print model0.weights, model0.intercept
model0TotalCorrect = OHETrainData.map(lambda point:  1 if model0.predict(point.features) == point.label else 0).sum()
print model0TotalCorrect
OHETrainDataCount = OHETrainData.count()
print OHETrainDataCount
print "Accuracy on training set:" 
print float(model0TotalCorrect) / float(OHETrainDataCount)

