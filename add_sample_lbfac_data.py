#!/usr/bin/env python3
"""
Add sample Labor Factoring data to database
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
from models import ProjectLbfac, User, Project

def add_sample_lbfac_data():
    """Add sample Labor Factoring data to the database"""
    db = SessionLocal()
    
    try:
        # Check if lbfac data already exists
        item_count = db.query(ProjectLbfac).count()
        
        if item_count > 0:
            print(f"Database already has {item_count} Labor Factoring records")
            return
        
        # Get existing users and projects
        users = db.query(User).all()
        projects = db.query(Project).all()
        
        if not users or not projects:
            print("No users or projects found. Please add sample data first.")
            return
        
        # Sample Labor Factoring data
        lbfac_items = [
            ProjectLbfac(
                project_id=projects[0].id,  # Website Redesign
                user_id=users[0].id,  # Admin
                labor_factoring="Direct Labor",
                factor="1.25",
                percent_of_direct_hrs="100",
                hours="40",
                rate="25.00",
                sub_total="1000.00",
                brdn_percent="15",
                frng="150.00",
                brdn_total="150.00",
                frng_total="150.00",
                total="1300.00",
                full_rate="32.50",
                code="DL001",
                type="Direct"
            ),
            ProjectLbfac(
                project_id=projects[0].id,  # Website Redesign
                user_id=users[1].id,  # John Doe
                labor_factoring="Indirect Labor",
                factor="1.15",
                percent_of_direct_hrs="20",
                hours="8",
                rate="20.00",
                sub_total="160.00",
                brdn_percent="10",
                frng="16.00",
                brdn_total="16.00",
                frng_total="16.00",
                total="192.00",
                full_rate="24.00",
                code="IL001",
                type="Indirect"
            ),
            ProjectLbfac(
                project_id=projects[1].id,  # Mobile App Development
                user_id=users[2].id,  # Jane Smith
                labor_factoring="Overtime Labor",
                factor="1.5",
                percent_of_direct_hrs="25",
                hours="10",
                rate="30.00",
                sub_total="300.00",
                brdn_percent="20",
                frng="60.00",
                brdn_total="60.00",
                frng_total="60.00",
                total="420.00",
                full_rate="42.00",
                code="OT001",
                type="Overtime"
            ),
            ProjectLbfac(
                project_id=projects[1].id,  # Mobile App Development
                user_id=users[0].id,  # Admin
                labor_factoring="Supervision",
                factor="1.35",
                percent_of_direct_hrs="15",
                hours="6",
                rate="35.00",
                sub_total="210.00",
                brdn_percent="12",
                frng="25.20",
                brdn_total="25.20",
                frng_total="25.20",
                total="260.40",
                full_rate="43.40",
                code="SUP001",
                type="Supervision"
            ),
            ProjectLbfac(
                project_id=projects[2].id,  # Database Migration
                user_id=users[1].id,  # John Doe
                labor_factoring="Specialty Labor",
                factor="1.4",
                percent_of_direct_hrs="30",
                hours="12",
                rate="40.00",
                sub_total="480.00",
                brdn_percent="18",
                frng="86.40",
                brdn_total="86.40",
                frng_total="86.40",
                total="652.80",
                full_rate="54.40",
                code="SPL001",
                type="Specialty"
            )
        ]
        
        # Add to database
        db.add_all(lbfac_items)
        db.commit()
        
        print("✅ Sample Labor Factoring data added successfully!")
        print(f"Added {len(lbfac_items)} Labor Factoring records")
        
        # Show summary
        for item in lbfac_items:
            project = db.query(Project).filter(Project.id == item.project_id).first()
            user = db.query(User).filter(User.id == item.user_id).first()
            print(f"- {item.labor_factoring} (Project: {project.name}, User: {user.username})")
            print(f"  Factor: {item.factor}, Hours: {item.hours}, Rate: ${item.rate}, Total: ${item.total}")
        
    except Exception as e:
        print(f"❌ Error adding sample Labor Factoring data: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_lbfac_data() 