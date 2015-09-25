from sqlalchemy import create_engine
import re
from math import exp
import pandas as pd
import time
import unicodedata
import praw

def get_postID(post):
    postID = re.sub(".*.comments/", "", post)
    postID = re.sub("/.*.", "", postID)

    return postID

def get_subreddit(post):
    subreddit = re.sub(".*./r/", "", post)
    subreddit = re.sub("/.*", "", subreddit)
     
    return subreddit

def get_recentPosts(DATABASE = 'recentPosts'):
    engine = create_engine("mysql+pymysql://root@localhost/" + str(DATABASE))
    con = engine.connect()
    dataid = 1022

    query_recent = con.execute("SELECT * FROM recent")
    
    recentPosts = pd.DataFrame(query_recent.fetchall())
    recentPosts.columns = query_recent.keys()
    
    return recentPosts

def get_postFromReddit(post):
    postID = get_postID(post)
    subreddit = get_subreddit(post)
    
    USERAGENT = '/u/insight_fu posts'
    r = praw.Reddit(USERAGENT)
    
    submission = r.get_submission(submission_id = postID)
    
    postInfo = []
    postInfo.append({'subreddit': subreddit,
                    'postID': postID,
                    'postCreated': submission.created_utc,
                    'postTitle': submission.title,
                    'postLink': submission.permalink})
    
    postInfoDF = pd.DataFrame(postInfo)
    
    return postInfoDF

def get_postInfo(post):
    postID = get_postID(post)
    
    recentPosts = get_recentPosts()
    postInfo = recentPosts[recentPosts['postID'] == postID]

    if len(postInfo) != 1:
        postInfo = get_postFromReddit(post)
    
    return postInfo
    
def get_recency(postInfo):
    postCreated = postInfo['postCreated'].iloc[0]
    postCreated = int(float(postCreated))
    
    commentCreated = int(float(time.time()))

    return commentCreated - postCreated

def AFINN():
    filenameAFINN = 'app/AFINN/AFINN-111.txt'
    afinn = {}
    with open(filenameAFINN, 'r') as f:
        for line in f:
            splitLine = line.strip().split('\t')
            afinn[splitLine[0]] = int(splitLine[1])
    
    return afinn

def clean_Comment(comment):
    words = re.sub(r"[']", '', comment)
    words = words.lower()
    
    pattern_split = re.compile(r"\W+")
    words = pattern_split.split(words)
    
    return words

def get_sentimentScores(comment):
    afinn = AFINN()
    words = clean_Comment(comment)

    scores = map(lambda word:afinn.get(word, 0), words)
    
    posScore = sum(score for score in scores if score > 0)
    negScore = sum(score for score in scores if score < 0)
        
    sentimentScores = (posScore, negScore)

    return sentimentScores

def get_commentSent(comment):
    words = clean_Comment(comment)
    
    returnString = ''
    
    for word in words:
        if get_commentLength(word) == 0:
            pass
        elif get_sentimentScores(word)[0] > 0:
            returnString += "<font color= 'blue'><strong> " + word + "</font></strong>"
        elif get_sentimentScores(word)[1] < 0:
            returnString += "<font color= 'red'><strong> " + word + "</font></strong>"
        else:
            returnString += " " + word
        
    return returnString

def get_commentLength(comment):
    return(len(clean_Comment(comment)))

def get_CSProbability(postInfo, comment):
    subreddit = postInfo['subreddit'].iloc[0]

    subLoL = 0
    subPics = 0
    subPol = 0
    
    if subreddit == 'leagueoflegends':
        subLoL = 1
    elif subreddit == 'pics':
        subPics = 1
    elif subreddit == 'politics':
        subPol = 1
        
    recency = get_recency(postInfo)
    recencyMin = recency/60
    
    commentLength = get_commentLength(comment)
    
    sentScore = get_sentimentScores(comment)
    posScore = sentScore[0]
    negScore = sentScore[1]
    
    commentLevel2 = 1
    
    intercept = 2.261e+00
    
    pred = intercept + \
    (-8.074e-01)*subLoL + \
    (-6.528e-01)*subPics + \
    (-6.755e-01)*subPol + \
    (-3.464e-03)*recencyMin + \
    (4.119e-03)*commentLength + \
    (-1.953e-02)*posScore + \
    (4.334e-02)*negScore + \
    (-2.685e-01)*commentLevel2
    
    probability = exp(pred)/(1 + exp(pred))
    
    return probability

def get_result(post, comment):
    probs = get_CSProbability(post, comment)
    
    if probs > .5:
        return "This comment is <font color = 'blue'><strong>likely</font></strong> to be upvoted <font color = 'blue'><strong>(" + str(round(probs, 3)*100) + "%)</font></strong>"
    elif probs < .5:
        return "This comment is <font color = 'red'><strong>unlikely</font></strong> to be upvoted <font color = 'red'><strong>(" + str(round(probs, 3)*100) + "%)</font></strong>" 
    elif probs == .5:
        return "Whoa. It's a toss-up whether this comment will be upvoted or not"

def get_timeUnits(timePost):
    if timePost/60 >= 60:
        return str(round(timePost/60/60, 1)) + " hours"
    elif timePost/60 < 60:
        return str(round(timePost/60, 1)) + " minutes"
