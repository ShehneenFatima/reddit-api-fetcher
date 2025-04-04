import praw
import argparse
import os
import csv
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Function to validate arguments
def validate_positive_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

def fetch_posts(subreddit_name, score_threshold, post_type, limit):
    # Create Reddit instance
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT)
    
    # Fetch posts based on the post type (hot, new, top, rising)
    if post_type == "hot":
        posts = reddit.subreddit(subreddit_name).hot(limit=limit)
    elif post_type == "new":
        posts = reddit.subreddit(subreddit_name).new(limit=limit)
    elif post_type == "top":
        posts = reddit.subreddit(subreddit_name).top(limit=limit)
    elif post_type == "rising":
        posts = reddit.subreddit(subreddit_name).rising(limit=limit)
    else:
        raise ValueError(f"Unknown post type: {post_type}")
    
    filtered_posts = []
    for post in posts:
        if post.score >= score_threshold:
            filtered_posts.append({
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "author": str(post.author),
                "created": post.created_utc,
                "num_comments": post.num_comments,
                "flair": post.link_flair_text or "No flair"
            })
    
    return filtered_posts

def save_to_csv(posts, path):
    # Save the filtered posts to a CSV file
    with open(os.path.join(path, "filtered_posts.csv"), mode='w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "score", "url", "author", "created", "num_comments", "flair"])
        writer.writeheader()
        for post in posts:
            writer.writerow(post)

def generate_pdf(posts, path):
    # Create a PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title and header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Filtered Reddit Posts", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    # Loop through posts and add to PDF
    for post in posts:
        pdf.cell(200, 10, txt=f"Title: {post['title']}", ln=True)
        pdf.cell(200, 10, txt=f"Score: {post['score']}", ln=True)
        pdf.cell(200, 10, txt=f"URL: {post['url']}", ln=True)
        pdf.cell(200, 10, txt=f"Author: {post['author']}", ln=True)
        pdf.cell(200, 10, txt=f"Created: {post['created']}", ln=True)
        pdf.cell(200, 10, txt=f"Comments: {post['num_comments']}", ln=True)
        pdf.cell(200, 10, txt=f"Flair: {post['flair']}", ln=True)
        pdf.ln(10)

    # Output PDF to file
    pdf.output(os.path.join(path, "Filtered_Posts.pdf"))

def main():
    parser = argparse.ArgumentParser(description="Fetch and filter Reddit posts based on score and other parameters.")
    parser.add_argument('--subreddit', type=str, required=True, help='Subreddit to fetch posts from')
    parser.add_argument('--score', type=validate_positive_int, required=True, help='Minimum score of the posts')
    parser.add_argument('--limit', type=validate_positive_int, required=True, help='Limit the number of posts to fetch')
    parser.add_argument('--type', type=str, choices=["hot", "new", "top", "rising"], default="hot", help="Post type to fetch")
    parser.add_argument('--path', type=str, required=True, help="Path where CSV and PDF files should be saved")

    args = parser.parse_args()

    # Fetch posts
    posts = fetch_posts(args.subreddit, args.score, args.type, args.limit)

    if posts:
        print(f"Filtered {len(posts)} posts with score >= {args.score}:")
        for post in posts:
            print(f"Title: {post['title']} | Score: {post['score']} | URL: {post['url']}")

        # Save to CSV and generate PDF
        save_to_csv(posts, args.path)
        generate_pdf(posts, args.path)

        print(f"Data has been written to {args.path}/filtered_posts.csv")
        print(f"PDF report has been created at {args.path}/Filtered_Posts.pdf")
    else:
        print(f"No posts found with score >= {args.score}.")

if __name__ == "__main__":
