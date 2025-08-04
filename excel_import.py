#!/usr/bin/env python3
"""
Excel Import System for Schlegel Accubid Data
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

def import_ext_data(df, db, project_id, user_id):
    """Import Ext (project_ext) data"""
    print(f"📊 Importing {len(df)} Ext records...")
    
    from src.models import ProjectItem
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            # Convert date to string if it's a datetime
            date_value = row['Date']
            if pd.notna(date_value) and hasattr(date_value, 'strftime'):
                date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
            
            # Skip rows with completely empty descriptions
            description = str(row['Description']) if pd.notna(row['Description']) else None
            if not description or description.strip() == '':
                continue
                
            project_item = ProjectItem(
                project_id=project_id,
                user_id=user_id,
                description=description,
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
            
            # Commit every 100 records to avoid memory issues
            if imported_count % 100 == 0:
                db.commit()
                # print(f"  ✅ Imported {imported_count} records...")
                
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} Ext records")
    return imported_count

def import_dirlib_data(df, db, project_id, user_id):
    """Import DirLb (project_dirlib) data"""
    print(f"📊 Importing {len(df)} DirLb records...")
    
    from src.models import ProjectDirlib
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            if pd.isna(row['Labor Type']) or str(row['Labor Type']).strip() == '':
                continue
                
            dirlib_item = ProjectDirlib(
                project_id=project_id,
                user_id=user_id,
                labor_type=str(row['Labor Type']) if pd.notna(row['Labor Type']) else None,
                crew=str(row['Crew']) if pd.notna(row['Crew']) else None,
                hours=str(row['Hours']) if pd.notna(row['Hours']) else None,
                rate=str(row['Rate $']) if pd.notna(row['Rate $']) else None,
                sub_total=str(row['SubTotal']) if pd.notna(row['SubTotal']) else None,
                brdn=str(row['Brdn %']) if pd.notna(row['Brdn %']) else None,
                frng=str(row['Frng $']) if pd.notna(row['Frng $']) else None,
                brdn_total=str(row['Brdn Tot.']) if pd.notna(row['Brdn Tot.']) else None,
                frng_total=str(row['Frng Tot.']) if pd.notna(row['Frng Tot.']) else None,
                total=str(row['Total']) if pd.notna(row['Total']) else None,
                full_rate=str(row['Full Rate']) if pd.notna(row['Full Rate']) else None,
                code=str(row['Code']) if pd.notna(row['Code']) else None,
                type=str(row['Type']) if pd.notna(row['Type']) else None
            )
            
            db.add(dirlib_item)
            imported_count += 1
            
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} DirLb records")
    return imported_count

def import_inclb_data(df, db, project_id, user_id):
    """Import IncLb (project_inclb) data"""
    print(f"📊 Importing {len(df)} IncLb records...")
    
    from src.models import ProjectInclb
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            if pd.isna(row['Incidental Labor']) or str(row['Incidental Labor']).strip() == '':
                continue
                
            inclb_item = ProjectInclb(
                project_id=project_id,
                user_id=user_id,
                incidental_labor=str(row['Incidental Labor']) if pd.notna(row['Incidental Labor']) else None,
                hours=str(row['Hours']) if pd.notna(row['Hours']) else None,
                rate=str(row['Rate $']) if pd.notna(row['Rate $']) else None,
                sub_total=str(row['SubTotal']) if pd.notna(row['SubTotal']) else None,
                brdn=str(row['Brdn %']) if pd.notna(row['Brdn %']) else None,
                frng=str(row['Frng $']) if pd.notna(row['Frng $']) else None,
                brdn_total=str(row['Brdn Tot.']) if pd.notna(row['Brdn Tot.']) else None,
                frng_total=str(row['Frng Tot.']) if pd.notna(row['Frng Tot.']) else None,
                total=str(row['Total']) if pd.notna(row['Total']) else None,
                full_rate=str(row['Full Rate']) if pd.notna(row['Full Rate']) else None,
                code=str(row['Code']) if pd.notna(row['Code']) else None,
                type=str(row['Type']) if pd.notna(row['Type']) else None
            )
            
            db.add(inclb_item)
            imported_count += 1
            
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} IncLb records")
    return imported_count

def import_lbfac_data(df, db, project_id, user_id):
    """Import LbFac (project_lbfac) data"""
    print(f"📊 Importing {len(df)} LbFac records...")
    
    from src.models import ProjectLbfac
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            if pd.isna(row['Labor Factoring']) or str(row['Labor Factoring']).strip() == '':
                continue
                
            lbfac_item = ProjectLbfac(
                project_id=project_id,
                user_id=user_id,
                labor_factoring=str(row['Labor Factoring']) if pd.notna(row['Labor Factoring']) else None,
                factor=str(row['Factor']) if pd.notna(row['Factor']) else None,
                percent_of_direct_hrs=str(row['% of Direct Hrs']) if pd.notna(row['% of Direct Hrs']) else None,
                hours=str(row['Hours']) if pd.notna(row['Hours']) else None,
                rate=str(row['Rate $']) if pd.notna(row['Rate $']) else None,
                sub_total=str(row['SubTotal']) if pd.notna(row['SubTotal']) else None,
                brdn_percent=str(row['Brdn %']) if pd.notna(row['Brdn %']) else None,
                frng=str(row['Frng $']) if pd.notna(row['Frng $']) else None,
                brdn_total=str(row['Brdn Tot.']) if pd.notna(row['Brdn Tot.']) else None,
                frng_total=str(row['Frng Tot.']) if pd.notna(row['Frng Tot.']) else None,
                total=str(row['Total']) if pd.notna(row['Total']) else None,
                full_rate=str(row['Full Rate']) if pd.notna(row['Full Rate']) else None,
                code=str(row['Code']) if pd.notna(row['Code']) else None,
                type=str(row['Type']) if pd.notna(row['Type']) else None
            )
            
            db.add(lbfac_item)
            imported_count += 1
            
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} LbFac records")
    return imported_count

def import_lbesc_data(df, db, project_id, user_id):
    """Import LbEsc (project_lbesc) data"""
    print(f"📊 Importing {len(df)} LbEsc records...")
    
    from src.models import ProjectLbfac  # Using the same model since table is project_lbesc
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            if pd.isna(row['Escalation Period']) or str(row['Escalation Period']).strip() == '':
                continue
                
            lbesc_item = ProjectLbfac(
                project_id=project_id,
                user_id=user_id,
                escalation_period=str(row['Escalation Period']) if pd.notna(row['Escalation Period']) else None,
                description=str(row['Description']) if pd.notna(row['Description']) else None,
                percent_of_contract=str(row['% of Contract']) if pd.notna(row['% of Contract']) else None,
                labor_hours=str(row['Labor Hours']) if pd.notna(row['Labor Hours']) else None,
                escalation_percent=str(row['Escalation %']) if pd.notna(row['Escalation %']) else None,
                escalation_amount=str(row['Escalation $']) if pd.notna(row['Escalation $']) else None,
                financing_percent=str(row['Financing %']) if pd.notna(row['Financing %']) else None,
                total=str(row['Total']) if pd.notna(row['Total']) else None,
                code=str(row['Code']) if pd.notna(row['Code']) else None,
                type=str(row['Type']) if pd.notna(row['Type']) else None
            )
            
            db.add(lbesc_item)
            imported_count += 1
            
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} LbEsc records")
    return imported_count

def import_indlb_data(df, db, project_id, user_id):
    """Import IndLb (project_indlb) data"""
    print(f"📊 Importing {len(df)} IndLb records...")
    
    from src.models import ProjectIndlb
    
    imported_count = 0
    for index, row in df.iterrows():
        try:
            if pd.isna(row['Indirect Labor']) or str(row['Indirect Labor']).strip() == '':
                continue
                
            indlb_item = ProjectIndlb(
                project_id=project_id,
                user_id=user_id,
                indirect_labor=str(row['Indirect Labor']) if pd.notna(row['Indirect Labor']) else None,
                labor_percent=str(row['Lab %']) if pd.notna(row['Lab %']) else None,
                hours=str(row['Hours']) if pd.notna(row['Hours']) else None,
                rate=str(row['Rate $']) if pd.notna(row['Rate $']) else None,
                sub_total=str(row['SubTotal']) if pd.notna(row['SubTotal']) else None,
                brdn=str(row['Brdn %']) if pd.notna(row['Brdn %']) else None,
                frng=str(row['Frng $']) if pd.notna(row['Frng $']) else None,
                brdn_total=str(row['Brdn Tot.']) if pd.notna(row['Brdn Tot.']) else None,
                frng_total=str(row['Frng Tot.']) if pd.notna(row['Frng Tot.']) else None,
                total=str(row['Total']) if pd.notna(row['Total']) else None,
                full_rate=str(row['Full Rate']) if pd.notna(row['Full Rate']) else None,
                code=str(row['Code']) if pd.notna(row['Code']) else None,
                type=str(row['Type']) if pd.notna(row['Type']) else None
            )
            
            db.add(indlb_item)
            imported_count += 1
            
        except Exception as e:
            print(f"  ❌ Error importing row {index}: {e}")
            continue
    
    db.commit()
    print(f"  ✅ Successfully imported {imported_count} IndLb records")
    return imported_count

def import_excel_data():
    """Main function to import Excel data"""
    
    excel_file = r"C:\Users\navee\Downloads\Schlegel Accubid in Excel (1).xlsx"
    
    print("📊 Excel Import System")
    print("=" * 50)
    print(f"File: {excel_file}")
    
    try:
        from src.database import SessionLocal, test_connection, DB_TYPE
        from src.models import User, Project
        
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
                name="Schlegel Accubid Import",
                description=f"Excel import from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                status="active"
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            
            print(f"✅ Created project: {project.name} (ID: {project.id})")
            
            # Import data from each sheet
            total_imported = 0
            
            # 1. Import Ext data
            try:
                df_ext = pd.read_excel(excel_file, sheet_name='Ext')
                df_ext = clean_dataframe(df_ext)
                count = import_ext_data(df_ext, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing Ext data: {e}")
            
            # 2. Import DirLb data
            try:
                df_dirlib = pd.read_excel(excel_file, sheet_name='DirLb')
                df_dirlib = clean_dataframe(df_dirlib)
                count = import_dirlib_data(df_dirlib, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing DirLb data: {e}")
            
            # 3. Import IncLb data
            try:
                df_inclb = pd.read_excel(excel_file, sheet_name='IncLb')
                df_inclb = clean_dataframe(df_inclb)
                count = import_inclb_data(df_inclb, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing IncLb data: {e}")
            
            # 4. Import LbFac data
            try:
                df_lbfac = pd.read_excel(excel_file, sheet_name='LbFac')
                df_lbfac = clean_dataframe(df_lbfac)
                count = import_lbfac_data(df_lbfac, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing LbFac data: {e}")
            
            # 5. Import LbEsc data
            try:
                df_lbesc = pd.read_excel(excel_file, sheet_name='LbEsc')
                df_lbesc = clean_dataframe(df_lbesc)
                count = import_lbesc_data(df_lbesc, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing LbEsc data: {e}")
            
            # 6. Import IndLb data
            try:
                df_indlb = pd.read_excel(excel_file, sheet_name='IndLb')
                df_indlb = clean_dataframe(df_indlb)
                count = import_indlb_data(df_indlb, db, project.id, user.id)
                total_imported += count
            except Exception as e:
                print(f"❌ Error importing IndLb data: {e}")
            
            print(f"\n🎉 Import completed successfully!")
            print(f"✅ Total records imported: {total_imported}")
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
    import_excel_data() 