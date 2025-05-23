import os
import requests
import openai
import streamlit as st
from dotenv import load_dotenv

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Define topics
topics = {
    "Nutrition": "nutrition",
    "World News": "world",
    "IELTS": "ielts",
    "Weather": "weather",
    "AI Development": "artificial intelligence"
}

# Function to fetch news from News API
def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=3"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return response.json().get("articles", [])

# Function to summarize article using OpenAI Chat API
def summarize(text):
    if not text:
        return "No content to summarize."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                {"role": "user", "content": f"Please summarize this article in 3 sentences:\n{text}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Summary failed: {e}"

# Function to fetch image from Unsplash
def fetch_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get("urls", {}).get("small")

# Streamlit UI
st.title("📰 AI-Powered News Digest")

for category, query in topics.items():
    st.header(category)
    articles = fetch_news(query)
    if not articles:
        st.write("No articles found.")
        continue
    for article in articles:
        st.subheader(article.get("title", "No Title"))
        image_url = fetch_image(query)
        if image_url:
            st.image(image_url, width=400)
        summary = summarize(article.get("description") or article.get("content") or "")
        st.write(summary)
        st.markdown("---")
