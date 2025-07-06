import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import pytesseract
from PIL import Image, ImageFile, UnidentifiedImageError
from io import BytesIO
import sqlite3

ImageFile.LOAD_TRUNCATED_IMAGES = True

fileName = "receipt_database.db"


def extract_pdf_text(pdf_path):
    if not pdf_path:
        raise ValueError("PDF path is required.")
    docs = PyPDFLoader(pdf_path).load()
    return "\n".join(doc.page_content for doc in docs)


def image_to_text(image_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            repaired_img = Image.open(buffer)
            return pytesseract.image_to_string(repaired_img)
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError("The uploaded image is invalid or cannot be read.")
    except pytesseract.TesseractError as te:
        raise ValueError("OCR failed due to image corruption. Please upload a different file.")


def query_values(text_or_doc):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDBZsUXvuiI8VbNJCtq7u7xacpQcFKXZD0"

    text = text_or_doc.page_content if isinstance(text_or_doc, Document) else str(text_or_doc)

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    items_prompt = (
        "Extract all items and their quantities from the following receipt text. "
        "Return as JSON with keys 'items' and 'quantities'. If quantity is missing, default to 1.\n\n"
        "Receipt text:\n" + text
    )

    try:
        items_response = model.invoke(items_prompt)
        items_data = json.loads(items_response.content)
        items = items_data.get('items', [])
        quantities = items_data.get('quantities', ['1'] * len(items))
    except (json.JSONDecodeError, AttributeError):
        items, quantities = [], []

    details_prompt = (
        "Extract store name, total amount, and date of transaction from the following receipt text. "
        "Return as JSON with keys 'store_name', 'total_amount', 'date_of_transaction'.\n\n"
        "Receipt text:\n" + text
    )

    try:
        details_response = model.invoke(details_prompt)
        details = json.loads(details_response.content)
    except (json.JSONDecodeError, AttributeError):
        details = {}

    return {
        'items': items,
        'quantity': quantities,
        'store_name': details.get('store_name', 'Unknown Store'),
        'total_amount': details.get('total_amount', '0.00'),
        'date_of_transaction': details.get('date_of_transaction', 'Unknown Date')
    }


def checkId(user_id):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def getId(username, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def addUser(name, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
    conn.commit()
    conn.close()


def addData(user_id, item, quantity, storename, date, total_amount):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO receipts 
        (user_id, item, quantity, storename, dateoftransaction, total_amount)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, item, quantity, storename, date, total_amount)
    )
    conn.commit()
    conn.close()