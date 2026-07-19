from ai.groq_ai import ask_llama

def extract_metadata(text):

    prompt = f"""
Extract the following metadata from the document.

Return in this format:

Title:
Author:
Date:
Keywords:
Document Type:

If any information is not available, return "Not Found".

Document:
{text}
"""

    return ask_llama(prompt)