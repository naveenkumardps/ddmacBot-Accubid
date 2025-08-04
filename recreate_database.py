#!/usr/bin/env python3
"""
Recreate database after downgrade
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def recreate_database():
    """Recreate all tables and add sample data"""
    
    print("🔄 Recreating Database")
    print("=" * 50)
    
    try:
        from src.database import engine, test_connection, DB_TYPE
        from src.models import Base
        
        # Test connection first
        print(f"Testing connection to {DB_TYPE} database...")
        if not test_connection():
            print("❌ Database connection failed!")
            return False
        
        print("✅ Database connection successful!")
        
        # Create all tables
        print("\n🏗️  Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Verify tables are created
        print("\n🔍 Verifying tables are created:")
        with engine.connect() as connection:
            from sqlalchemy import text
            if DB_TYPE == "mysql":
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
            else:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]
            
            print(f"✅ {len(tables)} tables created:")
            for table in tables:
                print(f"  - {table}")
        
        # Add sample data
        print("\n📊 Adding sample data...")
        
        # Add sample users and projects
        from src.database import SessionLocal
        from src.models import User, Project, ProjectItem, ProjectLbfac
        
        db = SessionLocal()
        try:
            # Check if data already exists
            user_count = db.query(User).count()
            if user_count == 0:
                # Add sample users
                users = [
                    User(username="admin", email="admin@example.com", full_name="Administrator", role="admin"),
                    User(username="john_doe", email="john@example.com", full_name="John Doe", role="user"),
                    User(username="jane_smith", email="jane@example.com", full_name="Jane Smith", role="user")
                ]
                db.add_all(users)
                db.commit()
                print("✅ Sample users added")
            else:
                print(f"✅ {user_count} users already exist")
            
            # Add sample projects
            project_count = db.query(Project).count()
            if project_count == 0:
                projects = [
                    Project(name="Website Redesign", description="Redesign the company website with modern UI/UX"),
                    Project(name="Mobile App Development", description="Develop a mobile app for iOS and Android"),
                    Project(name="Database Migration", description="Migrate from old database to new system")
                ]
                db.add_all(projects)
                db.commit()
                print("✅ Sample projects added")
            else:
                print(f"✅ {project_count} projects already exist")
                
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            db.rollback()
        finally:
            db.close()
        
        print("\n🎉 Database recreation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error recreating database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    recreate_database() 