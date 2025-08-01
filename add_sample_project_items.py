#!/usr/bin/env python3
"""
Add sample project items to database
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
from models import ProjectItem, User, Project

def add_sample_project_items():
    """Add sample project items to the database"""
    db = SessionLocal()
    
    try:
        # Check if project items already exist
        item_count = db.query(ProjectItem).count()
        
        if item_count > 0:
            print(f"Database already has {item_count} project items")
            return
        
        # Get existing users and projects
        users = db.query(User).all()
        projects = db.query(Project).all()
        
        if not users or not projects:
            print("No users or projects found. Please add sample data first.")
            return
        
        # Sample project items
        project_items = [
            ProjectItem(
                project_id=projects[0].id,  # Website Redesign
                user_id=users[0].id,  # Admin
                description="Premium Web Hosting Package",
                quantity=1.0,
                trade_price=99.99,
                price_unit="month",
                discount_percent=10.0,
                net_cost=89.99,
                total_material=89.99,
                manufacturer_name="HostGator",
                supplier_name="HostGator Inc.",
                supplier_code="HG001",
                sort_code_1="Hosting",
                sort_code_2="Premium"
            ),
            ProjectItem(
                project_id=projects[0].id,  # Website Redesign
                user_id=users[1].id,  # John Doe
                description="SSL Certificate",
                quantity=1.0,
                trade_price=49.99,
                price_unit="year",
                net_cost=49.99,
                total_material=49.99,
                manufacturer_name="DigiCert",
                supplier_name="DigiCert Inc.",
                supplier_code="DC001",
                sort_code_1="Security",
                sort_code_2="SSL"
            ),
            ProjectItem(
                project_id=projects[1].id,  # Mobile App Development
                user_id=users[2].id,  # Jane Smith
                description="iOS Developer License",
                quantity=1.0,
                trade_price=99.00,
                price_unit="year",
                net_cost=99.00,
                total_material=99.00,
                manufacturer_name="Apple Inc.",
                supplier_name="Apple Developer",
                supplier_code="AP001",
                sort_code_1="License",
                sort_code_2="iOS"
            ),
            ProjectItem(
                project_id=projects[1].id,  # Mobile App Development
                user_id=users[0].id,  # Admin
                description="Android Developer License",
                quantity=1.0,
                trade_price=25.00,
                price_unit="one-time",
                net_cost=25.00,
                total_material=25.00,
                manufacturer_name="Google",
                supplier_name="Google Play Console",
                supplier_code="GP001",
                sort_code_1="License",
                sort_code_2="Android"
            ),
            ProjectItem(
                project_id=projects[2].id,  # Database Migration
                user_id=users[1].id,  # John Doe
                description="Database Backup Service",
                quantity=12.0,
                trade_price=19.99,
                price_unit="month",
                discount_percent=15.0,
                net_cost=203.87,
                total_material=203.87,
                manufacturer_name="AWS",
                supplier_name="Amazon Web Services",
                supplier_code="AWS001",
                sort_code_1="Backup",
                sort_code_2="Cloud"
            )
        ]
        
        # Add to database
        db.add_all(project_items)
        db.commit()
        
        print("✅ Sample project items added successfully!")
        print(f"Added {len(project_items)} project items")
        
        # Show summary
        for item in project_items:
            project = db.query(Project).filter(Project.id == item.project_id).first()
            user = db.query(User).filter(User.id == item.user_id).first()
            print(f"- {item.description} (Project: {project.name}, User: {user.username})")
        
    except Exception as e:
        print(f"❌ Error adding sample project items: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_project_items() 