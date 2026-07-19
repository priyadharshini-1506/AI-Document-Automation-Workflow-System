from ai.groq_ai import ask_llama

def generate_summary(text):

    prompt = f"""
You are an AI document summarizer.

Summarize the following document in 5-8 concise bullet points.

Document:
{text}
"""

    return ask_llama(prompt)