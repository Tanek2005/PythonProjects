import csv
import os
import pandas as pd
from flask import Flask,request,render_template

fileName = 'contacts.csv'

#############################################################################################
header = ['name', 'phone_no', 'email']

#############################################################################################  

# Common Functions

def readFile():
    try:
        df = pd.read_csv(fileName)
        print(df)
    except FileNotFoundError:
        print(f"File '{fileName}' does not exist.")
    except Exception as e:
                print("Error while reading the file:", e)



#############################################################################################
#  Functions for csvfunctions for contact app
#############################################################################################


def updateContact(name,newName,newPhone,newEmail):
  

        
        with open(fileName, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)

        contactName = name
        for row in rows:
            if row[0].strip().lower() == contactName.strip().lower():
           

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

   
#############################################################################################

def addContact(name,phone_no,email):
   
   
  
        with open(fileName, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(header)
                    writer.writerow([name, phone_no, email])

                
    
       

#############################################################################################

def deleteContact(name):
     
   
        rows = []

        with open(fileName, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]


        header, data = rows[0], rows[1:]

        updated_data = [row for row in data if row[0].strip().lower() != name.strip().lower()]

        if len(data) == len(updated_data):
             return 1
           
        else:
            
            with open(fileName, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(updated_data)
           


    
#############################################################################################

