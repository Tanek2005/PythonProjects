from app import app, db, User

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Verify by counting users
        user_count = User.query.count()
        print(f"Current number of users in database: {user_count}")

if __name__ == '__main__':
    init_db()
