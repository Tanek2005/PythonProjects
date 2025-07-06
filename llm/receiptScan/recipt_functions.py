import os
from dotenv import load_dotenv
load_dotenv() 

import json
import sqlite3
import pytesseract
from PIL import Image, ImageFile
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_core.documents import Document

ImageFile.LOAD_TRUNCATED_IMAGES = True

fileName = "receipt_database.db"

def extract_pdf_text(pdf_path):
    docs = PyPDFLoader(pdf_path).load()
    return "\n".join(doc.page_content for doc in docs)

def image_to_text(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        return pytesseract.image_to_string(img, lang="eng").strip()

def query_values(vector_or_text):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set in environment variables.")

    if isinstance(vector_or_text, str):
        doc = Document(page_content=vector_or_text)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents([doc])
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        if not chunks:
            raise ValueError("No text chunks found to create embeddings.")
        vectorstore = FAISS.from_documents(chunks, embeddings)
    else:
        vectorstore = vector_or_text

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        convert_system_message_to_human=True
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        return_source_documents=True
    )
    prompt = (
        "Extract the following values from the receipt: "
        "items purchased, their quantities, the store name, the date of transaction, and the total amount. "
        "Return the output as a JSON object with keys: items, quantity, store_name, date_of_transaction, total_amount."
    )
    response = qa_chain.invoke({"query": prompt})
    text = response["result"].strip()

    if text.startswith("```"):
        text = text.lstrip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(f"Model response could not be parsed as JSON:\n\n{text}")

    if "total_amount" in data and data["total_amount"]:
        data["total_amount"] = data["total_amount"].replace(",", ".")
    else:
        data["total_amount"] = "0.0"

    if "quantity" in data and data["quantity"]:
        cleaned_quantities = []
        for q in data["quantity"]:
            if q is None:
                q = "0"
            q = q.replace(",", ".").strip()
            if not any(c.isdigit() for c in q):
                q = "0"
            cleaned_quantities.append(q)
        data["quantity"] = cleaned_quantities
    else:
        data["quantity"] = []

    if "items" not in data or data["items"] is None:
        data["items"] = []

    if "store_name" not in data or not data["store_name"]:
        data["store_name"] = "Unknown Store"

    if "date_of_transaction" not in data or not data["date_of_transaction"]:
        data["date_of_transaction"] = "Unknown Date"

    return data

def checkId(user_id):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    r = cursor.fetchone()
    conn.close()
    return r[0] if r else 0

def addUser(name, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
    conn.commit()
    conn.close()

def getId(username, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    r = cursor.fetchone()
    conn.close()
    return r[0] if r else 0

def addData(user_id, items, quantity, storename, date, total_amount):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO receipts (user_id, item, quantity, storename, dateoftransaction, total_amount) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, items, quantity, storename, date, total_amount)
    )
    conn.commit()
    conn.close()