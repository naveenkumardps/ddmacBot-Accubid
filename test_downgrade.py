#!/usr/bin/env python3
"""
Test script for the new downgrade functionality
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_downgrade_functionality():
    """Test the new downgrade functionality that drops all tables"""
    
    print("🧪 Testing Downgrade Functionality")
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
        
        # Show current tables
        print("\n📋 Current tables in database:")
        with engine.connect() as connection:
            from sqlalchemy import text
            if DB_TYPE == "mysql":
                result = connection.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
            else:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result.fetchall()]
            
            for table in tables:
                print(f"  - {table}")
        
        # Ask for confirmation
        print(f"\n⚠️  WARNING: This will drop ALL {len(tables)} tables from the database!")
        confirm = input("Are you sure you want to drop all tables? (yes/no): ")
        
        if confirm.lower() != "yes":
            print("❌ Downgrade cancelled.")
            return False
        
        # Drop all tables
        print("\n🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully!")
        
        # Verify tables are gone
        print("\n🔍 Verifying tables are removed:")
        with engine.connect() as connection:
            if DB_TYPE == "mysql":
                result = connection.execute(text("SHOW TABLES"))
                remaining_tables = [row[0] for row in result.fetchall()]
            else:
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                remaining_tables = [row[0] for row in result.fetchall()]
            
            if remaining_tables:
                print(f"⚠️  {len(remaining_tables)} tables still exist:")
                for table in remaining_tables:
                    print(f"  - {table}")
            else:
                print("✅ All tables successfully removed!")
        
        print("\n🎉 Downgrade test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during downgrade test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_downgrade_functionality() 