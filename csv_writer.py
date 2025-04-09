import csv


def write_to_csv(posts, filename="filtered_posts.csv"):
    """Writes a list of posts to a CSV file."""
    headers = ["Title", "Score", "URL"]  # CSV headers

    # Open the CSV file in write mode, create if doesn't exist
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers

        # Write each post's details to the CSV file
        for post in posts:
            writer.writerow([post["title"], post["score"], post["url"]])

    print(f"Data has been written to {filename}")
