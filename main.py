import argparse
import praw
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Function to fetch posts from Reddit
def fetch_posts(subreddit, min_score):
    posts = reddit.subreddit(subreddit).hot(limit=10)
    filtered_posts = filter(lambda post: post.score >= min_score, posts)
    
    return filtered_posts

# Command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch posts from a subreddit.")
    parser.add_argument('--subreddit', type=str, required=True, help="Subreddit name")
    parser.add_argument('--score', type=int, default=5, help="Minimum score for posts")
    return parser.parse_args()

def main():
    args = parse_args()
    
    print(f"Fetching posts from r/{args.subreddit} with a score greater than or equal to {args.score}")
    
    posts = fetch_posts(args.subreddit, args.score)
    
    print(f"\nFiltered Posts with score >= {args.score}:")
    for post in posts:
        print(f"Title: {post.title}")
        print(f"Score: {post.score}")
        print(f"URL: {post.url}")
        print("="*80)

if __name__ == "__main__":
    main()
from csv_writer import write_to_csv  # Import the function from csv_writer.py

# After filtering posts
filtered_posts = [
    {"title": "Ask Anything Monday - Weekly Thread", "score": 5, "url": "https://reddit.com/link1"},
    {"title": "Is pandas considered plaintext?", "score": 6, "url": "https://reddit.com/link2"},
    # Add more posts here...
]

# Call the write_to_csv function
write_to_csv(filtered_posts)
