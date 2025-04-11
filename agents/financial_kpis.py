# agents/financial_kpis.py
import streamlit as st
import yfinance as yf
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.4)

def fetch_kpis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Company": info.get("shortName"),
        "P/E Ratio": info.get("trailingPE"),
        "EPS": info.get("trailingEps"),
        "ROE": info.get("returnOnEquity"),
        "ROA": info.get("returnOnAssets"),
        "Market Cap": info.get("marketCap"),
        "Sector": info.get("sector"),
        "Industry": info.get("industry")
    }

def explain_kpis(kpi_data):
    desc = "".join([f"{key}: {value}\n" for key, value in kpi_data.items() if key != "Company"])
    prompt = ChatPromptTemplate.from_template(
        """Given the following financial KPIs for {company}, explain the investment outlook:

{desc}

Return a concise analysis for investors."""
    )
    chain = prompt | llm
    return chain.invoke({"company": kpi_data['Company'], "desc": desc}).content

def run_financial_kpis():
    st.title("📊 Financial KPIs")
    ticker = st.text_input("Enter a stock ticker:", "BARC")

    if ticker:
        ticker = ticker.strip().upper()
        with st.spinner("Fetching KPIs..."):
            kpis = fetch_kpis(ticker)

        st.subheader(f"📌 {kpis['Company']} ({ticker}) KPIs")
        st.write({
            "P/E Ratio": kpis["P/E Ratio"],
            "EPS": kpis["EPS"],
            "ROE": kpis["ROE"],
            "ROA": kpis["ROA"],
            "Market Cap": kpis["Market Cap"],
            "Sector": kpis["Sector"],
            "Industry": kpis["Industry"]
        })

        st.subheader("🧠 AI Explanation")
        explanation = explain_kpis(kpis)
        st.markdown(explanation)
