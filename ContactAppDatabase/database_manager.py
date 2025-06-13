import sqlite3

fileName = 'contacts_database.db'

def addContact(name, phoneNo, email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    INSERT INTO contactsList(name, phoneNo, email)
    VALUES ('{name}', '{phoneNo}', '{email}')
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def searchByName(contactName):
    
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()
    query = f'''
    SELECT name, phoneNo, email
    FROM contactsList
    WHERE name = '{contactName}'
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return result
    else:
        return "name not found","phone no not found","email not found"

    
def deleteContact(name,phoneNo,email):
    conn = sqlite3.connect(fileName)
    cursor = conn.cursor() 
    query = f'''
    DELETE FROM contactsList
    WHERE name= '{name}' AND phoneNo= '{phoneNo}' AND email= '{email}' ;
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()  

def updateContact(contactName, newName, phoneNo, email):

    conn = sqlite3.connect(fileName)
    cursor = conn.cursor()  
    query = f'''
    UPDATE contactsList
    SET name = '{newName}',  phoneNo = '{phoneNo}', email = '{email}'
    WHERE name = '{contactName}';
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()  