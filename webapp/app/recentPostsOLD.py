import praw
import pandas as pd
import unicodedata
from sqlalchemy import create_engine
from sqlalchemy.types import String

USERAGENT = '/u/insight_fu comments'
SUBREDDITS = ["pics", "politics", "leagueoflegends", "GirlGamers"]
DATABASE = 'recentPosts'
MAXPOSTS = 10

r = praw.Reddit(USERAGENT)

multi_reddits = []
for subreddit in SUBREDDITS:
    multi_reddits.append(r.get_subreddit(subreddit).get_top_from_day(limit = MAXPOSTS))

for reddit in multi_reddits:
    print reddit

subLinks = []
for reddit in multi_reddits:
    for post in reddit:
        subLinks.append({'subreddit': post.subreddit,
                        'postTitle': post.title,
                        'postURL': post.permalink,
                        'postCreated': post.created_utc})

subLinksPD = pd.DataFrame(subLinks)

convertThese = ['postURL', 'subreddit']
for convert in convertThese:
    subLinksPD[convert] = subLinksPD[convert].map(str)

convertThese = ['postTitle']
for convert in convertThese:
    subLinksPD[convert] = subLinksPD[convert].map(lambda x:unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'))

engine = create_engine("mysql+pymysql://root@localhost/" + str(DATABASE))
subLinksPD.to_sql('recent', engine, if_exists="append")
