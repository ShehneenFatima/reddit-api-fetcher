import csv

# Open the CSV file for reading
with open("filtered_posts.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    # Read and print the header (optional)
    header = next(reader)  # Skip the first row (header row)
    print(f"Header: {header}")

    # Read and print each row in the CSV file
    print("Rows:")
    for row in reader:
        print(row)
