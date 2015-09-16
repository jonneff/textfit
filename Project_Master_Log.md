Project Master Log

TextFit (http://textfit.me)


Description
TextFit is an app that provides users with feedback on a comment that they want to submit before they submit it, specifically how well their comment “fits” into the community they are submitting to.
Target use case is for people who may have a tendency to flame/rage/say negative things on the internet or for people who don’t know how other people will react to their comment. (E.g., Sometimes emotions run high when playing a video game, and people say something that they don’t mean out of anger. My app would provide a “check” that helps people pause and reconsider whether that’s something they would want to say.)
Used Reddit data where there is an upvote/downvote system (can get at whether the comment “fits” or doesn’t fit).


Bottlenecks for the data scientist
Obtaining data
Collected 1000 top posts from 4 subreddits; limited posts to ones with 350 comments or less because download time was too high
Comments are nested within “more comments” links. Each “opening” of a “more comments” link required a separate API call


Processing time when analyzing the data
First attempt to analyze data with Bayesian classifier. Had to run the process overnight.
Tried it two or three times but results were garbage (not enough data).


Goals


Collect more data and scale the project


Logistic Regression (Must implement)
Predict the likelihood of being upvoted or downvoted
Built the model on comments that were highly upvoted or highly downvoted (including neutral comments returned garbage)
Predictors: number of words, positive sentiment, negative sentiment, time since post, comment level (how far down the comment chain the comment is), subreddit


Bayesian classifier of words (Next steps)

What words are associated with comments that have a positive comment score vs. negative comment score


AWS instances, IAM accounts:

2015.09.09

 Good evening everyone,

If anyone is looking to use reddit as a potential data source, we have a bucket in S3 Oregon region containing all of the reddit comments from all the subreddits since 2007. Unfortunately we don't have a script to get more data, since it was purely a data dump. 

You can access the bucket with hadoop or spark at

 s3n://reddit-comments

The following link describes some the schema used for each record

https://archive.org/details/2015_reddit_comments_corpus

Let me know if anyone has trouble accessing it.

 Regards,

Austin

 --------------------

jonneff ~ $ aws s3 ls s3://reddit-comments --recursive --human-readable

2015-09-02 12:59:15    0 Bytes 2007/

2015-09-02 13:10:51   85.4 MiB 2007/RC_2007-10

2015-09-02 13:11:32  201.1 MiB 2007/RC_2007-11

2015-09-02 13:11:43  204.9 MiB 2007/RC_2007-12

2015-09-02 12:59:17    0 Bytes 2008/

2015-09-02 13:25:36  251.7 MiB 2008/RC_2008-01

2015-09-02 13:25:41  244.7 MiB 2008/RC_2008-02

2015-09-02 13:25:49  255.5 MiB 2008/RC_2008-03

2015-09-02 13:25:56  260.0 MiB 2008/RC_2008-04

2015-09-02 13:26:05  296.0 MiB 2008/RC_2008-05

2015-09-02 13:26:14  320.5 MiB 2008/RC_2008-06

2015-09-02 13:26:24  330.1 MiB 2008/RC_2008-07

2015-09-02 13:26:34  330.6 MiB 2008/RC_2008-08

2015-09-02 13:26:44  377.7 MiB 2008/RC_2008-09

2015-09-02 13:26:56  435.5 MiB 2008/RC_2008-10

2015-09-02 13:27:09  433.8 MiB 2008/RC_2008-11

2015-09-02 13:27:23  467.9 MiB 2008/RC_2008-12

2015-09-02 12:59:20    0 Bytes 2009/

2015-09-02 13:54:51  580.7 MiB 2009/RC_2009-01

2015-09-02 13:55:07  524.1 MiB 2009/RC_2009-02

2015-09-02 13:55:23  587.2 MiB 2009/RC_2009-03

2015-09-02 13:55:41  611.8 MiB 2009/RC_2009-04

2015-09-02 13:56:00  679.6 MiB 2009/RC_2009-05

2015-09-02 13:56:20  714.6 MiB 2009/RC_2009-06

2015-09-02 13:56:42  833.5 MiB 2009/RC_2009-07

2015-09-02 13:57:08  990.4 MiB 2009/RC_2009-08

2015-09-02 13:57:39    1.1 GiB 2009/RC_2009-09

2015-09-02 13:58:14    1.2 GiB 2009/RC_2009-10

2015-09-02 13:58:53    1.2 GiB 2009/RC_2009-11

2015-09-02 13:59:31    1.4 GiB 2009/RC_2009-12

2015-09-02 12:59:23    0 Bytes 2010/

2015-09-02 15:07:36    1.6 GiB 2010/RC_2010-01

2015-09-02 15:08:23    1.5 GiB 2010/RC_2010-02

2015-09-02 15:09:11    1.8 GiB 2010/RC_2010-03

2015-09-02 15:10:06    1.7 GiB 2010/RC_2010-04

2015-09-02 15:11:01    1.8 GiB 2010/RC_2010-05

2015-09-02 15:11:58    1.9 GiB 2010/RC_2010-06

2015-09-02 15:12:59    2.2 GiB 2010/RC_2010-07

2015-09-02 15:14:08    2.3 GiB 2010/RC_2010-08

2015-09-02 15:15:20    2.5 GiB 2010/RC_2010-09

2015-09-02 15:16:41    2.7 GiB 2010/RC_2010-10

2015-09-02 15:18:07    3.1 GiB 2010/RC_2010-11

2015-09-02 15:19:44    3.2 GiB 2010/RC_2010-12

2015-09-02 12:59:25    0 Bytes 2011/

2015-09-02 16:49:00    3.6 GiB 2011/RC_2011-01

2015-09-02 16:50:12    3.5 GiB 2011/RC_2011-02

2015-09-02 16:52:40    4.1 GiB 2011/RC_2011-03

2015-09-02 16:52:46    4.1 GiB 2011/RC_2011-04

2015-09-02 16:54:31    4.7 GiB 2011/RC_2011-05

2015-09-02 17:02:27    5.2 GiB 2011/RC_2011-06

2015-09-02 17:02:33    5.6 GiB 2011/RC_2011-07

2015-09-02 19:25:31    6.5 GiB 2011/RC_2011-08

2015-09-02 20:30:19    6.5 GiB 2011/RC_2011-09

2015-09-02 21:34:31    7.2 GiB 2011/RC_2011-10

2015-09-02 21:46:50    7.3 GiB 2011/RC_2011-11

2015-09-02 22:35:13    7.7 GiB 2011/RC_2011-12

2015-09-02 12:59:28    0 Bytes 2012/

2015-09-03 07:38:40    8.8 GiB 2012/RC_2012-01

2015-09-03 08:30:31    8.6 GiB 2012/RC_2012-02

2015-09-03 08:32:43    9.6 GiB 2012/RC_2012-03

2015-09-03 08:40:58   10.2 GiB 2012/RC_2012-04

2015-09-05 08:21:13   11.0 GiB 2012/RC_2012-05

2015-09-06 15:01:40   11.8 GiB 2012/RC_2012-06

2015-09-06 15:01:57   12.9 GiB 2012/RC_2012-07

2015-09-07 00:28:37   13.7 GiB 2012/RC_2012-08

2015-09-07 00:49:47   12.5 GiB 2012/RC_2012-09

2015-09-07 00:56:41   13.3 GiB 2012/RC_2012-10

2015-09-07 09:11:50   13.2 GiB 2012/RC_2012-11

2015-09-07 09:12:11   13.9 GiB 2012/RC_2012-12

2015-09-02 12:59:30    0 Bytes 2013/

2015-09-07 17:27:21   16.2 GiB 2013/RC_2013-01

2015-09-07 17:42:40   14.7 GiB 2013/RC_2013-02

2015-09-07 17:55:21   17.1 GiB 2013/RC_2013-03

2015-09-07 16:37:41   18.4 GiB 2013/RC_2013-04

2015-09-07 18:10:32   17.7 GiB 2013/RC_2013-05

2015-09-07 18:29:03   17.5 GiB 2013/RC_2013-06

2015-09-07 18:29:33   18.8 GiB 2013/RC_2013-07

2015-09-07 19:59:24   18.7 GiB 2013/RC_2013-08

2015-09-07 19:59:34   17.2 GiB 2013/RC_2013-09

2015-09-07 20:43:39   19.3 GiB 2013/RC_2013-10

2015-09-07 21:43:11   20.0 GiB 2013/RC_2013-11

2015-09-08 00:20:48   21.3 GiB 2013/RC_2013-12

2015-09-02 12:59:32    0 Bytes 2014/

2015-09-08 18:15:08   23.7 GiB 2014/RC_2014-01

2015-09-08 18:15:15   21.8 GiB 2014/RC_2014-02

2015-09-08 18:15:27   23.9 GiB 2014/RC_2014-03

2015-09-08 18:15:36   23.8 GiB 2014/RC_2014-04

2015-09-08 21:27:17   24.0 GiB 2014/RC_2014-05

2015-09-08 21:27:36   23.6 GiB 2014/RC_2014-06

2015-09-08 21:28:23   26.4 GiB 2014/RC_2014-07

2015-09-08 21:28:50   26.2 GiB 2014/RC_2014-08

2015-09-08 22:34:51   24.4 GiB 2014/RC_2014-09

2015-09-08 23:29:19   25.8 GiB 2014/RC_2014-10

2015-09-08 23:59:50   25.1 GiB 2014/RC_2014-11

2015-09-09 01:15:25   26.6 GiB 2014/RC_2014-12

2015-09-02 12:59:34    0 Bytes 2015/

2015-09-02 19:30:11   29.5 GiB 2015/RC_2015-01

2015-09-09 09:25:51   26.7 GiB 2015/RC_2015-02

2015-09-09 09:57:02   30.4 GiB 2015/RC_2015-03

2015-09-09 11:19:46   31.3 GiB 2015/RC_2015-04

2015-09-09 11:20:18   31.2 GiB 2015/RC_2015-05

jonneff ~ $

—————

You can’t parallelize gzip unzip, at least on hdfs.  Not sure about S3, but prolly same

http://hvivani.com.ar/2014/11/23/mapreduce-compression-and-input-splits/

—————————

2015.09.13

OBJECTIVE AND PROJECT PLAN

Primary objective, minimum viable product:  process all 1.6B Reddit comments and classify according to upvote/downvote using same features as Alyssa, get comparable accuracy (64%).  Secondary objectives (resurrect Alyssa’s mode, compare to Alyssa on one machine, improve accuracy, do better sentiment analysis, etc.) can wait.  

Specification:  what code has to do:

ZERO:  Unzip files (if zipped, I think they are) and write to S3:  DO THIS ONCE!!!  Might need to automate this and let process run overnight.  WHAT IS QUICKEST WAY TO UNZIP FILES ON S3 AND WRITE BACK TO ANOTHER S3 BUCKET? 

Ingest data
		get key list from S3 bucket (sc.textFile doesn’t work well w/ S3)

		create RDD from key list, map file contents into R

Batch processing:  Spark and MLlib
		DO WHAT ALYSSA DID, BUT WITH SPARK

		write output weights to flat file

Project plan:  how will I do this?

Develop, run and debug using Spark on local laptop, using small dataset, preferably Alyssa’s dataset so I can easily check results.  Otherwise I have to get Alyssa’s code running to check with new data.
Estimate and provision compute resources needed to do copy, unzip as well as logistic regression.  
Get Reddit files from S3, unzip, write decompressed files to HDFS (my cluster)- get data and computation on same cluster. ONLY HAVE TO DO THIS ONCE.
Move my code to cluster, test using small dataset from step 1.
Test using one or two Reddit files on HDFS.
Run on entire dataset.
Pop cork on champagne.  
Produce 1st set of briefing charts.
Add new objective, return to step 1.  
Local Spark install:  /Users/jonneff/spark-1.4.0-bin-hadoop2.6

Too much trouble to get IPython notebook working with Spark.  Instead I will go back to local virtual machine from Spark class.

Created special directory for virtual machine:

/Users/jonneff/myvagrant

 

To start the virtual machine, go to the myvagrant directory and enter

vagrant up

You can see the VM running in Virtual Box.  To stop the virtual machine, enter

vagrant halt

You can also completely delete the virtual machine

vagrant destroy

After destroy, if you enter ‘vagrant up’ it creates a new virtual machine.

Virtual machine gives you access to an Ipython notebook with interface to Spark.

http://localhost:8001

——————————

Alyssa had all her data in a MySQL database.  Question:  should I try to put my data into MySQL to get things up and running or not?  I think not, because that is a detour and not necessary.  Instead I should mod her code to pull in features and labels directly from JSON.  I think.  I’m not using MySQL in for scaled solution.  

Copying a file from S3 to wherever:  http://docs.aws.amazon.com/cli/latest/reference/s3/cp.html

Just downloaded smallest Reddit file.  Guess what?  It appears to be uncompressed JSON.  This simplifies things quite a bit, don’t you think?  :)

So all files in Reddit dataset are less than 1 Terabyte, about 908 GB.  

Having a devil of a time getting IPython notebook running with Spark on local machine.  Keep getting the following error message when I try to initialize a Spark context:

Exception: Java gateway process exited before sending the driver its port number
There are a number of other people having the same problem with various solutions offered, none of which worked for me.
https://forums.databricks.com/questions/1662/spark-python-java-gateway-process-exited-before-se.html
So I’m stuck.  Looks like this:
INPUT
import matplotlib.pyplot as plt
import json
import os
import sys
 
# Path for spark source folder
os.environ['SPARK_HOME'] = "/Users/jonneff/spark-1.4.0-bin-hadoop2.6"
 
# Append pyspark to Python Path
sys.path.append("/Users/jonneff/spark-1.4.0-bin-hadoop2.6/python")
 
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
conf = SparkConf().setMaster("local").setAppName("Words Tweeted")
sc = SparkContext(conf = conf)
OUTPUT
Exception                                 Traceback (most recent call last)
<ipython-input-3-39906ef53d10> in <module>()
----> 1 conf = SparkConf().setMaster("local").setAppName("Words Tweeted")
      2 sc = SparkContext(conf = conf)

/Users/jonneff/spark-1.4.0-bin-hadoop2.6/python/pyspark/conf.pyc in __init__(self, loadDefaults, _jvm, _jconf)
    102         else:
    103             from pyspark.context import SparkContext
--> 104             SparkContext._ensure_initialized()
    105             _jvm = _jvm or SparkContext._jvm
    106             self._jconf = _jvm.SparkConf(loadDefaults)

/Users/jonneff/spark-1.4.0-bin-hadoop2.6/python/pyspark/context.pyc in _ensure_initialized(cls, instance, gateway)
    227         with SparkContext._lock:
    228             if not SparkContext._gateway:
--> 229                 SparkContext._gateway = gateway or launch_gateway()
    230                 SparkContext._jvm = SparkContext._gateway.jvm
    231 

/Users/jonneff/spark-1.4.0-bin-hadoop2.6/python/pyspark/java_gateway.pyc in launch_gateway()
     87                 callback_socket.close()
     88         if gateway_port is None:
---> 89             raise Exception("Java gateway process exited before sending the driver its port number")
     90 
     91         # In Windows, ensure the Java child processes do not linger after Python has exited.

Exception: Java gateway process exited before sending the driver its port number

So I’m trying to set up a Pyspark kernel for IPython, a la 

http://thepowerofdata.io/configuring-jupyteripython-notebook-to-work-with-pyspark-1-4-0/

That’s not working either:
jonneff ~ $ ipython console --kernel pyspark
/System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python: No module named IPython
IPython Console 3.2.1

ERROR: Kernel did not respond

Shutting down kernel

I tried updating ipython using conda:

conda update ipython ipython-notebook ipython-qtconsole

Now I get worse error message when I try to star the console with the pyspark kernel.  

onneff ~ $ ipython console --kernel pyspark
Traceback (most recent call last):
  File "/Users/jonneff/anaconda/bin/ipython", line 6, in <module>
    sys.exit(start_ipython())
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/IPython/__init__.py", line 118, in start_ipython
    return launch_new_instance(argv=argv, **kwargs)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 591, in launch_instance
    app.initialize(argv)
  File "<string>", line 2, in initialize
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 75, in catch_config_error
    return method(app, *args, **kwargs)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/IPython/terminal/ipapp.py", line 305, in initialize
    super(TerminalIPythonApp, self).initialize(argv)
  File "<string>", line 2, in initialize
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 75, in catch_config_error
    return method(app, *args, **kwargs)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/IPython/core/application.py", line 386, in initialize
    self.parse_command_line(argv)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/IPython/terminal/ipapp.py", line 300, in parse_command_line
    return super(TerminalIPythonApp, self).parse_command_line(argv)
  File "<string>", line 2, in parse_command_line
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 75, in catch_config_error
    return method(app, *args, **kwargs)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 487, in parse_command_line
    return self.initialize_subcommand(subc, subargv)
  File "<string>", line 2, in initialize_subcommand
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 75, in catch_config_error
    return method(app, *args, **kwargs)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/traitlets/config/application.py", line 418, in initialize_subcommand
    subapp = import_item(subapp)
  File "/Users/jonneff/anaconda/lib/python2.7/site-packages/ipython_genutils/importstring.py", line 31, in import_item
    module = __import__(package, fromlist=[obj])
ImportError: No module named jupyter_console.app
jonneff ~ $

2015.09.14

FIXED IT.  There is a MUCH easier way to start IPython with Spark.  Enter this on the command line in the directory where you have the .ipynb files you want to execute:

IPYTHON_OPTS="notebook" pyspark

That's it!  :)

Getting error message on test helper.  Have to download and install this package:

https://pypi.python.org/pypi/test_helper/0.2

To install test_helper go to Downloads and unzip, then run

python ./setup.py install

To convert a Spark DataFrame to a regular RDD, use the .rdd method:

rdd = df.rdd

Here's what Alyssa had as columns in her Pandas dataframe, and what APPEARS to correspond to in my Spark dataframe:
    
    Alyssa:             Me:             Checked?
    commentAuthor       author          Y
    commentCreated      created_utc
    commentID           id              Y
    commentLink         link_id
    commentScore        score
    postID              N/A
    subreddit           subreddit       Y
    postAuthor  
    postBody            body            Pretty sure
    postCreated
    NegRaw  
    vNegRaw             downs
    vPos                ups
    Pos     
    Neg     
    vNeg    
    posNegRatio     
    posNegDiff  
    commentBody2    
    commentLengthSW

Question for Alyssa:  how did you map from JSON to the MySQL table?  I think I found the answer.  In her Github repo, there is a directory for data collection with IPython notebooks for collecting Reddit posts and comments using praw, the Python Reddit API Wrapper.  There she defines the mapping form comment JSON to her MySQL table:

for comment in flat_allComments:
                c.append({'subreddit': comment.subreddit,
                          'commentID': comment.id,
                          'postID': submission.id,
                          'commentParentID': comment.parent_id,
                          'commentCreated': comment.created,
                          'commentLink': comment.permalink,
                          'commentAuthor': comment.author,
                          'commentScore': comment.score,
                          'commentBody': comment.body})

Talked to Alyssa, who walked me through R code for data cleaning.  For comment time since post, she suggests using first comment time as a proxy for time post was made.  Or I could look at her data and compute average time from post to first comment.  Good idea.

Reddit obfuscates the actual upvotes and downvotes, although they provide a "score" that is the difference that is correct.  From the Reddit wiki:
-------------
How is a submission's score determined?

A submission's score is simply the number of upvotes minus the number of downvotes. If five users like the submission and three users don't it will have a score of 2. Please note that the vote numbers are not "real" numbers, they have been "fuzzed" to prevent spam bots etc. So taking the above example, if five users upvoted the submission, and three users downvote it, the upvote/downvote numbers may say 23 upvotes and 21 downvotes, or 12 upvotes, and 10 downvotes. The points score is correct, but the vote totals are "fuzzed".
-------------

Reddit JSON data dictionary:  https://github.com/reddit/reddit/wiki/JSON

In Spark logistic regression module, input HAS to be a Spark Dataframe.  Interesting.  Not sure if it takes categorical variables.  If it doesn't, I think I can use one-hot encoding a la Spark ML course, lab 4.  So I will have to do OHE for subreddits, of which there will be thousands.  

VERY IMPORTANT PRINCIPLE:  FILTER OUT 94% OF DATA THAT IS NOT EXTREME UPVOTE OR DOWNVOTE FIRST.  That leaves you with a MUCH smaller data set to manage.  

Here is the outline of the order of computation. 

1.  For each post link_id, find minimum created_utc timestamp [can't trust data is ordered by time] and store in key-value pair (pair RDD) {link_id: min_created_utc},  (Plan B:  set up API to get timestamp for all posts in Reddit)
2.  Filter to retain only records that are top or bottom 3% in comment score (upvotes-downvotes) of their subreddit.  Reduces dataset for all subsequent processing.
3.  Filter out exclusions.  Further reduce dataset.
4.  Calculate timeSince based on created_utc and min_created_utc.
5.  Clean comment body, calculate commentLength
6.  Run sentiment analysis, calculate posNegDiff.
7.  Set up OHE for subreddit
8.  May need to deal with sparse matrices from OHE. (Do later if necessary.)
9.  Run linear regression.


Convert Dataframe to plain RDD
For each link_id, find smallest created_utc

How to compute percentiles of large datasets in Spark?  One solution in Scala:

https://eradiating.wordpress.com/2015/02/25/compute-percentile-with-spark/

Fast approximate percentiles using t-digests:

http://apache-spark-user-list.1001560.n3.nabble.com/Percentile-td19978.html

Have to install t digest for Python:

pip install tdigest

Problem with T-digest.  When I do map-reduce and try to have T-digest "eat itself" on the reduce, I get back an object that Spark does not recognize as a T-digest.  I get some other dtype.  Ronak says that sometimes when you do reduce you get a pipeline RDD (whatever that is) and you have to "unwrap" the value to get the object you want.  Ronak showed me an example below, at about lines 57 thorugh 60.

https://github.com/ronaknnathani/gitgraph/blob/master/scripts/batch/2015_events.py

Ronak says I should move code to cluster NOW.  

Public DNSs for my cluster:

jon-master : ec2-52-89-6-161.us-west-2.compute.amazonaws.com
jon-worker1:  ec2-52-89-2-243.us-west-2.compute.amazonaws.com
jon-worker2:  ec2-52-89-6-162.us-west-2.compute.amazonaws.com
jon-worker3:  ec2-52-89-6-148.us-west-2.compute.amazonaws.com

Transferring files when you have passwordless ssh set up using scp:

scp test_helper-0.2.tar.gz ubuntu@master:/home/ubuntu/

Unzip and un-tar file in one step on Linux:  tar xvfz somefilename.tar.gz

