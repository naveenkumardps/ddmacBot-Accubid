#!/usr/bin/env python3
"""
Database Migration Management Script

This script provides easy commands to manage database migrations.
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return None

def test_db_connection():
    """Test database connection before running migrations"""
    try:
        from src.database import test_connection, DB_TYPE
        print(f"Testing connection to {DB_TYPE} database...")
        if test_connection():
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            return False
    except Exception as e:
        print(f"❌ Error testing database connection: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_migrations.py <command>")
        print("\nAvailable commands:")
        print("  test              - Test database connection")
        print("  create <message>  - Create a new migration")
        print("  upgrade           - Apply all pending migrations")
        print("  downgrade         - Revert the last migration")
        print("  current           - Show current migration version")
        print("  history           - Show migration history")
        print("  status            - Show migration status")
        print("  reset             - Reset database (drop all tables and recreate)")
        return

    command = sys.argv[1]

    if command == "test":
        test_db_connection()
    
    elif command == "create" and len(sys.argv) >= 3:
        message = sys.argv[2]
        print(f"Creating migration: {message}")
        
        # Test connection first
        if not test_db_connection():
            print("Cannot create migration - database connection failed!")
            return
            
        result = run_command(f"alembic revision --autogenerate -m \"{message}\"")
        if result is not None:
            print("Migration created successfully!")
        else:
            print("Failed to create migration.")
    
    elif command == "upgrade":
        print("Applying migrations...")
        
        # Test connection first
        if not test_db_connection():
            print("Cannot apply migrations - database connection failed!")
            return
            
        result = run_command("alembic upgrade head")
        if result is not None:
            print("Migrations applied successfully!")
        else:
            print("No pending migrations to apply or migration failed.")
    
    elif command == "downgrade":
        print("Reverting last migration...")
        
        # Test connection first
        if not test_db_connection():
            print("Cannot revert migration - database connection failed!")
            return
            
        result = run_command("alembic downgrade -1")
        if result is not None:
            print("Migration reverted successfully!")
        else:
            print("Failed to revert migration.")
    
    elif command == "current":
        print("Current migration version:")
        result = run_command("alembic current")
        if result:
            print(result)
        else:
            print("Failed to get current version.")
    
    elif command == "history":
        print("Migration history:")
        result = run_command("alembic history")
        if result:
            print(result)
        else:
            print("Failed to get history.")
    
    elif command == "status":
        print("Migration status:")
        result = run_command("alembic current")
        if result:
            print(f"Current version: {result.strip()}")
        else:
            print("Failed to get current version.")
        
        print("\nMigration history:")
        history_result = run_command("alembic history")
        if history_result:
            print(history_result)
        else:
            print("Failed to get history.")
    
    elif command == "reset":
        print("⚠️  WARNING: This will drop all tables and recreate them!")
        confirm = input("Are you sure you want to continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Reset cancelled.")
            return
            
        # Test connection first
        if not test_db_connection():
            print("Cannot reset database - database connection failed!")
            return
            
        print("Dropping all tables...")
        try:
            from src.database import engine
            from src.models import Base
            Base.metadata.drop_all(bind=engine)
            print("Tables dropped successfully!")
            
            print("Recreating tables...")
            Base.metadata.create_all(bind=engine)
            print("Tables recreated successfully!")
            
            print("Resetting migration version...")
            run_command("alembic stamp head")
            print("Database reset completed!")
            
        except Exception as e:
            print(f"Error resetting database: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python manage_migrations.py' to see available commands.")

if __name__ == "__main__":
    main() 