from docx import Document

def extract_docx_text(filepath):

    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text