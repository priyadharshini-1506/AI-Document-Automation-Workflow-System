from ai.groq_ai import ask_llama


def chatbot(document_text, question):

    prompt = f"""
You are an AI assistant.

Answer ONLY from the uploaded document.

Document:
{document_text}

Question:
{question}

If the answer is not found in the document, say:
"I couldn't find that information in the uploaded document."
""" 

    return ask_llama(prompt)

