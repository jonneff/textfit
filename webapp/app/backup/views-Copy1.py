from flask import render_template, request
from app import app
import functions as fu
import time

@app.route('/')
@app.route('/index')
def input():
    return render_template("index.html")

@app.route("/testInput")
def test_input():
    return render_template("testInput.html")

@app.route("/testOutput")
def test_output():
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
    
    features = fu.features(eg_subreddit, post_URL, eg_comment, commentCreated)

    eg_prob = ''
    eg_prob = fu.probability(features)
    
    eg_score = [comment.score for comment in postAtt.comments][0]
    
    eg_commentForm = fu.commentSent(eg_comment)

    return render_template("testOutput.html", eg_postTitle = eg_postTitle, eg_commentForm = eg_commentForm, eg_score = eg_score, eg_prob = eg_prob, sentiment = sentiment, comLength = comLength, timeDiffCur = timeDiffCur, timeDiffC = timeDiffC, eg_comment = eg_comment, post_URL = post_URL, eg_subreddit = eg_subreddit)

@app.route("/output")
def output():
    post = request.args.get('post')
    comment = request.args.get('comment')

    postAtt = fu.rcommentLink(post)
    postTitle = postAtt.title

    the_subreddit = ''
    the_subreddit = fu.subreddit(post)
    
    the_post = ''
    the_post = post
    
    your_comment = ''
    your_comment = comment

    features = fu.features(the_subreddit, post, comment, time.time())

    timePost = ''
    timePost = fu.timePresent(features[4])

    comLength = ''
    comLength = fu.cLength(features[5])

    sentiment = ''
    sentiment = fu.sentiment(your_comment)

    prob = ''
    prob = fu.probability(features)

    commentForm = fu.commentSent(your_comment)

    return render_template("output.html", postTitle = postTitle, commentForm = commentForm, prob = prob, timePost = timePost, comLength = comLength, sentiment = sentiment, the_subreddit = the_subreddit, the_post = the_post, your_comment = your_comment)


