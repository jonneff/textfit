# Introduction to textfitXL
============

Table of Contents:

1. [Introduction](README.md#1-introduction)
2. [Algorithm, Features, Scaling and Filtering](README.md#2-algo)
3. [Data and Pipeline](README.md#3-pipeline) 
4. [Cluster and Cost](README.md#4-cluster)
5. [Accuracy and Runtime](README.md#5-accuracy)
6. [Engineering Challenges](README.md#6-challenges)
7. [Installation Instructions](README.md#7-install)

## 1. Introduction

In July 2015, an Insight fellow named Alyssa Fu trained a logistic regression model in R to predict whether a comment would be voted up or down on Reddit.  Her training data was extracted from about 500,000 comments she downloaded through the Reddit API for April and May 2015.  The name of her project was [textfit.](https://github.com/alyssafu/Insight-Project).  

The goal of textfitXL is to scale up Alyssa's project to handle 1.6 billion comments (908 GB) comprising eight years of Reddit data from 2007 to 2015.  Note that no attempt was made to alter or improve her original approach.  The source data was obtained by Jason Baumgartner and placed in 92 files in an Amazon S3 bucket.  

textfitXL is implemented in Apache Spark using the Python API and a Jupyter (Ipython) notebook running on an AWS cluster.  The repository also includes a [simple web app](http://www.textfitxl.com/) that allows a user to select a Reddit post, type in a sample comment, and get a prediction of whether the comment will be voted up or down.  The web app re-uses much of Alyssa's code, with her permission.  

## 2. Algorithm, Features, Scaling and Filtering

The figure below shows the basic approach used in textfitXL.  

![alt text](img/algo.jpg "Algorithm, Features and Scaling")

Regularized logistic regression is used to classify comments as either upvoted (1) or downvoted (0).  As in Alyssa's project, four features were used:  time since post, comment length, sentiment, and subreddit.  Subreddit is a categorical variable with four categories:  GirlGamers, leagueoflegends, pics, and politics.  (While Reddit has many thousands of subreddits, Alyssa chose four for her model.)  Sentiment analysis is done using the [AFINN](https://github.com/fnielsen/afinn) model, which is essentially a table lookup based on movie reviews.  Per the request of the author, listed below is the reference for the paper describing AFINN:

Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs" , Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)

Scalability is achieved by using Spark for parallel processing.  The features are placed in a SparseVector format, which reduces memory and processing time during execution.  Finally, stochastic gradient descent is used to reduce time to calculate gradients, which can be a compute-intensive process.  

The initial 908 GB dataset is filtered down to less than 55 MB by choosing only comments that are in the top or bottom 3% of votes.  Logistic regression models have difficulty learning from data points that are not "extreme" values.  

![alt text](img/filter.jpg "Filter to Top/Bottom 3%")


## 3. Data and Pipeline

![alt text](img/pipeline.jpg "Data and Pipeline")

## 4. Cluster and Cost

![alt text](img/cost.jpg "Cluster and Cost")

## 5. Accuracy and Runtime

## 6.  Engineering Challenges

![alt text](img/mixed.jpg "Mixed Numerical and Categorical Variables")

![alt text](img/shuffle.jpg "Join is Long and Brittle Due to Shuffling")

![alt text](img/repartition.jpg "Repartitioning Improves Performance")

## 7.  Installation Instructions

See the [install directions](INSTALL.md) for installation instructions
