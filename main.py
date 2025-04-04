import argparse
import praw
from dotenv import load_dotenv
import os
from csv_writer import write_to_csv  # Import the function to write to CSV
from pdf_generator import create_pdf  # Import the function to create the PDF

# Load environment variables
load_dotenv()

# Initialize the Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Function to fetch posts from Reddit
def fetch_posts(subreddit, min_score, limit):
    posts = reddit.subreddit(subreddit).hot(limit=limit)
    filtered_posts = filter(lambda post: post.score >= min_score, posts)
    
    # Return as a list of dictionaries
    return [{"title": post.title, "score": post.score, "url": post.url} for post in filtered_posts]

# Command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch posts from a subreddit.")
    parser.add_argument('--subreddit', type=str, required=True, help="Subreddit name")
    parser.add_argument('--score', type=int, default=5, help="Minimum score for posts")
    parser.add_argument('--limit', type=int, default=10, help="Number of posts to fetch")
    return parser.parse_args()

def main():
    args = parse_args()

    # Fetch filtered posts dynamically
    print(f"Fetching posts from r/{args.subreddit} with a score greater than or equal to {args.score}")
    posts = fetch_posts(args.subreddit, args.score, args.limit)
    
    # Display the filtered posts
    print(f"\nFiltered Posts with score >= {args.score}:")
    for post in posts:
        print(f"Title: {post['title']}")
        print(f"Score: {post['score']}")
        print(f"URL: {post['url']}")
        print("="*80)

    # Write the filtered posts to CSV
    write_to_csv(posts)
    print("Data has been written to filtered_posts.csv")

    # Create a PDF report for the filtered posts
    create_pdf(posts)
    print("PDF report has been created successfully!")

if __name__ == "__main__":
    main()
