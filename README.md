# 💼 AI Investment Analyst + Explainer (UK Stocks)

This is a Streamlit-based dashboard and chatbot that helps users explore UK stock insights, including:
- 🧠 AI Chat for finance queries
- 📊 Stock KPI analysis
- 📰 Financial news summaries
- 📈 Multi-stock comparison
- 🏭 Sector benchmarks

Built with:
- `LangChain` + `OpenAI`
- `yfinance`, `newsapi`, `Plotly`
- `Streamlit`

🔗 [Visit the App](https://huggingface.co/spaces/kartikG2000/ai-finance-dashboard)


## 🚀 Deployment
Deployed on Hugging Face Spaces using `streamlit` SDK. Secure API keys via Secrets:
- `OPENAI_API_KEY`
- `NEWS_API_KEY`

---

# .huggingface.yml

sdk: streamlit
app_file: app.py
python_version: 3.10
