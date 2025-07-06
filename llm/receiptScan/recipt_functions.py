import os, json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
import pytesseract
from PIL import Image
import sqlite3

fileName="receipt_database.db"

def extract_pdf_text(pdf_path):
    if not pdf_path:
        raise ValueError("PDF path is required.")
    docs = PyPDFLoader(pdf_path).load()
    return "\n".join(doc.page_content for doc in docs)

def query(text_or_doc, prompt):
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
    text = text_or_doc.page_content if isinstance(text_or_doc, Document) else str(text_or_doc)
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])
    return model.invoke(f"{prompt}\n\nContext:\n{text}").content

def image_to_text(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def query_values(text_or_doc):
    os.environ["GOOGLE_API_KEY"] = ""
    text = text_or_doc.page_content if isinstance(text_or_doc, Document) else str(text_or_doc)
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.environ["GOOGLE_API_KEY"])
    items_prompt = """Extract all items and their quantities from the following receipt text. 
Return as JSON with 'items' and 'quantities'. If quantity is missing, default to 1.
Receipt text: """ + text
    try:
        items_data = json.loads(model.invoke(items_prompt).content)
        items = items_data.get('items', [])
        quantities = items_data.get('quantities', ['1'] * len(items))
    except json.JSONDecodeError:
        items, quantities = [], []

    details_prompt = """Extract store name, total amount, and date of transaction from the following receipt text.
Return as JSON with keys 'store_name', 'total_amount', 'date_of_transaction'.
Receipt text: """ + text
    try:
        details = json.loads(model.invoke(details_prompt).content)
    except json.JSONDecodeError:
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
    query = f'''
    SELECT id
    FROM users
    WHERE id = '{user_id}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else :
        return 0

def addUser(name, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO users(name, password) VALUES ('{name}', '{password}')
    ''')
    conn.commit()
    conn.close()

def getId(username,password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT id
    FROM users
    WHERE name = '{username}' AND password='{password}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else :
        return 0
    
def addData(user_id,items,quantity,storename,date,total_amount):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    cursor.execute('''
INSERT INTO receipts(user_id,items,quantity,storename,dateoftransaction,amount)
                   user_id='{user_id}',items='{items}',quantity='{quantity}',dateoftransaction='{date}',total_amount='{amount}'
''')
    conn.commit()
    conn.close()

    