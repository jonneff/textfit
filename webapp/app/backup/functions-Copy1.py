import re
import time
import praw
import numpy as np
import cPickle

def rsubmissionID(post):
    USERAGENT = '/u/insight_fu posts'
    r = praw.Reddit(USERAGENT)
    postID = re.sub(".*.comments/", "", post)
    postID = re.sub("/.*.", "", postID)
    submission = r.get_submission(submission_id = postID)
    
    return submission

def rcommentLink(postURL):
    USERAGENT = '/u/insight_fu posts'
    r = praw.Reddit(USERAGENT)
    submission = r.get_submission(url = postURL)
    
    return submission

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

def features(subreddit, post, comment, time):

    commentLength = comLength(comment)

    posNegDiff = sentimentScore(comment)
    
    submission = rsubmissionID(post)

    commentTime = time
    postTime = submission.created_utc
    timeSince = round(commentTime - postTime)

    dict = {'GirlGamers': [1, 0, 0, 0],
           'leagueoflegends': [0, 1, 0, 0],
           'pics': [0, 0, 1, 0],
           'politics': [0, 0, 0, 1]}
           
    for key in dict.keys():
        if key == subreddit:
            subredditDC = dict[key]

    features = np.append([subredditDC], [timeSince, commentLength, posNegDiff])

    return features


def probability(features):
    f = open('app/model', 'r')
    model = cPickle.load(f)
    f.close()

    probs = model.predict_proba(features)

    return "Your chance of being <font color= 'blue'><strong>upvoted: " + str(round(probs[0][1], 3)*100) + "%</font></strong>"

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


