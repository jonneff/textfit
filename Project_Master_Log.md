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

——————————

Alyssa had all her data in a MySQL database.  Question:  should I try to put my data into MySQL to get things up and running or not?  I think not, because that is a detour and not necessary.  Instead I should mod her code to pull in features and labels directly from JSON.  I think.  I’m not using MySQL in for scaled solution.  

Copying a file from S3 to wherever:  http://docs.aws.amazon.com/cli/latest/reference/s3/cp.html

Just downloaded smallest Reddit file.  Guess what?  It appears to be uncompressed JSON.  This simplifies things quite a bit, don’t you think?  :)

So all files in Reddit dataset are less than 1 Terabyte, about 908 GB.  


2015.09.14

How to start IPython with Spark.  Enter this on the command line in the directory where you have the .ipynb files you want to execute:

IPYTHON_OPTS="notebook" pyspark

That's it!  :)  The other way (creating and editing ipython_notebook_config.py) took a long time and never worked for me.  I could never get it to create ipython_notebook_config.py.

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

Should probably do comment body before exclusions because some exclusions are based on body.  I've reduced my dataset by 94% with extreme up/down vote so this shouldn't impact performance too much.  

2015.09.16

DEPENDENCY
Downloaded and installed AFINN Python package for sentiment analysis.  
https://github.com/fnielsen/afinn

I CAN read in files sequentially and find min time comment because min time comment is always in the first input file int which the post link_id occurs.  This is because data files are organized by month.  HOWEVER, Ronak says that reading and processing sequentially will be slower than reading everything in at once.  If you run out of memory (which I will), data just spills to disk.  Then during processing, even with the disk IO, Spark will be faster than Hadoop because it uses directed acyclic graph (DAG) to optimize computation.  Also it is still doing some processing in memory.  Ronak has read in 1 TB data and it worked ok.  

I can also do subreddit probability distributions sequentially because I can always add T-digests.  Not sure if this is the right way to go.  

2015.09.17

Struggling with OHE and SparseVector representation in LabeledPoint for input to LogisticRegressionWithSGD.  I have to THINK BACKWARDS.

I want to input into LRWSGD an RDD of LabeledPoints:

(label, SparseVector)

where SparseVector is created from a dense vector:

(posNegDiff, commentLength, timeSince, 0,0,0,...1,0,0...0)

Note there are two parts to this dense vector:  the non-categorical variables and one hot encoding of the categorical variable subreddit. 

The dense vector is created from the simple raw features:

(posNegDiff, commentLength, timeSince, subreddit)

OK I am throwing out the OHE approach and going straight to hash features.  So here are the steps:

* Calculate label from score
* Create rawData:  Put each record into format (label, noncats, raw feature), i.e. 
  (label, (commentLength, posNegDiff, timeSince), subreddit)
* Split into training and test sets:  rawTrainData and rawTestData
* Create hashTrainData = rawTrainData.map(parseHashPoint)

I need to modify parseHashPoint to ignore the non-categorical features and NOT use parsePoint because I have only one categorical feature.  THis is a hack but it makes everything simpler.  If I have more than one non-categorical variable then I will need a parsePoint function.  

THE BIG CHALLENGE SO FAR IS MIXING CATEGORICAL AND NON-CATEGORICAL VARIABLES IN A SINGLE LabeledPoint in a compact sparse representation.  Here is how to do it:

cl = comment length
pn = posNegDiff
ts = timeSince
sr = subreddit (i.e., categorical variable)

I can create a SparseVector out of a list of (index,value) tuples.  My list will always look like

[(0,cl), (1,pn), (2,ts), (srIndex,1)]

where srIndex is the index of the 1 value for the subreddit category from OHE.  

My OHE dict will look like this:

{ (0,'politics'):  0,
(0,'reddit.com'):  1,
(0,'gadgets'):  2,
(0,'gaming'):  0, 
...
}

It will look like this because I have only one categorical feature so the first element of the key tuple is always 0.  

I can't just pull the index out of the value in the dict because it will collide with my non-categorical variables.  So, I shift the value of the OHE dict by 3 for all elements.  Then I can put them together in the smae list as input to SparseVector.

Something like 

OHEdict3 = OHEdict + 3 

for all values.  Then my srIndex is simply:

srIndex = OHEdict3[(0,sr)]

2015.09.18  

Stuff to clean up later:
*  Split data into training, val and test BEFORE creating subreddit digest.  If I use probability distributions from entire dataset then I am cheating in filtering data.  Once I do this, my OHE dict should be ok because I calculate it from the subreddit digest.
*  

Need to port code to cluster and set up git client on master node.

To connect to IPython notebook running on remote AWS server use port forwarding:

ssh -N -f -L localhost:7778:localhost:7777 ubuntu@$public-dns

Change public-dns to your specific master node public dns and make sure ports are correct.  More detail:

ssh -L localport:host:hostport user@ssh_server -N 

where: 
-L - port forwarding parameters (see below) 
localport - local port (chose a port that is not in use by other service) 
host - server that has the port (hostport) that you want to forward 
hostport - remote port 
-N - do not execute a remote command, (you will not have the shell, see below) 
user - user that have ssh access to the ssh server (computer) 
ssh_server - the ssh server that will be used for forwarding/tunneling 

Without the -N option you will have not only the forwardig port but also the remote
 shell. Try with and without it to see the difference.

Need to specify PEM key file in port forwarding or it won't work.  Use this:

ssh -i ~/.ssh/insight-jon.pem -N -f -L localhost:7778:localhost:8888 ubuntu@ec2-52-89-6-161.us-west-2.compute.amazonaws.com

LATER, FOR TUNING SPARK PERFORMANCE:  Brian Cruz (alum) says number of partitions in Spark:  2 per core is a good number.

2015.09.20

Using tmux

Need to install tmux on remote server.  After installing, enter following on remote server:

tmux new -s <session name>

then start your process.  Now you can log out, close window, get timed out and process will keep going.  

To list available sessions, enter following on remote host:

tmux ls

To attach to an existing session:

tmux a -t <target session>

Starting IPython notebook with Spark to use workers by default:

IPYTHON_OPTS="notebook" pyspark --master spark://ip-172-31-47-195:7077 --executor-memory 6400M --driver-memory 6400M

Patrick Zheng discovered that IPython-Spark uses just the master node to execute workbook by default.  Adding these parameters enables you to execute IPython notebook with workers.  

Git problems:

Do "git pull" before making changes on either the local laptop OR the server.  That way you are always up to date.

To access S3 from Spark IPython notebook, need to edit .profile under home directory and add the following:

export AWS_ACCESS_KEY_ID=<your access>
export AWS_SECRET_ACCESS_KEY=<your secret>

I set these env variables and restarted IPython server.  No joy.  Do I have to restart Spark?  Trying that next. Austin got it to work.  Here's what he said:

"Magic! no, basically you had the key's in your ~/.profile, but you never sourced them in your IPython notebook server terminal. I just stopped the IPython notebook server, sourced the ~/.profile and voila!"

"Process locality:  The values of environment variables are local, which means they are specific to the running process in or for which they were set. This means that if we open two terminal windows (which means we have two separate bash processes running), and change a value of an environment variable in one of the windows, that change will not be seen by the shell in the other window or any other program currently on the desktop." https://help.ubuntu.com/community/EnvironmentVariables

Have to install afinn, tdigest etc. on worker nodes or you get this error:

ImportError: No module named tdigest.tdigest

It takes ~20 minutes to create subredditDigest on an 85 MB input file EVEN ON THE CLUSTER.  Not good.  But how much of this is Spark overhead?

2015.09.22

Implementing accuracy checking.  My performance is HORRIBLE.  Baseline is just giving predictions according to average percentage on training set, which is close to 50%.  
OHE Features Train Logloss:
  Baseline = 0.693
  LogReg = 9.839

Here are my weights and intercept:

[-0.10322076674490815, -0.038175769180245248, -0.033515425808193736, -0.031231564685160879, -0.027168234465817155, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.010858031673728294, 0.043883835637280835, 0.052609844995172315, 0.74844587378001814, 0.76979891768686493, 1.8964562127415054, 6.4059693462854845, 13.564270390032908, 822.29158792336955, 6050.4316845170852] 10.6945827861

Some of these weights are enormous.  I am tempted to jack up the regularization parameter because that would decrease size of weights.  But that's not my problem.  If anything the big weights should be overfitting.  Unfortunately I did just a really lousy job of fitting the data.  OR NOT.  I think maybe I need to alter code that calculates the probability of an observation, i.e., getP().

A log loss of ~25.3 for a specific point means that we completely got it wrong.  If label was 1, we predicted 0 or vice versa.  0.99 and 0 would give a log loss of ~4.6.  My mean log loss over all data points is 9.8, indicating my model is wrong almost all of the time.  In fact, this is suspcious.  It seems to indicate that the model would be accurate if I REVERSED the prediction.  Odd.  

So I printed training predictions and it appears that my model is predicting 0.999999999999999 for every point.  *sigh*  I am using linear regression with stochastic gradient descent.  

Talked to Ronak.  I'm going to throw out log loss evaluation because it's not a good fit for my problem. Log loss is useful for rare events, like clickthrough on ads.  Voting something up or down is not rare.  Instead I will work with ROC plots, AUC, % of labels that were correct, etc.  

Have to set environment variables for matplotlib because what I have is not working correctly.  

BASICALLY ALL MY PREDICTIONS ARE THE SAME NUMBER:  0.9999999979388463.  If I run LRWSGD with mostly default inputs I get the same thing.

Interesting note about my data:

for key in srDigestR.keys():
    print key, df.filter(df['subreddit'] == key).count()

eo 1
arxiv 4
zh 3
features 19
programming 16162
it 31
sv 1
gadgets 314
nsfw 287
politics 34088
id 20
es 1
ru 17
netsec 43
ads 50
entertainment 819
tr 41
sports 300
freeculture 5
gaming 572
fr 5
business 526
reddit.com 88601
de 15
lipstick.com 1
ja 33
science 8326
joel 24
no 1
request 11
bugs 104
sl 4

And this is BEFORE I filter down to 6% of data set.  Maybe the lack of data for most of the subreddits is throwing log reg model off.Maybe I don't have enough data for stochastic gradient descent.

Patrick Zheng and Ryan Walker suggest changing my input data so that I have only four categories:
Programming
Politics
Reddit.com
Other

Since I have only a few categories for my categorical variable, I need to "leave out" one of them from encoding to avoid numerical instability.  So the encoding will be

programming [1 0 0]
politics [0 1 0]
reddit.com [0 0 1]
Other [0 0 0]

In the long run I need to automatically filter out subreddits that just don't have enough data.  What's the right threshold?  I won't know until I read in all the data.....

The result of reducing number of categories was:  I get same result, predicted values all = 1.  Played with hyperparameters and get same result.  Ronak suggests reading in data roughly corresponding to Alyssa's input data from S3 and seeing what result I get.  To do this, I need to read several input files from S3, filter out to just the subreddits she used, and run logistic regression on them.  

I also need to beef up my cluster ot handle 1 TB of data.  Ronak suggests 6 nodes, each with 1 TB of disk.  Turn off Hadoop since I'm not using it.  

2015.09.23

Spark Master web page port 8080:  it is telling me some of my m4.large instances have six cores.  They only have 2.  Ronak thinks this is a bug in Spark.  

Raw data files appear to have 1 JSON object per line.  Good.  At least that's what the first 85 MB file has.

Time for a single 10 GB input file:
* read in data file:  7 min
* create subreddit digest:  28 min
* filter down to top/bottom 3% and split into train, val and test:  

OK so I have been recording times in an Excel spreadsheet.  So far so good.  I removed some .take() and .count() to improve performance.  I think there is something I am not cacheing because it looks like it is having to go back and re-calculate some things.  

GOOD NEWS:  with 10 GB file, I am no longer getting all 1's.  BAD NEWS:  I only have 47% prediction accuracy.  Why?  Perhaps it is because I am creating specific OHE variables for politics, reddit.com, and programming and every other point is "other".  Not very accurate probably with all other subreddits going this way.

IDEA:  At beginning, filter my data to only Alyssa's subreddits:  

leagueoflegends
GirlGamers
pics
politics

FURTHERMORE, use as input data roughly the time frame she collected from, or nearby.  That should give me comparable results. 

You can use the  .cancelAllJobs() method in Spark Context to cancel things that are running too long.

LOTS of performance issues.  Two bottlenecks are reading data and creating subreddit digest.  GAME PLAN:

1.  Tell Spark about new disk space so it is availble.  Create the following directories and add the following to spark-env.sh:

export SPARK_LOCAL_DIRS=/mnt/my-data/spark_local_dir
export SPARK_WORKER_DIR=/mnt/my-data/spark_worker_dir

2.  Replace .cache() with .persist(StorageLevel.MEMORY_AND_DISK_SER)
If there is not enough room in memory, sometimes Spark has to go back and read from S3 to recreate data.  According to Austin.

3.  Refactor subreddit digest code to use .mapPartition()  Austin agrees should run faster bc it has some paralellism.

4.  Specify schema on json read.  The way I'm doing it now, Spark reads entire file TWICE:  once to make SURE it has the right schema, then it actually reads in the data.  See Austin's code.

5.  Run tests on subset of data for read and create subreddit schema.  See what the performance increase is.  

If that's not enough, take some EXTREME MEASURES:
*  Add three more nodes
*  Run Spark on PyPy:  PYSPARK_PYTHON=pypy ./bin/spark-submit wordcount.py

















