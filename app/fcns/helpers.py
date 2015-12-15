
import re
from afinn import Afinn # import afinn, used for sentiment analysis
from pyspark.sql.types import StructField, BooleanType, StringType, LongType, StructType # For json schema for read
from pyspark.sql import SQLContext, HiveContext
from pyspark.mllib.regression import LabeledPoint # Stuff for logistic regression
from pyspark.mllib.linalg import SparseVector

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

def createsrDict(df, srList, isIn, hiveContext):
    hiveContext.registerDataFrameAsTable(df, "rcomments")
    srDigest = {}
    for key in srList:
        if isIn[key]:  # if the subreddit is in the input data set 
            SQL = "select percentile(score, array(0.03,0.97)) from rcomments where subreddit=="+"'" + key + "'"
            srDigest[key] = hiveContext.sql(SQL).collect()[0][0]
    return srDigest

def cleanup(body):
	body = re.sub("&gt;", ">", body) # Recode HTML codes
	body = re.sub("&lt;", "<", body)
	body = re.sub("&amp;", "&", body)
	body = re.sub("&nbsp;", " ", body)
	body = re.sub("^[deleted]$", "", body) # Remove deleted
	body = re.sub("http[[:alnum:][:punct:]]*", " ", body) # Remove URL
	body = re.sub("/r/[[:alnum:]]+|/u/[[:alnum:]]+", " ", body) # Remove /r/subreddit, /u/user
	body = re.sub("(>.*?\\n\\n)+", " ", body) # Remove quoted comments
	body = re.sub("[[:cntrl:]]", " ", body) # Remove control characters (\n, \b)
	body = re.sub("'", "", body) # Remove single quotation marks (contractions)
	body = re.sub("[[:punct:]]", " ", body) # Remove punctuation
	body = re.sub("\\s+", " ", body) # Replace multiple spaces with single space
	body = body.strip()
	body = body.lower() # Lower case
	return body # Return body (cleaned up text)

def sentiment(body):
    afinn = Afinn()
    return afinn.score(body)

def label(score, subreddit, percentMap):
    if score <= percentMap[subreddit][0]: 
    	return 0
    else: 
    	return 1

def createOHEMap(sr):
    if sr == u'leagueoflegends': 
    	return (3,1)
    elif sr == u'pics' : 
    	return (4,1)
    elif sr == u'politics' :
    	return (5,1)
    else: 
    	return (5,0)

def createLabeledPoint(point,numFeats):
    label = point[0]
    feats = point[1:]
    sv = SparseVector(numFeats, feats)
    return LabeledPoint(label, sv)