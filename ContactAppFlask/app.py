import csv
import os
import pandas as pd
from flask import Flask,request,render_template

import sys
from pathlib import Path



library_path = Path(__file__).resolve().parent.parent/ "Library"
sys.path.append(str(library_path))

import contact_manager



app=Flask(__name__)

#############################################################################################
header = ['name', 'phone_no', 'email']
#############################################################################################

def searchbyName(fileName):
    
    try:
        with open(fileName, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            
            for row in reader:
                if row[0].strip().lower() == fileName.strip().lower():
                    print(f"Contact found:\n Name :{row[0]}\t PhoneNo :{row[1]} Email: {row[2]}")
                    
                    break
                else:
                    continue
    except Exception as e:
        print(f"No file found of the name {fileName}",e)

@app.route('/update', methods=['GET', 'POST'])
def updateContact():
     if request.method == 'POST':
          contactName = request.form['Search']
          newName = request.form.get('name')
          newPhone = request.form.get('number')
          newEmail = request.form.get('email')
          contact_manager.updateContact(contactName,newName,newPhone,newEmail)
          
     return render_template('update.html')


@app.route('/add',methods=['GET','POST'])
def addContact():
    
    if request.method=='POST':
         name = request.form['name']
         phone_no = request.form['phone']
         email = request.form['email']
         contact_manager.addContact(name,phone_no,email)
  
    return render_template("addcontact.html")
                    

@app.route('/delete', methods=['GET', 'POST'])
def deleteContact():
    if request.method == 'POST':
        name = request.form['name']
        contact_manager.deleteContact(name)

    return render_template("delete.html")


#############################################################################################
@app.route('/')
def program():
     return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
#############################################################################################
