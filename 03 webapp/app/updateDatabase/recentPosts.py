import praw
import pandas as pd
import unicodedata
from sqlalchemy import create_engine
from sqlalchemy.types import String

def getRecentPosts():
    USERAGENT = '/u/insight_fu comments'
    SUBREDDITS = ["pics", "politics", "leagueoflegends", "GirlGamers"]
    DATABASE = 'recentPosts'
    MAXPOSTS = 10

    r = praw.Reddit(USERAGENT)

    multi_reddits = []
    for subreddit in SUBREDDITS:
        if subreddit == 'GirlGamers':
            multi_reddits.append(r.get_subreddit(subreddit).get_top_from_day(limit = MAXPOSTS))
        elif subreddit == 'politics':
            multi_reddits.append(r.get_subreddit(subreddit).get_top_from_day(limit = MAXPOSTS))
        else:
            multi_reddits.append(r.get_subreddit(subreddit).get_top_from_hour(limit = MAXPOSTS))
        
    subLinks = []
    for reddit in multi_reddits:
        for post in reddit:
            subLinks.append({'subreddit': post.subreddit,
                            'postTitle': post.title,
                            'postURL': post.permalink,
                            'postCreated': post.created_utc,
                            'postID': post.id})

    subLinksPD = pd.DataFrame(subLinks)

    convertThese = ['postTitle', 'postURL']
    for convert in convertThese:
        subLinksPD[convert] = subLinksPD[convert].map(lambda x:unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'))

    convertThese = ['subreddit', 'postCreated']
    for convert in convertThese:
        subLinksPD[convert] = subLinksPD[convert].map(str)

    engine = create_engine("mysql+pymysql://root@localhost/" + str(DATABASE))
    subLinksPD.to_sql('recent', engine, if_exists="replace")