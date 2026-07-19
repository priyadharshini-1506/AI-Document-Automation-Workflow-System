from ai.groq_ai import ask_llama

def classify_document(text):

    prompt = f"""
Classify the following document into ONLY ONE category.

Categories:
- HR
- Finance
- Legal
- Medical
- Administration
- Technical
- Education
- Other

Return ONLY the category name.

Document:
{text}
"""

    return ask_llama(prompt).strip()