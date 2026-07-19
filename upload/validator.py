import os

ALLOWED_EXTENSIONS = [
    "pdf",
    "docx",
    "jpg",
    "jpeg",
    "png"
]

def allowed_file(filename):
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_EXTENSIONS



