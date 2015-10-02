from flask import render_template, request
from app import app
import functions as fu
import functions2 as fu2
import time

@app.route('/')
@app.route('/index')
def input():
    
    recentPosts = fu.recentPosts()
    
    Pic = recentPosts[recentPosts['subreddit'] == 'pics']
    Pol = recentPosts[recentPosts['subreddit'] == 'politics']
    LoL = recentPosts[recentPosts['subreddit'] == 'leagueoflegends']
    GG = recentPosts[recentPosts['subreddit'] == 'GirlGamers']
    
    return render_template("index.html", Pic = Pic, Pol = Pol, LoL = LoL, GG = GG)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/egOutput")
def eg_output():
    post_URL = request.args.get('postURL')

    eg_subreddit = fu.subreddit(post_URL)

    postAtt = fu.rcommentLink(post_URL)
   
    eg_postTitle = postAtt.title
    
    eg_comment = [comment.body for comment in postAtt.comments][0]
    
    commentCreated = int([comment.created_utc for comment in postAtt.comments][0])
    postCreated = postAtt.created_utc
    
    timeDiffC = fu.timePresent(round(commentCreated - postCreated))
    timeDiffCur = fu.timePresent(round(time.time() - commentCreated))
    
    comLength = fu.cLength(fu.comLength(eg_comment))

    sentiment = ''
    sentiment = fu.sentiment(eg_comment)
    
    recentPosts = fu.recentPosts()

    features = fu.features(recentPosts, eg_subreddit, post_URL, eg_comment, commentCreated)

    eg_prob = ''
    eg_prob = fu.probability(features)
    
    eg_result = ''
    eg_result = fu.probFeedback(features)
    
    eg_score = [comment.score for comment in postAtt.comments][0]
    if eg_score < 1:
        eg_score = "<font color= 'red'>" + str(eg_score) + "</font>"
    elif eg_score > 1:
        eg_score = "<font color= 'blue'>" + str(eg_score) + "</font>"
    
    eg_commentForm = fu2.get_commentSent(eg_comment)

    subLinks = fu.rsubreddits()

    sentiment = fu2.get_sentimentScores(eg_comment)
    posSent = sentiment[0]
    negSent = sentiment[1]

    return render_template("egOutput.html", eg_postTitle = eg_postTitle, eg_commentForm = eg_commentForm, eg_score = eg_score, eg_prob = eg_prob, sentiment = sentiment, comLength = comLength, timeDiffCur = timeDiffCur, timeDiffC = timeDiffC, eg_comment = eg_comment, post_URL = post_URL, eg_subreddit = eg_subreddit, subLinks = subLinks, eg_result = eg_result, posSent = posSent, negSent = negSent)

@app.route("/output")
def output():
    recentPosts = fu.recentPosts()

    post = request.args.get('post')
    comment = request.args.get('comment')

    postAtt = fu.rcommentLink(post)
    postTitle = postAtt.title
    post_URL = postAtt.permalink

    the_subreddit = ''
    the_subreddit = fu.subreddit(post)
    
    the_post = ''
    the_post = post
    
    your_comment = ''
    your_comment = comment

    features = fu.features(recentPosts, the_subreddit, post, comment, time.time())

    timePost = ''
    timePost = fu.timePresent(features[4])

    comLength = ''
    comLength = fu.cLength(features[5])

    sentiment = ''
    sentiment = fu.sentiment(your_comment)

    prob = ''
    prob = fu.probability(features)
    
    the_result = ''
    the_result = fu.probFeedback(features)

    commentForm = fu.commentSent(your_comment)
    
    subLinks = fu.rsubreddits()


    return render_template("output.html", postTitle = postTitle, commentForm = commentForm, prob = prob, timePost = timePost, comLength = comLength, sentiment = sentiment, the_subreddit = the_subreddit, the_post = the_post, your_comment = your_comment, subLinks = subLinks, the_result = the_result, post_URL = post_URL)

@app.route("/output2")
def output2():
    
    the_post = request.args.get('post')
    your_comment = request.args.get('comment')
    
    postInfo = fu2.get_postInfo(the_post)
    
    sentiment = fu2.get_sentimentScores(your_comment)
    posSent = sentiment[0]
    negSent = sentiment[1]
    
    timePost = fu2.get_recency(postInfo)
    recency = fu2.get_timeUnits(timePost)
    
    comLength = fu2.get_commentLength(your_comment)
    
    the_subreddit = fu2.get_subreddit(the_post)
    
    postTitle = postInfo['postTitle'].iloc[0]
    
    commentForm = fu2.get_commentSent(your_comment)
    
    the_result = fu2.get_result(postInfo, your_comment)
    
    return render_template("output2.html", your_comment = your_comment, the_post = the_post, the_result = the_result, posSent = posSent, negSent = negSent, recency = recency, comLength = comLength, the_subreddit = the_subreddit, postTitle = postTitle, commentForm = commentForm)
