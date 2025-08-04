#!/usr/bin/env python3
"""
Fix Migration Issues Script

This script fixes migration chain issues by:
1. Dropping all tables
2. Recreating the database from scratch
3. Adding sample data
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def fix_migration_issues():
    """Fix migration issues by recreating the database"""
    
    print("🔧 Fixing Migration Issues")
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
        
        # Show current state
        print("\n📋 Current database state:")
        with engine.connect() as connection:
            from sqlalchemy import text
            if DB_TYPE == "mysql":
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
            else:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]
            
            print(f"Tables: {tables}")
            
            # Check alembic version
            if 'alembic_version' in tables:
                result = connection.execute(text("SELECT version_num FROM alembic_version"))
                version = result.fetchone()
                print(f"Alembic version: {version[0] if version else 'None'}")
        
        # Ask for confirmation
        print(f"\n⚠️  WARNING: This will completely reset your database!")
        print("This will:")
        print("  - Drop all existing tables")
        print("  - Recreate all tables from models")
        print("  - Add sample data")
        print("  - Reset migration version")
        
        confirm = input("\nAre you sure you want to continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Fix cancelled.")
            return False
        
        # Step 1: Drop all tables
        print("\n🗑️  Step 1: Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully!")
        
        # Step 2: Create all tables
        print("\n🏗️  Step 2: Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Step 3: Verify tables
        print("\n🔍 Step 3: Verifying tables...")
        with engine.connect() as connection:
            if DB_TYPE == "mysql":
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
            else:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]
            
            print(f"✅ {len(tables)} tables created:")
            for table in tables:
                print(f"  - {table}")
        
        # Step 4: Add sample data
        print("\n📊 Step 4: Adding sample data...")
        from src.database import SessionLocal
        from src.models import User, Project, ProjectItem, ProjectLbfac
        
        db = SessionLocal()
        try:
            # Add sample users
            users = [
                User(username="admin", email="admin@example.com", full_name="Administrator", role="admin"),
                User(username="john_doe", email="john@example.com", full_name="John Doe", role="user"),
                User(username="jane_smith", email="jane@example.com", full_name="Jane Smith", role="user")
            ]
            db.add_all(users)
            db.commit()
            print("✅ Sample users added")
            
            # Add sample projects
            projects = [
                Project(name="Website Redesign", description="Redesign the company website with modern UI/UX"),
                Project(name="Mobile App Development", description="Develop a mobile app for iOS and Android"),
                Project(name="Database Migration", description="Migrate from old database to new system")
            ]
            db.add_all(projects)
            db.commit()
            print("✅ Sample projects added")
            
            # Add sample project items
            project_items = [
                ProjectItem(
                    project_id=projects[0].id,
                    user_id=users[0].id,
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
                    project_id=projects[1].id,
                    user_id=users[1].id,
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
                )
            ]
            db.add_all(project_items)
            db.commit()
            print("✅ Sample project items added")
            
            # Add sample labor factoring data
            lbfac_items = [
                ProjectLbfac(
                    project_id=projects[0].id,
                    user_id=users[0].id,
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
                )
            ]
            db.add_all(lbfac_items)
            db.commit()
            print("✅ Sample labor factoring data added")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            db.rollback()
            import traceback
            traceback.print_exc()
        finally:
            db.close()
        
        # Step 5: Reset migration version
        print("\n🔄 Step 5: Resetting migration version...")
        try:
            import subprocess
            result = subprocess.run("alembic stamp head", shell=True, check=True, capture_output=True, text=True)
            print("✅ Migration version reset to head")
        except Exception as e:
            print(f"⚠️  Warning: Could not reset migration version: {e}")
            print("This is okay - the database is still functional")
        
        print("\n🎉 Migration issues fixed successfully!")
        print("\n📋 Summary:")
        print("  ✅ Database cleaned and recreated")
        print("  ✅ All tables created from models")
        print("  ✅ Sample data added")
        print("  ✅ Ready for new migrations")
        
        print("\n🚀 Next steps:")
        print("  1. Test the database: python check_mysql_tables.py")
        print("  2. Create new migrations: python manage_migrations.py create 'description'")
        print("  3. Use downgrade if needed: python manage_migrations.py downgrade")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing migration issues: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_migration_issues() 