from reddit_generator import fetch_posts, filter_posts

# Fetch top 5 posts from the 'python' subreddit
posts = fetch_posts("python", post_limit=5)

# Filter posts with a minimum score of 10
filtered_posts = filter_posts(posts, min_score=10)

# Print each post's title and score
for post in filtered_posts:
    print(f"{post.title} - Score: {post.score}")
