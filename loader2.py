from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
default_api_key = os.getenv("OPENAI_API_KEY")
user_api_key = st.text_input("Enter your OpenAI API Key:", type="password", value=default_api_key)

st.set_page_config(layout="wide", page_title="EABL RAG Application", page_icon=":rocket:")

# Input field for user's OpenAI API key
# user_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if user_api_key:
    os.environ['OPENAI_API_KEY'] = user_api_key
    
    # Load and split the predefined PDF file
    loader = PyPDFLoader("2023-EABL-Annual-Report.pdf")
    pages = loader.load_and_split()

    # Create FAISS index
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())

    # Input field for user query
    query = st.text_input("Ask a question about the EABL annual report:", key="query")

    if query:
        # Perform similarity search
        docs = faiss_index.similarity_search(query, k=2)

        # Display search results
        st.write("Search Results:")
        for doc in docs:
            st.write(f"Page {doc.metadata['page']}: {doc.page_content[:300]}")
else:
    st.write("Please enter your OpenAI API key to proceed.")
