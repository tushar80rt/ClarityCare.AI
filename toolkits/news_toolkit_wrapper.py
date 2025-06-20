import os
import requests
from dotenv import load_dotenv

load_dotenv("api.env")  

def get_wellness_news():
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    if not NEWSAPI_KEY:
        return ["❌ NEWSAPI_KEY not found in environment."]

    url = (
        "https://newsapi.org/v2/everything?"
        "q=mental+health+OR+wellness&"
        "language=en&"
        f"apiKey={NEWSAPI_KEY}"
    )

    try:
        res = requests.get(url)
        data = res.json()
        if data.get("status") != "ok":
            return [f"⚠️ Error from NewsAPI: {data.get('message', 'Unknown error')}"]
        return [a["title"] for a in data.get("articles", [])[:5]]

    except Exception as e:
        return [f"⚠️ Exception while fetching news: {str(e)}"]










