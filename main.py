import praw
import argparse
import csv
import os
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()

# Fetch Reddit API credentials from environment variables
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')

# Define upper limits for score and limit
MAX_SCORE = 1000000  # Adjust as needed
MAX_LIMIT = 100  # Adjust as needed

# Function to fetch posts based on subreddit, score, type, and limit
def fetch_posts(subreddit, score, post_type, limit):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    subreddit = reddit.subreddit(subreddit)

    # Fetch posts based on type
    if post_type == 'hot':
        posts = subreddit.hot(limit=limit)
    elif post_type == 'new':
        posts = subreddit.new(limit=limit)
    elif post_type == 'top':
        posts = subreddit.top(limit=limit)
    elif post_type == 'rising':
        posts = subreddit.rising(limit=limit)
    else:
        raise ValueError("Invalid post type")

    filtered_posts = []
    for post in posts:
        # Filter posts based on score less than or equal to the given score
        if post.score <= score:
            filtered_posts.append({
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': str(post.author),
                'num_comments': post.num_comments,
                'created_utc': post.created_utc
            })
    
    return filtered_posts

# Function to save the posts in CSV format
def save_to_csv(posts, path):
    csv_file = os.path.join(path, "filtered_posts.csv")
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'score', 'url', 'author', 'num_comments', 'created_utc'])
        writer.writeheader()
        for post in posts:
            writer.writerow(post)

# Function to generate a PDF report from the posts
def generate_pdf(posts, path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Filtered Reddit Posts", ln=True, align='C')

    # Add posts
    pdf.set_font('Arial', '', 12)
    for post in posts:
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Title: {post['title']}", ln=True)
        pdf.cell(200, 10, txt=f"Score: {post['score']}", ln=True)
        pdf.cell(200, 10, txt=f"Author: {post['author']}", ln=True)
        pdf.cell(200, 10, txt=f"Number of Comments: {post['num_comments']}", ln=True)
        pdf.cell(200, 10, txt=f"URL: {post['url']}", ln=True)
        pdf.cell(200, 10, txt=f"Created UTC: {post['created_utc']}", ln=True)
        pdf.ln(5)

    pdf_output_path = os.path.join(path, "Filtered_Posts.pdf")
    pdf.output(pdf_output_path)
    print(f"PDF report has been created successfully at {pdf_output_path}!")

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Reddit posts")
    parser.add_argument('--subreddit', type=str, required=True, help="Subreddit to fetch posts from")
    parser.add_argument('--score', type=int, required=True, help="Maximum score of the posts")
    parser.add_argument('--limit', type=int, required=True, help="Number of posts to fetch")
    parser.add_argument('--type', type=str, choices=['hot', 'new', 'top', 'rising'], default='hot', help="Type of posts to fetch")
    parser.add_argument('--path', type=str, required=True, help="Path to store the files (CSV, PDF)")

    args = parser.parse_args()

    # Validate score and limit to ensure positive values and within upper limits
    if args.score < 0 or args.score > MAX_SCORE:
        raise ValueError(f"Score must be a non-negative integer and less than or equal to {MAX_SCORE}")
    if args.limit <= 0 or args.limit > MAX_LIMIT:
        raise ValueError(f"Limit must be a positive integer and less than or equal to {MAX_LIMIT}")

    # Validate if the path exists
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"The specified path {args.path} does not exist.")
    
    return args

# Main function
def main():
    args = parse_args()
    
    # Fetch posts
    print(f"Fetching posts from r/{args.subreddit} with a score less than or equal to {args.score}")
    posts = fetch_posts(args.subreddit, args.score, args.type, args.limit)
    
    # Check if any posts are found
    if not posts:
        print("No posts found with the given criteria.")
        return

    # Save the posts to CSV
    save_to_csv(posts, args.path)
    print(f"Data has been written to {args.path}/filtered_posts.csv")

    # Generate PDF report
    generate_pdf(posts, args.path)

# Entry point for the script
if __name__ == "__main__":
    main()
