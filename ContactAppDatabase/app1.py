import csv
import os
import pandas as pd
from flask import Flask,request,render_template
import sys
from pathlib import Path

library_path1 = Path(__file__).resolve().parent.parent/ "untitled folder"
sys.path.append(str(library_path1))

import database_manager

app=Flask(__name__)

header = ['name', 'phone_no', 'email']

@app.route('/update', methods=['GET', 'POST'])
def updateContact():
     if request.method == 'POST':
          contactName = request.form['Search']
          button=request.form.get('action')
          if button == "search":
               name,phoneNo,email = database_manager.searchByName(contactName)
               return render_template("update.html",name=name,phoneNo=phoneNo,email=email,search=name)       
          if button == "update":
              newName = request.form.get('name')
              newPhone = request.form.get('number')
              newEmail = request.form.get('email')
              name,phoneNo,email = database_manager.searchByName(contactName)
              database_manager.updateContact(name, newName, newPhone, newEmail,phoneNo,email)
     return render_template('update.html')

@app.route('/add',methods=['GET','POST'])
def addContact():
    if request.method=='POST':
         name = request.form['name']
         phone_no = request.form['phone']
         email = request.form['email']
         database_manager.addContact(name,phone_no,email)
         
    return render_template("addcontact.html")
                
@app.route('/delete', methods=['GET', 'POST'])
def deleteContact():
    if request.method == 'POST':
        contactName = request.form['Search']
        button=request.form.get('action')
        if button == "search":
               name,phoneNo,email = database_manager.searchByName(contactName)
               return render_template("delete.html",name=name,phoneNo=phoneNo,email=email,search=name)
        if button == "delete":
               name,phoneNo,email = database_manager.searchByName(contactName)
               database_manager.deleteContact(name,phoneNo,email)

    return render_template("delete.html")
@app.route('/', methods=['GET', 'POST'])
def login():
    import sqlite3

    conn = sqlite3.connect("contacts_database.db")
    cursor = conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts(
    name TEXT,
    phoneNo TEXT,
    email TEXT
)
''')
    conn.commit()
    conn.close()
    Name = "account"
    Password = "password"
    if request.method == 'POST':
        if (request.form.get('name') == Name and 
            request.form.get('password') == Password and 
            request.form.get('action')):
            return render_template("index.html")
        else:
            return render_template("form.html", name="invalid", password="invalid")

    return render_template("form.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

