from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    contacts = db.relationship('Contact', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password')
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Input validation
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('register.html', username=username)
            
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('This username is already taken. Please choose a different one.', 'error')
            return render_template('register.html', username=username)
            
        # Create new user
        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in with your new account.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html', username=username)
        
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
        contact = Contact(name=name, phone=phone, email=email, user_id=current_user.id)
        db.session.add(contact)
        db.session.commit()
        
        flash('Contact added successfully!')
        return redirect(url_for('dashboard'))
        
    return render_template('add_contact.html')

@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    
    if contact.owner != current_user:
        flash('You do not have permission to edit this contact')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        contact.name = request.form.get('name')
        contact.phone = request.form.get('phone')
        contact.email = request.form.get('email')
        
        db.session.commit()
        flash('Contact updated successfully!')
        return redirect(url_for('dashboard'))
        
    return render_template('edit_contact.html', contact=contact)

@app.route('/delete_contact/<int:id>', methods=['POST'])
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    
    if contact.owner != current_user:
        flash('You do not have permission to delete this contact')
        return redirect(url_for('dashboard'))
    
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('dashboard'))
        
    contacts = Contact.query.filter(
        (Contact.name.ilike(f'%{query}%')) |
        (Contact.phone.ilike(f'%{query}%')) |
        (Contact.email.ilike(f'%{query}%')),
        Contact.user_id == current_user.id
    ).all()
    
    return render_template('search.html', contacts=contacts, query=query)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
