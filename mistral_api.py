import os
import requests
from dotenv import load_dotenv

load_dotenv("api.env")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def query_mistral(prompt, temperature=0.7):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    json_data = {
        "model": "mistral-large",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content']