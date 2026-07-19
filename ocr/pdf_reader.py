import fitz  # PyMuPDF

def extract_pdf_text(filepath):
    text = ""

    doc = fitz.open(filepath)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text