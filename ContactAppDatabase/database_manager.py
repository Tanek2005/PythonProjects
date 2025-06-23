import sqlite3
import os
from datetime import datetime

current = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fileName = 'contacts_database.db'

def init_db():
    if not os.path.exists(fileName):
        conn = sqlite3.connect(fileName)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            createdate TEXT,
            updatedate TEXT
        )
        ''')
        
        # Create contacts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phoneNo TEXT,
            email TEXT,
            userid INTEGER,
            createdate TEXT,
            updatedate TEXT,
            FOREIGN KEY (userid) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        conn.close()

# Initialize the database when this module is imported
init_db()

def getId(username):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT id
    FROM users
    WHERE name = '{username}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else :
        return 0
    
def checkId(user_id):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT id
    FROM users
    WHERE name = '{user_id}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else :
        return 0

def addUser(name, password):
    try:
        conn = sqlite3.connect(fileName)
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
        if cursor.fetchone() is not None:
            return False, "Username already exists"
            
        # Add new user
        cursor.execute('''
        INSERT INTO users(name, password, createdate, updatedate) 
        VALUES (?, ?, ?, ?)
        ''', (name, password, current, current))
        
        conn.commit()
        return True, "User created successfully"
        
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()

def checkUser(username, password):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT * FROM users
    WHERE name='{username}' AND password='{password}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return 1 if result else 0

def addContact(useid,name,phoneNo,email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    INSERT INTO contacts(name,phoneNo,email,userid,createdate,updatedate)
    VALUES ('{name}', '{phoneNo}', '{email}', '{useid}','{current}', '{current}')
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def searchByName(contactName,user_id):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT name, phoneNo, email
    FROM contacts
    WHERE name = '{contactName}' AND userid='{user_id}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result
    else:
        return ("name not found", "phone no not found", "email not found")

def deleteContact(useid, name, phoneNo, email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    DELETE FROM contacts
    WHERE name= '{name}' AND phoneNo= '{phoneNo}' AND email= '{email}' AND userid='{useid}'
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def updateContact(useid,contactName, newName, newphoneNo, newEmail, phoneNo, email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    UPDATE contacts
    SET name = '{newName}', phoneNo = '{newphoneNo}', email = '{newEmail}', updatedate='{current}'
    WHERE name = '{contactName}' AND phoneNo = '{phoneNo}' AND email = '{email}' AND userid='{useid}'

    '''
    cursor.execute(query)
    conn.commit()
    conn.close()