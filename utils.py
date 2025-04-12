from fpdf import FPDF

def create_pdf(feedback, output_path="resume_feedback.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in feedback.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(output_path)
