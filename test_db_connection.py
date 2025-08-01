#!/usr/bin/env python3
"""
Database Connection Test Script

This script tests the database connection based on the configuration in your .env file.
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

from database import test_connection, init_db, DB_TYPE, DATABASE_URL

def main():
    print("=" * 50)
    print("Database Connection Test")
    print("=" * 50)
    
    print(f"Database Type: {DB_TYPE}")
    print(f"Database URL: {DATABASE_URL}")
    print("-" * 50)
    
    # Test connection
    print("Testing database connection...")
    if test_connection():
        print("✅ Database connection successful!")
        
        # Test table creation
        print("\nTesting table creation...")
        if init_db():
            print("✅ Database tables created successfully!")
        else:
            print("❌ Failed to create database tables")
    else:
        print("❌ Database connection failed!")
        print("\nTroubleshooting tips:")
        print("1. Check your .env file configuration")
        print("2. Ensure the database server is running")
        print("3. Verify credentials and connection details")
        print("4. Check firewall settings if connecting remotely")
        
        if DB_TYPE == "mysql":
            print("\nMySQL specific tips:")
            print("- Ensure MySQL server is running")
            print("- Check if the database exists")
            print("- Verify user permissions")
            
        elif DB_TYPE == "postgresql":
            print("\nPostgreSQL specific tips:")
            print("- Ensure PostgreSQL server is running")
            print("- Check if the database exists")
            print("- Verify user permissions")
            
        elif DB_TYPE == "supabase":
            print("\nSupabase specific tips:")
            print("- Verify SUPABASE_URL and SUPABASE_KEY")
            print("- Check if your Supabase project is active")
            print("- Ensure the database is accessible")

if __name__ == "__main__":
    main() 