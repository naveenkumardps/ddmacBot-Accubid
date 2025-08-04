#!/usr/bin/env python3
"""
Simple Excel Import for Schlegel Accubid Data
"""

import pandas as pd
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import numpy as np

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def clean_dataframe(df):
    """Clean dataframe by removing empty rows and handling NaN values"""
    # Remove rows where all values are NaN
    df = df.dropna(how='all')
    
    # Replace NaN with None for database compatibility
    df = df.replace({np.nan: None})
    
    return df

def import_ext_data_simple():
    """Import Ext (project_ext) data with better error handling"""
    
    excel_file = r"C:\Users\navee\Downloads\Schlegel Accubid in Excel (1).xlsx"
    
    print("📊 Simple Excel Import - Ext Data")
    print("=" * 50)
    print(f"File: {excel_file}")
    
    try:
        from src.database import SessionLocal, test_connection, DB_TYPE
        from src.models import User, Project, ProjectItem
        
        # Test connection first
        print(f"\nTesting connection to {DB_TYPE} database...")
        if not test_connection():
            print("❌ Database connection failed!")
            return False
        
        print("✅ Database connection successful!")
        
        # Create a new project for this import
        db = SessionLocal()
        try:
            # Get or create a user for import
            user = db.query(User).first()
            if not user:
                print("❌ No users found in database. Please run add_sample_data.py first.")
                return False
            
            # Create a new project for this import
            project = Project(
                name="Schlegel Accubid Import - Ext",
                description=f"Excel import from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                status="active"
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            
            print(f"✅ Created project: {project.name} (ID: {project.id})")
            
            # Import Ext data
            print("\n📊 Reading Ext sheet...")
            df_ext = pd.read_excel(excel_file, sheet_name='Ext')
            df_ext = clean_dataframe(df_ext)
            print(f"📋 Found {len(df_ext)} rows in Ext sheet")
            
            # Filter out rows with empty descriptions
            valid_rows = []
            for index, row in df_ext.iterrows():
                description = row['Description']
                if pd.notna(description) and str(description).strip() != '':
                    valid_rows.append((index, row))
            
            print(f"📋 {len(valid_rows)} rows have valid descriptions")
            
            imported_count = 0
            error_count = 0
            
            for index, row in valid_rows:
                try:
                    # Convert date to string if it's a datetime
                    date_value = row['Date']
                    if pd.notna(date_value) and hasattr(date_value, 'strftime'):
                        date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
                    
                    project_item = ProjectItem(
                        project_id=project.id,
                        user_id=user.id,
                        description=str(row['Description']),
                        quantity=float(row['Quantity']) if pd.notna(row['Quantity']) else 1.0,
                        date=date_value,
                        trade_price=float(row['Trade Price']) if pd.notna(row['Trade Price']) else None,
                        price_unit=str(row['Price Unit']) if pd.notna(row['Price Unit']) else None,
                        discount_percent=float(row['Disc %']) if pd.notna(row['Disc %']) else 0.0,
                        link_price=float(row['Link Price']) if pd.notna(row['Link Price']) else None,
                        cost_adjustment_percent=float(row['Cost Adj %']) if pd.notna(row['Cost Adj %']) else 0.0,
                        net_cost=float(row['Net Cost']) if pd.notna(row['Net Cost']) else None,
                        db_labor=float(row['DB Labor']) if pd.notna(row['DB Labor']) else None,
                        labor=float(row['Labor']) if pd.notna(row['Labor']) else None,
                        labor_unit=str(row['Labor Unit']) if pd.notna(row['Labor Unit']) else None,
                        labor_adjustment_percent=float(row['Lab Adj %']) if pd.notna(row['Lab Adj %']) else 0.0,
                        total_material=float(row['Total Material']) if pd.notna(row['Total Material']) else None,
                        total_hours=float(row['Total Hours']) if pd.notna(row['Total Hours']) else None,
                        material_condition=str(row['Material Condition']) if pd.notna(row['Material Condition']) else None,
                        labor_condition=str(row['Labor Condition']) if pd.notna(row['Labor Condition']) else None,
                        weight=float(row['Weight']) if pd.notna(row['Weight']) else None,
                        weight_unit=str(row['Weight Unit']) if pd.notna(row['Weight Unit']) else None,
                        total_weight=float(row['Total Weight']) if pd.notna(row['Total Weight']) else None,
                        manufacturer_name=str(row['Manufacturer Name']) if pd.notna(row['Manufacturer Name']) else None,
                        catalog_number=str(row['Catalog Number']) if pd.notna(row['Catalog Number']) else None,
                        price_code=str(row['Price Code']) if pd.notna(row['Price Code']) else None,
                        reference=str(row['Reference']) if pd.notna(row['Reference']) else None,
                        supplier_name=str(row['Supplier Name']) if pd.notna(row['Supplier Name']) else None,
                        supplier_code=str(row['Supplier Code']) if pd.notna(row['Supplier Code']) else None,
                        sort_code_1=str(row['Sort Code 1']) if pd.notna(row['Sort Code 1']) else None,
                        sort_code_2=str(row['Sort Code 2']) if pd.notna(row['Sort Code 2']) else None,
                        sort_code_3=str(row['Sort Code 3']) if pd.notna(row['Sort Code 3']) else None,
                        sort_code_4=str(row['Sort Code 4']) if pd.notna(row['Sort Code 4']) else None,
                        sort_code_5=str(row['Sort Code 5']) if pd.notna(row['Sort Code 5']) else None,
                        sort_code_6=str(row['Sort Code 6']) if pd.notna(row['Sort Code 6']) else None,
                        sort_code_7=str(row['Sort Code 7']) if pd.notna(row['Sort Code 7']) else None,
                        sort_code_8=str(row['Sort Code 8']) if pd.notna(row['Sort Code 8']) else None,
                        quick_takeoff_code=str(row['Quick Takeoff Code']) if pd.notna(row['Quick Takeoff Code']) else None
                    )
                    
                    db.add(project_item)
                    imported_count += 1
                    
                    # Commit every 50 records to avoid memory issues
                    if imported_count % 50 == 0:
                        db.commit()
                        print(f"  ✅ Imported {imported_count} records...")
                        
                except Exception as e:
                    error_count += 1
                    print(f"  ❌ Error importing row {index}: {e}")
                    db.rollback()
                    continue
            
            # Final commit
            db.commit()
            
            print(f"\n🎉 Import completed!")
            print(f"✅ Successfully imported: {imported_count} records")
            print(f"❌ Errors: {error_count} records")
            print(f"✅ Project ID: {project.id}")
            print(f"✅ User ID: {user.id}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during import: {e}")
            db.rollback()
            import traceback
            traceback.print_exc()
        finally:
            db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import_ext_data_simple() 