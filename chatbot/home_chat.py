# chatbot/home_chat.py
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate
from config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.5)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

prompt = ChatPromptTemplate.from_template(
    """You are a helpful financial investment assistant specialized in UK stock markets.
Answer user questions clearly and concisely. Be informative, but friendly.

Current conversation:
{chat_history}

User: {user_input}
AI:"""
)

chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=None, memory=memory, combine_docs_chain_kwargs={"prompt": prompt})

def run_home_chat():
    st.title("🧠 Home AI Chat")
    st.write("Ask anything about UK stocks, sectors, or financial advice:")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("AI is thinking..."):
            ai_response = chain.run(user_input)

        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)
