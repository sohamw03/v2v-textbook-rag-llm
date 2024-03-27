from openai import OpenAI
import requests
import openai
import os

OPENAI_API_KEY = str(os.getenv("OPENAI_API_KEY"))

querytest = "Didn't understand the point 1.1.1"


def initiateChatWithContext(context, query):
    user_msg = context + "\n\n" + query

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
        "max_tokens": 200,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    print(response.json()["choices"][0]["message"]["content"])
    return response.json()["choices"][0]["message"]["content"]


# initiateChatWithContext("I didn't understand the point 1.1.1")
