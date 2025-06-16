import sqlite3

fileName = 'contacts_database.db'

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
        return result
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

def addContact(id,name,phoneNo,email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    INSERT INTO contacts(name,phoneNo,email,userid)
    VALUES ('{name}', '{phoneNo}', '{email}', '{id}')
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def searchByName(contactName):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT name, phoneNo, email
    FROM contacts
    WHERE name = '{contactName}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result
    else:
        return ("name not found", "phone no not found", "email not found")

def deleteContact(id, name, phoneNo, email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    DELETE FROM contacts
    WHERE name= '{name}' AND phoneNo= '{phoneNo}' AND email= '{email}' AND userid='{id}'
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def updateContact(id,contactName, newName, newphoneNo, newEmail, phoneNo, email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    UPDATE contacts
    SET name = '{newName}', phoneNo = '{newphoneNo}', email = '{newEmail}'
    WHERE name = '{contactName}' AND phoneNo = '{phoneNo}' AND email = '{email}' AND userid='{id}'
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()