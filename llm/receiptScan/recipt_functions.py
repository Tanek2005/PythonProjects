import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
import pytesseract
from PIL import Image
import json

def extract_pdf_text(pdf_path):
    if not pdf_path:
        raise ValueError("PDF path is required.")
    os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_documents(docs)
    return texts

def query(vector_or_text, prompt):
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDBZsUXvuiI8VbNJCtq7u7xacpQcFKXZD0"
    if isinstance(vector_or_text, str):
        doc = Document(page_content=vector_or_text)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_documents([doc])
    else:
        texts = vector_or_text

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    vectorstore = FAISS.from_documents(texts, embeddings)
    retriever = vectorstore.as_retriever()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        return_source_documents=True
    )
    response = qa_chain.invoke({"query": prompt})
    return response["result"]

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def query_values(vector_or_text):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDBZsUXvuiI8VbNJCtq7u7xacpQcFKXZD0"

    if isinstance(vector_or_text, str):
        doc = Document(page_content=vector_or_text)
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        ).split_documents([doc])
    else:
        chunks = vector_or_text

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()
    
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    
    # First, extract items and quantities
    items_prompt = """Extract all items and their quantities from the following receipt text. 
    Return the response as a JSON object with 'items' as a list of item names and 'quantities' as a list of quantities.
    If quantity is not specified for an item, use '1' as default.
    Receipt text: """ + str(vector_or_text)
    
    items_response = model.invoke(items_prompt)
    try:
        items_data = json.loads(items_response.content)
        items = items_data.get('items', [])
        quantities = items_data.get('quantities', ['1'] * len(items))
    except json.JSONDecodeError:
        items = []
        quantities = []
    
    # Then extract other details
    details_prompt = """Extract the following details from the receipt text:
    1. Store name (as 'store_name')
    2. Total amount (as 'total_amount')
    3. Date of transaction (as 'date_of_transaction')
    
    Return the response as a JSON object with these fields.
    Receipt text: """ + str(vector_or_text)
    
    details_response = model.invoke(details_prompt)
    try:
        details = json.loads(details_response.content)
    except json.JSONDecodeError:
        details = {}
    
    # Combine all data
    result = {
        'items': items,
        'quantity': quantities,
        'store_name': details.get('store_name', 'Unknown Store'),
        'total_amount': details.get('total_amount', '0.00'),
        'date_of_transaction': details.get('date_of_transaction', 'Unknown Date')
    }
    
    return result
