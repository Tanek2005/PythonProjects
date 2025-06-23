from flask import Flask, request, render_template,redirect,make_response
import sqlite3
import database_manager
app = Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_Id = request.cookies.get('user_id')
    if user_Id:
        return redirect('/')
    
    error = None
    if request.method == 'POST':
        username = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            error = "Both username and password are required"
        else:
            success, message = database_manager.addUser(username, password)
            if success:
                user_id = database_manager.getId(username)
                if user_id:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('user_id', str(user_id), max_age=60*60*24*7)
                    return resp
                else:
                    error = "Failed to log in after registration. Please try logging in."
            else:
                error = message or "Failed to create user"
    
    return render_template('signup.html', error=error)

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect('/login')
    username = database_manager.get_username(user_id)
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = request.cookies.get('user_id')
    if user_id:
        return redirect('/')
        
    if request.method == 'POST':
        username = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('form.html', error="Both username and password are required")
            
        if database_manager.checkUser(username, password):
            user_id = database_manager.getId(username)
            resp = make_response(redirect('/'))
            resp.set_cookie('user_id', str(user_id), max_age=60*60*24*7)  # 1 week cookie
            return resp
        else:
            return render_template('form.html', error="Invalid username or password")
            
    return render_template("form.html")

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.delete_cookie('user_id')
    return resp


@app.route('/add', methods=['GET', 'POST'])
def addContact():
    user_id= request.cookies.get('user_id')
    if request.method == 'POST':
        name = request.form['name']
        phoneNo = request.form['phone']
        email = request.form['email']
        database_manager.addContact(user_id,name, phoneNo, email)
    return render_template("addcontact.html")


@app.route('/update', methods=['GET', 'POST'])
def updateContact():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect('/login')
        
    username = database_manager.get_username(user_id)
    error = None
    contact = None
    
    if request.method == 'POST':
        button = request.form.get('action')
        
        if button == "search":
            contact_name = request.form.get('Search', '').strip()
            if not contact_name:
                error = "Please enter a contact name to search"
            else:
                contact = database_manager.searchByName(contact_name, user_id)
                if contact == ("name not found", "phone no not found", "email not found"):
                    error = f"Contact '{contact_name}' not found"
                    contact = None
                    
        elif button == "update":
            contact_name = request.form.get('search', '').strip()
            new_name = request.form.get('name', '').strip()
            new_phone = request.form.get('number', '').strip()
            new_email = request.form.get('email', '').strip()
            
            if not all([contact_name, new_name, new_phone]):
                error = "Name and phone number are required"
            else:
                contact = database_manager.searchByName(contact_name, user_id)
                if contact == ("name not found", "phone no not found", "email not found"):
                    error = f"Contact '{contact_name}' not found"
                else:
                    name, phone, email = contact
                    database_manager.updateContact(user_id, name, new_name, new_phone, new_email, phone, email)
                    return redirect('/')
    
    return render_template('update.html', 
                         contact=contact, 
                         username=username,
                         error=error)


@app.route('/delete', methods=['GET', 'POST'])
def deleteContact():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect('/login')
        
    username = database_manager.get_username(user_id)
    error = None
    contact = None
    
    if request.method == 'POST':
        button = request.form.get('action')
        
        if button == "search":
            contact_name = request.form.get('Search', '').strip()
            if not contact_name:
                error = "Please enter a contact name to search"
            else:
                contact = database_manager.searchByName(contact_name, user_id)
                if contact == ("name not found", "phone no not found", "email not found"):
                    error = f"Contact '{contact_name}' not found"
                    contact = None
                    
        elif button == "delete":
            contact_name = request.form.get('search', '').strip()
            if not contact_name:
                error = "No contact selected"
            else:
                contact = database_manager.searchByName(contact_name, user_id)
                if contact == ("name not found", "phone no not found", "email not found"):
                    error = f"Contact '{contact_name}' not found"
                else:
                    name, phone, email = contact
                    database_manager.deleteContact(user_id, name, phone, email)
                    return redirect('/')
    
    return render_template('delete.html', 
                         contact=contact, 
                         username=username,
                         error=error)


@app.route('/contacts')
def view_contacts():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect('/login')
        
    username = database_manager.get_username(user_id)
    contacts = database_manager.get_all_contacts(user_id)
    
    return render_template('contacts.html', 
                         contacts=contacts, 
                         username=username,
                         contact_count=len(contacts))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)