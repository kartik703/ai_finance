# agents/compare_stocks.py
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY

# Initialize the LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.4)

def get_stock_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="6mo")
        data[ticker] = {
            "P/E": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
            "Sector": info.get("sector"),
            "Price Data": hist["Close"],
            "Market Cap": info.get("marketCap"),
            "Company": info.get("shortName")
        }
    return data

def generate_comparison_summary(data):
    summary_input = ""
    for ticker, stats in data.items():
        summary_input += f"{stats['Company']} ({ticker}): P/E={stats['P/E']}, EPS={stats['EPS']}, MarketCap={stats['Market Cap']}, Sector={stats['Sector']}\n"

    prompt = ChatPromptTemplate.from_template(
        """Compare the following stocks in terms of value, profitability, and growth potential:

{summary_input}

Return a concise analysis with a recommendation."""
    )
    chain = prompt | llm
    return chain.invoke({"summary_input": summary_input}).content

def plot_price_chart(data):
    fig = go.Figure()
    for ticker, stats in data.items():
        fig.add_trace(go.Scatter(
            x=stats["Price Data"].index,
            y=stats["Price Data"].values,
            name=ticker
        ))
    fig.update_layout(title="Stock Price Trend (Last 6 Months)", xaxis_title="Date", yaxis_title="Price")
    return fig

def run_compare_stocks():
    st.title("📈 Compare Stocks")
    tickers = st.text_input("Enter 2-3 stock tickers (comma separated):", "AZN, GSK")

    if tickers:
        ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
        if len(ticker_list) < 2:
            st.warning("Please enter at least two tickers.")
            return

        with st.spinner("Fetching data..."):
            data = get_stock_data(ticker_list)

        st.subheader("KPI Comparison")
        for ticker in ticker_list:
            stats = data[ticker]
            st.markdown(f"**{stats['Company']} ({ticker})**")
            st.write({
                "P/E Ratio": stats["P/E"],
                "EPS": stats["EPS"],
                "Market Cap": stats["Market Cap"],
                "Sector": stats["Sector"]
            })

        st.subheader("📉 Price Trend")
        st.plotly_chart(plot_price_chart(data), use_container_width=True)

        st.subheader("🧠 AI-Generated Analysis")
        analysis = generate_comparison_summary(data)
        st.markdown(analysis)