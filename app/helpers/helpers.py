"""
This module contains helper functions for logistic regression on selected subreddit comments
within the Reddit corpus.

Constants defined in this module:
    fields:  schema for reading Reddit comments in JSON format

Functions in this module:
    create_sr_dict:  return dictionary containing 3rd and 97th percentile scores, key is subreddit
    cleanup:  use regular expressions to clean up comment text, e.g., punctuation etc.
    sentiment:  calculate sentiment using Afinn model
    label:  label data points based on value of score (either up or down)
    create_ohe_map:  create one hot encoding map of categorical feature (subreddit)
    create_labeled_point:  create LabeledPoint data structure from data point
"""

import re

from pyspark.sql.types import StructField, BooleanType, StringType, LongType #, StructType # schema
# from pyspark.sql import SQLContext, HiveContext
from pyspark.mllib.regression import LabeledPoint # Stuff for logistic regression
from pyspark.mllib.linalg import SparseVector

from afinn import Afinn # import afinn, used for sentiment analysis

"""
fields:  schema for reading Reddit comments in JSON format.
speeds up reading JSON by a factor of 2.
"""
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

def create_sr_dict(df, srlist, isin, hiveContext):
    """
    return dictionary containing 3rd and 97th percentile scores, key is subreddit
    :type df:  SparkSQL DataFrame
    :type srlist:  List[unicode str]
    :type isin:  Dictionary
    :type hiveContext:  SparkSQL HiveContext
    :rtype: Dictionary
    """
    hiveContext.registerDataFrameAsTable(df, "rcomments")
    sr_digest = {}
    for key in srlist:
        if isin[key]:  # if the subreddit is in the input data set
            sql = ("select percentile(score, array(0.03,0.97)) from rcomments"
                   "where subreddit=="+"'" + key + "'")
            sr_digest[key] = hiveContext.sql(sql).collect()[0][0]
    return sr_digest

def cleanup(body):
    """
    use regular expressions to clean up comment text, e.g., punctuation etc.
    :type body:  unicode str
    :rtype: unicode str
    """
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
    """
    calculate sentiment using Afinn model
    :type body:  unicode str
    :rtype: int
    """
    afinn = Afinn()
    return afinn.score(body)

def label(score, subreddit, percent_map):
    """
    label data points based on value of score (either up or down)
    :type score:  int
    :type subreddit:  unicode str
    :type percent_map:  Dictionary
    :rtype: int
    """
    if score <= percent_map[subreddit][0]:
        return 0
    else:
        return 1

def create_ohe_map(sr):
    """
    create one hot encoding map of categorical feature (subreddit)
    :type sr:  unicode str
    :rtype: tuple
    """
    if sr == u'leagueoflegends':
        return (3, 1)
    elif sr == u'pics':
        return (4, 1)
    elif sr == u'politics':
        return (5, 1)
    else:
        return (5, 0)

def create_labeled_point(point, num_feats):
    """
    create LabeledPoint data structure from data point
    :type point:  tuple
    :type num_feats:  int
    :rtype: Spark LabeledPoint
    """
    label = point[0]
    feats = point[1:]
    sv = SparseVector(num_feats, feats)
    return LabeledPoint(label, sv)
