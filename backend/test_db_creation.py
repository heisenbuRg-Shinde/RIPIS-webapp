from app.core.database import SessionLocal, init_db
from app.core.auth import get_password_hash
from app.core.database import User

def test_create_user():
    print("Initializing DB...")
    init_db()
    
    print("Testing password hashing...")
    pwd = "password123"
    try:
        hashed = get_password_hash(pwd)
        print(f"Hash generated: {hashed[:10]}...")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"HASHING ERROR: {e}")
        return

    print("Creating DB session...")
    db = SessionLocal()
    
    try:
        user_data = {"username": "test_script_user", "email": "test_script@example.com"}
        
        # Cleanup
        existing = db.query(User).filter(User.username == user_data['username']).first()
        if existing:
            print("Deleting existing test user...")
            db.delete(existing)
            db.commit()

        print("Creating new user...")
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
            hashed_password=hashed
        )
        db.add(new_user)
        db.commit()
        print("User committed successfully!")
        
    except Exception as e:
        print(f"DB ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_create_user()
