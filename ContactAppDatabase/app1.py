from flask import Flask, request, render_template, redirect
import sqlite3
import database_manager

app = Flask(__name__)
id = None 

@app.route('/adduser', methods=['GET', 'POST'])
def addUserRoute():
    global id
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        database_manager.addUser(username, password)
        id = database_manager.getId(username)
        return render_template('index.html')
    return render_template('AddUserForm.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    global id
    conn = sqlite3.connect("contacts_database.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        password TEXT,
        createdate TEXT DEFAULT CURRENT_TIMESTAMP,
        updatedate TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY,
        userid INTEGER,
        name TEXT,
        phoneNo TEXT,
        email TEXT,
        createdate TEXT DEFAULT CURRENT_TIMESTAMP,
        updatedate TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userid) REFERENCES users(id)
    )
    ''')
    cursor.execute('DROP TABLE IF EXISTS contactsList')
    conn.commit()
    conn.close()

    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')
        if request.form.get('action') == 'Login':
            if database_manager.checkUser(username, password):
                id = database_manager.getId(username)
                return render_template('index.html')
            else:
                return render_template('form.html', name="invalid", password="invalid")
        elif request.form.get('action') == 'add':
            return redirect('/adduser')

    return render_template("form.html")

@app.route('/add', methods=['GET', 'POST'])
def addContactRoute():
    if request.method == 'POST':
        name = request.form['name']
        phoneNo = request.form['phone']
        email = request.form['email']
        database_manager.addContact(id, name, phoneNo, email)
    return render_template("addcontact.html")

@app.route('/update', methods=['GET', 'POST'])
def updateContactRoute():
    if request.method == 'POST':
        contactName = request.form['Search']
        button = request.form.get('action')
        if button == "search":
            name, phoneNo, email = database_manager.searchByName(contactName)
            return render_template("update.html", name=name, phoneNo=phoneNo, email=email, search=name)
        if button == "update":
            newName = request.form.get('name')
            newPhone = request.form.get('number')
            newEmail = request.form.get('email')
            name, phoneNo, email = database_manager.searchByName(contactName)
            database_manager.updateContact(id, name, newName, newPhone, newEmail, phoneNo, email)
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def deleteContactRoute():
    if request.method == 'POST':
        contactName = request.form['Search']
        button = request.form.get('action')
        if button == "search":
            name, phoneNo, email = database_manager.searchByName(contactName)
            return render_template("delete.html", name=name, phoneNo=phoneNo, email=email, search=name)
        if button == "delete":
            name, phoneNo, email = database_manager.searchByName(contactName)
            database_manager.deleteContact(id, name, phoneNo, email)
    return render_template("delete.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)