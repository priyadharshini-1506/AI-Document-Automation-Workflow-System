from ai.groq_ai import ask_llama

def detect_priority(text):

    prompt = f"""
Determine the priority of this document.

Return ONLY ONE of:

High
Medium
Low

Rules:
High = urgent/legal/payment/deadline
Medium = internal reports/approvals
Low = general information

Document:
{text}
"""

    return ask_llama(prompt).strip()