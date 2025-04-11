# agents/sector_analysis.py
import streamlit as st
import yfinance as yf
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.4)

# Sample sector benchmark data (in practice, replace with actual sector averages from a DB or API)
SECTOR_BENCHMARKS = {
    "Technology": {"avg_PE": 25.0},
    "Healthcare": {"avg_PE": 18.5},
    "Financial Services": {"avg_PE": 14.2},
    "Communication Services": {"avg_PE": 16.8},
    "Consumer Defensive": {"avg_PE": 20.3},
    "Energy": {"avg_PE": 12.6},
    "Industrials": {"avg_PE": 19.7}
}

def fetch_stock_kpi(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Company": info.get("shortName"),
        "P/E Ratio": info.get("trailingPE"),
        "Sector": info.get("sector"),
    }

def generate_sector_comparison(kpi_data):
    sector = kpi_data.get("Sector")
    pe = kpi_data.get("P/E Ratio")
    benchmark = SECTOR_BENCHMARKS.get(sector, {}).get("avg_PE")
    
    if benchmark is None or pe is None:
        return f"Not enough data to compare P/E ratio for {kpi_data['Company']} in the {sector} sector."

    prompt = ChatPromptTemplate.from_template(
        """The P/E ratio of {company} in the {sector} sector is {pe}. The sector average is {benchmark}.
Compare and explain if the stock is overvalued or undervalued, and what this might mean for investors."""
    )
    chain = prompt | llm
    return chain.invoke({"company": kpi_data['Company'], "sector": sector, "pe": pe, "benchmark": benchmark}).content

def run_sector_analysis():
    st.title("🏭 Sector Comparison")
    ticker = st.text_input("Enter a stock ticker:", "VOD")

    if ticker:
        ticker = ticker.strip().upper()
        with st.spinner("Fetching stock KPI and sector data..."):
            kpi_data = fetch_stock_kpi(ticker)

        st.subheader(f"📌 {kpi_data['Company']} ({ticker})")
        st.write({
            "P/E Ratio": kpi_data["P/E Ratio"],
            "Sector": kpi_data["Sector"]
        })

        st.subheader("📊 Sector Benchmark")
        benchmark = SECTOR_BENCHMARKS.get(kpi_data["Sector"], {}).get("avg_PE")
        if benchmark:
            st.write({"Sector Avg P/E": benchmark})
        else:
            st.warning("Sector benchmark not available.")

        st.subheader("🧠 AI Interpretation")
        comparison = generate_sector_comparison(kpi_data)
        st.markdown(comparison)