from openai import OpenAI
import requests
import openai
import os
from .translate import translate

OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

def initiateChatWithContext(context, query, userLanguage) -> str:
    query = translate(userLanguage, "en", query)

    user_msg = f"""Context: {context}
    
    Query: {query}
    
    Language: English.
    """

    system_msg = "You are a ninth grade science teacher. You will explain the concept in simple and clear language such that even a fifth grade student understands."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [
            {"role": "system", "content": system_msg},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_msg},
                ],
            },
        ],
        "max_tokens": 512,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    responseJson = response.json()
    print(responseJson)
    return responseJson["choices"][0]["message"]["content"]


if __name__ == "__main__":
    from loadData import loadData

    context = loadData()
    query = "वन पॉईंट वन समझ नहीं आया"
    initiateChatWithContext(context, query)
