import csv
import os
import pandas as pd
from flask import Flask,request,render_template



#############################################################################################
header = ['name', 'phone_no', 'email']

#############################################################################################  
# Common Functions
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

def readFile(fileName):
    try:
        df = pd.read_csv(fileName)
        print(df)
    except FileNotFoundError:
        print(f"File '{fileName}' does not exist.")
    except Exception as e:
                print("Error while reading the file:", e)



#############################################################################################
#  Functions for Flask App
#############################################################################################


def updateContactFlask(fileName,name):
  

    if request.method == 'POST':
        
        with open(fileName, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

        contactName = name
        for row in rows:
            if row[0].strip().lower() == contactName.strip().lower():
           
                newName = request.form.get('name')
                newPhone = request.form.get('number')
                newEmail = request.form.get('email')

                if newName:
                    row[0] = newName
            
                if newPhone:
                    row[1] = newPhone

                if newEmail:
                    row[2] = newEmail
                break  

        with open(fileName, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

    return render_template("update.html")

#############################################################################################

def addContactFlask(fileName):
   
   
    if request.method=='POST':

        with open(fileName, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(header)
                    name = request.form['name']
                    phone_no = request.form['phone']
                    email = request.form['email']
                    writer.writerow([name, phone_no, email])
  
    return render_template("addcontact.html")
                    
                
    
       

#############################################################################################

def deleteContactFlask(fileName):
     
   
    
    if request.method == 'POST':
        name = request.form['name']
        rows = []

        with open(fileName, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]


        header, data = rows[0], rows[1:]

        updated_data = [row for row in data if row[0].strip().lower() != name.strip().lower()]

        if len(data) == len(updated_data):
            message = "Contact not found."
        else:
            
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(updated_data)
            message = "Contact deleted successfully."

    return render_template("delete.html")
        
    
#############################################################################################



#############################################################################################
#Functions for CLI
#############################################################################################



def updateContact(contactName,fileName):
    try:
        
        with open(fileName, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)  

        
        for row in rows:
            if row[0].strip().lower() == contactName.strip().lower():
                newName = input("Enter new name: ")
                if newName!="":
                     row[0]=newName     
                newPhone = input("Enter new phone number: ")
                if newPhone!="":
                     row[1]=newPhone
                newEmail = input("Enter new email: ")
                if newEmail!="":
                     row[2]=newEmail
                
                break
        else:
            print(f"No contact found with the name '{contactName}'.")
            return

        
        with open(fileName, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)

        print(f"Contact '{contactName}' updated successfully.")
    
    except FileNotFoundError:
        print(f"File '{fileName}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



#############################################################################################

def addContact(fileName,name,phone_no,email):
 
            try:
                with open(fileName, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(header)
                    
            
                    writer.writerow([name, phone_no, email])
                    print("Contact added successfully.")
            except FileNotFoundError:
                print(f"File '{fileName}' does not exist. Please create it first.")
            except Exception as e:
                print("Error while adding contact:", e)

#############################################################################################

def deleteContact(fileName):
    

    try:
                rows = []
                name = input("Enter the name of the contact you want to delete: ")
                with open(fileName, mode='r', newline='') as file:
                    reader = csv.reader(file)
                    rows = [row for row in reader]
                header, data = rows[0], rows[1:]
                updated_data = [row for row in data if row[0].strip().lower() != name.strip().lower()]
                if len(data) == len(updated_data):
                    print("Contact not found.")
                else:
                    with open(fileName, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(updated_data)
                    print("Contact deleted successfully.")
    except FileNotFoundError:
                print(f"File '{fileName}' does not exist.")
    except Exception as e:
                print("Error while deleting contact:", e)

#############################################################################################