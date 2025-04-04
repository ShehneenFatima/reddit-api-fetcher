import os
import praw
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get credentials
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Reddit API connection using PRAW
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

def fetch_posts(subreddit_name, post_limit=10):
    """
    Fetch hot posts from a given subreddit.
    """
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.hot(limit=post_limit)

def filter_posts(posts, min_score=50):
    """
    Generator function to yield posts with score >= min_score
    """
    filtered = filter(lambda post: post.score >= min_score, posts)
    for post in filtered:
        yield post
