from fpdf import FPDF
import os
from datetime import datetime
 
 
REPORT_FOLDER = "generated_reports"
 
os.makedirs(REPORT_FOLDER, exist_ok=True)
 
 
def safe_text(text):
    """
    The built-in 'Arial' PDF font only supports Latin-1.
    AI-generated text (summaries, metadata, etc.) often contains
    characters like bullet points (•), smart quotes, or em-dashes
    that aren't in Latin-1 and would otherwise crash FPDF.
    This replaces any unsupported character instead of crashing.
    """
 
    if text is None:
        return ""
 
    return str(text).encode("latin-1", "replace").decode("latin-1")
 
 
def generate_pdf_report(
    username,
    filename,
    category,
    summary,
    metadata,
    priority,
    department,
    workflow,
    reminder
):
 
    pdf = FPDF()
 
    pdf.set_auto_page_break(auto=True, margin=15)
 
    pdf.add_page()
 
 
    # ==========================
    # TITLE
    # ==========================
 
    pdf.set_font("Arial", "B", 18)
 
    pdf.cell(
        0,
        10,
        "AI Document Automation Report",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C"
    )
 
    pdf.ln(8)
 
 
    # ==========================
    # USER DETAILS
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "User Information", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.cell(
        0,
        8,
        safe_text(f"Username : {username}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.cell(
        0,
        8,
        safe_text(f"Document : {filename}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.cell(
        0,
        8,
        safe_text(f"Generated : {datetime.now()}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # DOCUMENT DETAILS
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "Document Details", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.multi_cell(
        0,
        8,
        safe_text(f"Category : {category}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.multi_cell(
        0,
        8,
        safe_text(f"Priority : {priority}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.multi_cell(
        0,
        8,
        safe_text(f"Department : {department}"),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # SUMMARY
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "AI Summary", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.multi_cell(
        0,
        8,
        safe_text(summary),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # METADATA
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "Metadata", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.multi_cell(
        0,
        8,
        safe_text(metadata),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # WORKFLOW
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "Workflow Recommendation", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.multi_cell(
        0,
        8,
        safe_text(workflow),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # REMINDER
    # ==========================
 
    pdf.set_font("Arial", "B", 13)
 
    pdf.cell(0, 8, "Reminder", new_x="LMARGIN", new_y="NEXT")
 
    pdf.set_font("Arial", "", 12)
 
    pdf.multi_cell(
        0,
        8,
        safe_text(reminder),
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
    pdf.ln(5)
 
 
    # ==========================
    # FOOTER
    # ==========================
 
    pdf.set_font("Arial", "I", 10)
 
    pdf.multi_cell(
        0,
        8,
        "Generated automatically by AI-Powered Intelligent Document Automation and Workflow Management System.",
        new_x="LMARGIN",
        new_y="NEXT"
    )
 
 
    report_name = f"{filename}_report.pdf"
 
    report_path = os.path.join(
        REPORT_FOLDER,
        report_name
    )
 
    pdf.output(report_path)
 
    return report_path