from ai.groq_ai import ask_llama

def assign_department(text):

    prompt = f"""
Determine which department should handle this document.

Departments:

HR
Finance
Legal
Administration
Technical
Medical

Return ONLY the department name.

Document:
{text}
"""

    return ask_llama(prompt).strip()