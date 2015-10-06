import re
import time
import praw
import numpy as np
import pandas as pd
import cPickle
from sqlalchemy import create_engine
import math

USERAGENT = '/u/insight_fu posts'
r = praw.Reddit(USERAGENT)

def recentPosts(DATABASE = 'recentPosts'):
    engine = create_engine("mysql+pymysql://root@localhost/" + str(DATABASE))
    con = engine.connect()
    dataid = 1022

    query_recent = con.execute("SELECT * FROM recent")
    
    recentPosts = pd.DataFrame(query_recent.fetchall())
    recentPosts.columns = query_recent.keys()
    
    return recentPosts
        
def rsubmissionID(post, r = r):
    postID = re.sub(".*.comments/", "", post)
    postID = re.sub("/.*.", "", postID)
    submission = r.get_submission(submission_id = postID)
    
    return submission

def rcommentLink(postURL, r = r):
    submission = r.get_submission(url = postURL)
    
    return submission

def rsubreddits(r = r):
    SUBREDDITS = "pics+politics+leagueoflegends+GirlGamers"
    MAXPOSTS = 4
    multi_reddits = r.get_subreddit(SUBREDDITS).get_rising(limit = MAXPOSTS)
    
    subLinks = []
    for post in multi_reddits:
        subLinks.append({'subreddit': post.subreddit,
                        'postTitle': post.title,
                        'postURL': post.permalink})
    
    subLinksPD = pd.DataFrame(subLinks)
    
    return subLinksPD
    
def subreddit(postURL):
     subreddit = re.sub(".*./r/", "", postURL)
     subreddit = re.sub("/.*", "", subreddit)
     
     return subreddit

def comLength(comment):
    return len(comment.split())


def sentimentScore(comment):
    filenameAFINN = 'app/AFINN/AFINN-111.txt'
    afinn = {}
    with open(filenameAFINN, 'r') as f:
        for line in f:
            splitLine = line.strip().split('\t')
            afinn[splitLine[0]] = int(splitLine[1])
    
    commentLength = comLength(comment)

    pattern_split = re.compile(r"\W+")

    words = pattern_split.split(comment.lower())
    score = sum(map(lambda word: afinn.get(word, 0), words))/commentLength
    posNegDiff = score
    
    return posNegDiff

def features(db, subreddit, post, comment, time):

    commentLength = comLength(comment)

    posNegDiff = sentimentScore(comment)
    
    commentTime = int(time)
    test = db[db['postURL'].isin([post])]
    
    if len(test) == 0:
        submission = rsubmissionID(post)
        postTime = int(submission.created_utc)
    elif len(test) > 0:
        postTime = int(float(test.postCreated))
    
    timeSince = round(commentTime - postTime)

    dict = {'GirlGamers': [0, 0, 0],
           'leagueoflegends': [1, 0, 0],
           'pics': [0, 1, 0],
           'politics': [0, 0, 1]}
           
    for key in dict.keys():
        if key == subreddit:
            subredditDC = dict[key]

    features = np.append([commentLength, posNegDiff, timeSince], [subredditDC])

    return features

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def findProb(features):
    f = open('app/weights.csv', 'r')
    weights = np.genfromtxt('app/weights.csv',delimiter=',')
    f.close()

    z = weights.dot(features)
    return sigmoid(z)

def probability(features):
    # f = open('app/model', 'r')
    # model = cPickle.load(f)
    # f.close()

    # probs = model.predict_proba(features)

    prob = findProb(features)

    return "Your chance of being <font color= 'blue'><strong>upvoted: " + str(round(prob*100)) + "%</font></strong>"

def probFeedback(features):
    # f = open('app/model', 'r')
    # model = cPickle.load(f)
    # f.close()
    # probs = model.predict_proba(features)
    prob = findProb(features)

    if prob > .5:
        return "This comment is <font color = 'blue'><strong>likely</font></strong> to be upvoted <font color = 'blue'><strong>(" + str(round(prob)*100) + "%)</font></strong>"
    elif prob < .5:
        return "This comment is <font color = 'red'><strong>unlikely</font></strong> to be upvoted <font color = 'red'><strong>(" + str(round(prob)*100) + "%)</font></strong>" 
    elif prob == .5:
        return "Whoa. It's a toss-up whether this comment will be upvoted or not"
    
def timePresent(timeSec):
    if timeSec/60 >= 60:
        return str(round(timeSec/60/60, 1)) + " hours"
    elif timeSec/60 < 60:
        return str(round(timeSec/60, 1)) + " minutes"

def cLength(commentLength):
    return str(int(commentLength)) + " words"

def sentiment(comment):
    score = sentimentScore(comment)
    
    if score > 0:
        return "<font color= 'blue'><strong>" + str(score) + "</font></strong>"
    elif score < 0:
        return "<font color= 'red'><strong>" + str(score) + "</font></strong>"

def commentSent(comment):
    pattern_split = re.compile(r"\W+")
    words = pattern_split.split(comment.lower())
    
    returnString = ''
    
    for word in words:
        if comLength(word) == 0:
            pass
        elif sentimentScore(word) > 0 :
            returnString+= "<font color= 'blue'><strong> "+word+"</font></strong>"
        elif sentimentScore(word) < 0 :
            returnString+= "<font color= 'red'><strong> "+word+"</font></strong>"
        else: 
            returnString+= " " + word
    return returnString

