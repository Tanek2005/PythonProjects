import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, make_response, request
from recipt_functions import (
    extract_pdf_text,
    image_to_text,
    query_values,
    getId,
    checkId,
    addUser,
    addData,
)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    action = request.form.get("action")

    if action == "login":
        user_id = getId(username, password)
        if user_id:
            resp = make_response(redirect("/upload"))
            resp.set_cookie("user_id", str(user_id))
            return resp
        else:
            return "Invalid credentials", 401

    elif action == "signup":
        return redirect("/signup")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            addUser(username, password)
            user_id = getId(username, password)
            resp = make_response(redirect("/upload"))
            resp.set_cookie("user_id", str(user_id))
            return resp
    return render_template("signup.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    user_id = request.cookies.get("user_id")
    if not checkId(user_id):
        return redirect("/")

    if request.method == "POST":
        uploaded_file = request.files.get("document")
        if not uploaded_file:
            return "No file uploaded", 400

        filename = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(filename)

        if filename.lower().endswith(".pdf"):
            text = extract_pdf_text(filename)
        else:
            text = image_to_text(filename)

        data = query_values(text)

        items = ",".join(data.get("items", []))
        quantity = ",".join(data.get("quantity", []))
        store_name = data.get("store_name") or "Unknown Store"
        date_of_transaction = data.get("date_of_transaction") or "Unknown Date"
        total_amount = data.get("total_amount") or "0.0"

        if items and total_amount and user_id:
            addData(
                user_id,
                items,
                quantity,
                store_name,
                date_of_transaction,
                total_amount,
            )
            return "Receipt data saved successfully"
        else:
            return f'''Empty receipt:
            items: {items},
            quantity: {quantity},
            store: {store_name},
            date: {date_of_transaction},
            amount: {total_amount},
            Text: {text}
            '''

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)