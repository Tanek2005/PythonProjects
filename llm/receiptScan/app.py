import os
from flask import Flask, render_template, redirect, make_response, request
from werkzeug.utils import secure_filename
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
        else:
            return "Please provide both username and password.", 400
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

        safe_filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
        uploaded_file.save(filepath)

        try:
            if filepath.lower().endswith(".pdf"):
                text = extract_pdf_text(filepath)
            else:
                text = image_to_text(filepath)
        except ValueError as e:
            return f"File processing error: {e}", 400

        data = query_values(text)
        items = ",".join(data["items"])
        quantity = ",".join(data["quantity"])

        addData(
            user_id,
            items,
            quantity,
            data["store_name"],
            data["date_of_transaction"],
            data["total_amount"],
        )

        return "Receipt data saved successfully."

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)