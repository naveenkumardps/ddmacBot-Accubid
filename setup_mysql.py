#!/usr/bin/env python3
"""
MySQL Setup Script
"""

import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """Test MySQL connection with different configurations"""
    
    # Try different MySQL configurations
    configs = [
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'ddmacbot'
        },
        {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'ddmacbot'
        },
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'ddmacbot'
        }
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n--- Testing MySQL Configuration {i} ---")
        print(f"Host: {config['host']}")
        print(f"Port: {config['port']}")
        print(f"User: {config['user']}")
        print(f"Password: {'*' * len(config['password']) if config['password'] else '(empty)'}")
        print(f"Database: {config['database']}")
        
        try:
            import pymysql
            
            # Test connection
            connection = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                charset='utf8mb4'
            )
            
            print("✅ MySQL connection successful!")
            
            # Check if database exists
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                
                if config['database'] in databases:
                    print(f"✅ Database '{config['database']}' exists")
                    
                    # Use the database
                    cursor.execute(f"USE {config['database']}")
                    
                    # Check tables
                    cursor.execute("SHOW TABLES")
                    tables = [row[0] for row in cursor.fetchall()]
                    
                    if tables:
                        print(f"✅ Database has {len(tables)} tables: {tables}")
                    else:
                        print("⚠️  Database exists but has no tables")
                        
                else:
                    print(f"❌ Database '{config['database']}' does not exist")
                    print("Creating database...")
                    cursor.execute(f"CREATE DATABASE {config['database']}")
                    print(f"✅ Database '{config['database']}' created successfully!")
            
            connection.close()
            
            # If we get here, this configuration works
            print(f"\n🎉 Working MySQL configuration found!")
            print(f"Update your .env file with:")
            print(f"DB_HOST={config['host']}")
            print(f"DB_PORT={config['port']}")
            print(f"DB_USER={config['user']}")
            print(f"DB_PASSWORD={config['password']}")
            print(f"DB_NAME={config['database']}")
            
            return config
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            continue
    
    print("\n❌ No working MySQL configuration found!")
    print("Please check:")
    print("1. MySQL server is running")
    print("2. MySQL credentials are correct")
    print("3. MySQL is accessible on localhost:3306")
    return None

if __name__ == "__main__":
    test_mysql_connection() 