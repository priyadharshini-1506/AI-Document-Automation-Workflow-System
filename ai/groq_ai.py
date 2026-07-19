from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def ask_llama(prompt):

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=300
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {e}"