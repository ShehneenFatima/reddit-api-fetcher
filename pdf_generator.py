from fpdf import FPDF


def create_pdf(posts):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Loop through posts and add each to the PDF
    for post in posts:
        pdf.cell(200, 10, txt=f"Title: {post['title']}", ln=True)
        pdf.cell(200, 10, txt=f"Score: {post['score']}", ln=True)
        pdf.cell(200, 10, txt=f"URL: {post['url']}", ln=True)
        pdf.cell(200, 10, txt="=" * 80, ln=True)

    # Output the PDF to a file
    pdf.output("Filtered_Posts.pdf")
