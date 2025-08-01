#!/usr/bin/env python3
"""
Check database tables script
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

from database import engine
from sqlalchemy import text

def check_tables():
    """Check what tables exist in the database"""
    try:
        with engine.connect() as conn:
            # For SQLite
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = result.fetchall()
            
            print("Tables in database:")
            if tables:
                for table in tables:
                    print(f"- {table[0]}")
                    
                    # Show table structure
                    try:
                        result = conn.execute(text(f"PRAGMA table_info({table[0]})"))
                        columns = result.fetchall()
                        print(f"  Columns:")
                        for col in columns:
                            print(f"    - {col[1]} ({col[2]})")
                        
                        # Show row count
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table[0]}"))
                        count = result.fetchone()[0]
                        print(f"  Rows: {count}")
                        
                        # Show sample data (first 3 rows)
                        if count > 0:
                            result = conn.execute(text(f"SELECT * FROM {table[0]} LIMIT 3"))
                            rows = result.fetchall()
                            print(f"  Sample data:")
                            for row in rows:
                                print(f"    {row}")
                        print()
                    except Exception as e:
                        print(f"  Error getting table info: {e}")
            else:
                print("No tables found!")
                
            # Also check alembic_version table
            try:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                version = result.fetchone()
                if version:
                    print(f"Alembic version: {version[0]}")
                else:
                    print("No alembic_version table found!")
            except Exception as e:
                print(f"Error checking alembic_version: {e}")
                
    except Exception as e:
        print(f"Error checking tables: {e}")

if __name__ == "__main__":
    check_tables() 