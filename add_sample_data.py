#!/usr/bin/env python3
"""
Add sample data to database tables
"""

import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

from database import SessionLocal
from models import User, Project

def add_sample_data():
    """Add sample data to the database"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        user_count = db.query(User).count()
        project_count = db.query(Project).count()
        
        if user_count > 0 or project_count > 0:
            print(f"Database already has {user_count} users and {project_count} projects")
            return
        
        # Add sample users
        users = [
            User(
                username="admin",
                email="admin@example.com",
                full_name="Administrator",
                is_active=True,
                role="admin"
            ),
            User(
                username="john_doe",
                email="john@example.com",
                full_name="John Doe",
                is_active=True,
                role="user"
            ),
            User(
                username="jane_smith",
                email="jane@example.com",
                full_name="Jane Smith",
                is_active=True,
                role="user"
            )
        ]
        
        # Add sample projects
        projects = [
            Project(
                name="Website Redesign",
                description="Redesign the company website with modern UI/UX",
                status="active"
            ),
            Project(
                name="Mobile App Development",
                description="Develop a mobile app for iOS and Android",
                status="active"
            ),
            Project(
                name="Database Migration",
                description="Migrate from old database to new system",
                status="completed"
            )
        ]
        
        # Add to database
        db.add_all(users)
        db.add_all(projects)
        db.commit()
        
        print("✅ Sample data added successfully!")
        print(f"Added {len(users)} users and {len(projects)} projects")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_data() 