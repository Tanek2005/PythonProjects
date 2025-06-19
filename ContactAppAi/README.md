# Contact App

A Flask-based web application for managing your contacts with user authentication.

## Features

- User registration and login
- Add, edit, and delete contacts
- Search contacts by name, phone, or email
- Responsive design that works on mobile and desktop
- Secure password hashing
- SQLite database

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository or download the source code

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Set the Flask app environment variable:
   ```bash
   export FLASK_APP=app.py
   # On Windows use: set FLASK_APP=app.py
   ```

2. Run the application:
   ```bash
   flask run
   ```

3. Open your web browser and go to: http://127.0.0.1:5000/

## Usage

1. Register a new account or log in if you already have one
2. Add contacts using the "Add Contact" button
3. View, edit, or delete your contacts from the dashboard
4. Use the search bar to quickly find contacts

## Database

The application uses SQLite and will automatically create a `contacts.db` file in the instance folder when you first run the application.

## Security Note

This is a development setup. For production use, please:
- Set a strong `SECRET_KEY` in `app.py`
- Use a production-ready WSGI server (e.g., Gunicorn, uWSGI)
- Set up HTTPS
- Use a more robust database (e.g., PostgreSQL)
- Implement rate limiting and other security best practices

## License

This project is open source and available under the [MIT License](LICENSE).
