# agents/news_summary.py
import streamlit as st
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import NEWS_API_KEY, OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.4)

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def fetch_news(ticker_or_topic):
    params = {
        "q": ticker_or_topic,
        "apiKey": NEWS_API_KEY,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5
    }
    response = requests.get(NEWS_ENDPOINT, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [f"- {a['title']} ({a['source']['name']})\n{a['description']}\n" for a in articles]
    else:
        return ["Failed to fetch news. Check API key or query."]


def summarize_news(articles):
    text = "\n".join(articles)
    prompt = ChatPromptTemplate.from_template(
        """Summarize the following financial news headlines and descriptions:

{text}

Return a brief summary useful for an investor."""
    )
    chain = prompt | llm
    return chain.invoke({"text": text}).content


def run_news_summary():
    st.title("📰 Financial News")
    topic = st.text_input("Enter a stock ticker or topic:", "FTSE 100")

    if topic:
        with st.spinner("Fetching latest news..."):
            articles = fetch_news(topic)

        st.subheader("🗞️ Latest Headlines")
        for article in articles:
            st.markdown(article)

        st.subheader("🧠 AI Summary")
        summary = summarize_news(articles)
        st.markdown(summary)
