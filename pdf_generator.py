from fpdf import FPDF
import csv

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title
pdf.set_font("Arial", 'B', 12)
pdf.cell(200, 10, txt="Filtered Reddit Posts", ln=True, align='C')

# Set font for content
pdf.set_font("Arial", size=10)

# Open the CSV file and read the rows
with open('filtered_posts.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        title, score, url = row
        # Write each post in the PDF
        pdf.multi_cell(0, 10, f"Title: {title}")
        pdf.multi_cell(0, 10, f"Score: {score}")
        pdf.multi_cell(0, 10, f"URL: {url}")
        pdf.multi_cell(0, 10, "================================================================================")

# Output PDF
pdf.output("Filtered_Posts.pdf")
print("PDF created successfully!")
