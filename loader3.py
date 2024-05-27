import os
import fitz  # PyMuPDF
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Configure Streamlit
st.set_page_config(layout="wide", page_title="EABL RAG Application", page_icon=":rocket:")

# Load environment variables
load_dotenv()

# Input field for user's OpenAI API key
user_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if user_api_key:
    os.environ['OPENAI_API_KEY'] = user_api_key
    
    # Extract text from PDF and save to a text file
    pdf_path = "2023-EABL-Annual-Report.pdf"
    txt_path = "EABL.txt"

    with fitz.open(pdf_path) as doc:
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            for page in doc:
                txt_file.write(page.get_text())
    
    # Load the text file and split it into chunks
    raw_documents = TextLoader(txt_path).load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    
    # Create FAISS index
    db = FAISS.from_documents(documents, OpenAIEmbeddings())

    # Input field for user query
    query = st.text_input("Ask a question about the EABL annual report:", key="query")

    if query:
        # Perform similarity search
        docs = db.similarity_search(query, k=2)

        # Display search results
        st.write("Search Results:")
        for doc in docs:
            st.write(f"Page {doc.metadata['page']}: {doc.page_content[:300]}")
else:
    st.write("Please enter your OpenAI API key to proceed.")
