import os

from ocr.pdf_reader import extract_pdf_text
from ocr.docx_reader import extract_docx_text
from ocr.image_reader import extract_image_text


def extract_text(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(filepath)

    elif extension == ".docx":
        return extract_docx_text(filepath)

    elif extension in [".jpg", ".jpeg", ".png"]:
        return extract_image_text(filepath)

    else:
        return "Unsupported File"