#!/usr/bin/env python3
"""
Add sample data to existing database
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def add_sample_data():
    """Add sample data to the existing database"""
    
    print("📊 Adding Sample Data")
    print("=" * 50)
    
    try:
        from src.database import SessionLocal, test_connection, DB_TYPE
        from src.models import User, Project, ProjectItem, ProjectLbfac
        
        # Test connection first
        print(f"Testing connection to {DB_TYPE} database...")
        if not test_connection():
            print("❌ Database connection failed!")
            return False
        
        print("✅ Database connection successful!")
        
        db = SessionLocal()
        try:
            # Check if data already exists
            user_count = db.query(User).count()
            if user_count > 0:
                print(f"✅ Database already has {user_count} users")
                print("Skipping data addition...")
                return True
            
            print("📝 Adding sample users...")
            # Add sample users
            users = [
                User(username="admin", email="admin@example.com", full_name="Administrator"),
                User(username="john_doe", email="john@example.com", full_name="John Doe"),
                User(username="jane_smith", email="jane@example.com", full_name="Jane Smith")
            ]
            db.add_all(users)
            db.commit()
            print("✅ Sample users added")
            
           
           
            
            print("\n🎉 Sample data added successfully!")
            print(f"✅ {len(users)} users added")
          
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            db.rollback()
            import traceback
            traceback.print_exc()
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_sample_data() 