#!/usr/bin/env python3
"""
Check MySQL database tables script
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def check_mysql_tables():
    """Check what tables exist in the MySQL database"""
    try:
        import pymysql
        
        # Get database configuration from environment
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = int(os.getenv("DB_PORT", "3306"))
        DB_NAME = os.getenv("DB_NAME", "ddmacbot")
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        
        # Connect to MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        print("MySQL Database Connection Successful!")
        print(f"Database: {DB_NAME}")
        print("=" * 50)
        
        with connection.cursor() as cursor:
            # Show all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"Tables in database: {len(tables)}")
            for table in tables:
                table_name = table[0]
                print(f"\n- {table_name}")
                
                # Show table structure
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print(f"  Columns:")
                for col in columns:
                    print(f"    - {col[0]} ({col[1]})")
                
                # Show row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  Rows: {count}")
                
                # Show sample data (first 3 rows)
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    rows = cursor.fetchall()
                    print(f"  Sample data:")
                    for row in rows:
                        print(f"    {row}")
        
        connection.close()
        
    except Exception as e:
        print(f"Error checking MySQL tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mysql_tables() 