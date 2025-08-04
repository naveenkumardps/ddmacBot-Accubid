#!/usr/bin/env python3
"""
Web Interface for Excel Import System
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import pandas as pd
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
import json

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def clean_dataframe(df):
    """Clean dataframe by removing empty rows and handling NaN values"""
    # Remove rows where all values are NaN
    df = df.dropna(how='all')
    
    # Replace NaN with None for database compatibility
    df = df.replace({np.nan: None})
    
    return df

def import_sheet_data(sheet_name, df, project_id, user_id, db):
    """Import data from a specific sheet"""
    from src.models import ProjectItem, ProjectDirlib, ProjectInclb, ProjectLbfac, ProjectIndlb
    
    imported_count = 0
    error_count = 0
    
    if sheet_name == 'Ext':
        # Filter out rows with empty descriptions
        valid_rows = []
        for index, row in df.iterrows():
            description = row['Description']
            if pd.notna(description) and str(description).strip() != '':
                valid_rows.append((index, row))
        
        for index, row in valid_rows:
            try:
                # Convert date to string if it's a datetime
                date_value = row['Date']
                if pd.notna(date_value) and hasattr(date_value, 'strftime'):
                    date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
                
                project_item = ProjectItem(
                    project_id=project_id,
                    user_id=user_id,
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
                
            except Exception as e:
                error_count += 1
                continue
    
    elif sheet_name == 'DirLb':
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
                error_count += 1
                continue
    
    elif sheet_name == 'IncLb':
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
                error_count += 1
                continue
    
    elif sheet_name == 'LbFac':
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
                error_count += 1
                continue
    
    elif sheet_name == 'LbEsc':
        for index, row in df.iterrows():
            try:
                if pd.isna(row['Escalation Period']) or str(row['Escalation Period']).strip() == '':
                    continue
                    
                lbesc_item = ProjectLbfac(  # Using same model since table is project_lbesc
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
                error_count += 1
                continue
    
    elif sheet_name == 'IndLb':
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
                error_count += 1
                continue
    
    return imported_count, error_count

@app.route('/')
def index():
    return render_template('excel_import.html')

@app.route('/examine_excel', methods=['POST'])
def examine_excel():
    """Examine the Excel file structure"""
    try:
        excel_file = r"C:\Users\navee\Downloads\Schlegel Accubid in Excel (1).xlsx"
        
        if not os.path.exists(excel_file):
            return jsonify({'error': 'Excel file not found'})
        
        # Read all sheets
        excel_file_obj = pd.ExcelFile(excel_file)
        sheets_info = {}
        
        for sheet_name in excel_file_obj.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            df = clean_dataframe(df)
            
            sheets_info[sheet_name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'sample_data': df.head(3).to_dict('records'),
                'data_types': df.dtypes.to_dict(),
                'non_null_counts': df.count().to_dict()
            }
        
        return jsonify({
            'success': True,
            'sheets': sheets_info,
            'total_sheets': len(excel_file_obj.sheet_names)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/import_excel', methods=['POST'])
def import_excel():
    """Import Excel data"""
    try:
        data = request.get_json()
        selected_sheets = data.get('sheets', [])
        
        if not selected_sheets:
            return jsonify({'error': 'No sheets selected'})
        
        excel_file = r"C:\Users\navee\Downloads\Schlegel Accubid in Excel (1).xlsx"
        
        if not os.path.exists(excel_file):
            return jsonify({'error': 'Excel file not found'})
        
        from src.database import SessionLocal, test_connection, DB_TYPE
        from src.models import User, Project
        
        # Test connection
        if not test_connection():
            return jsonify({'error': 'Database connection failed'})
        
        db = SessionLocal()
        try:
            # Get user
            user = db.query(User).first()
            if not user:
                return jsonify({'error': 'No users found in database'})
            
            # Create project
            project = Project(
                name=f"Schlegel Accubid Import - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                description=f"Excel import from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                status="active"
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            
            results = {}
            total_imported = 0
            total_errors = 0
            
            for sheet_name in selected_sheets:
                try:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    df = clean_dataframe(df)
                    
                    imported_count, error_count = import_sheet_data(sheet_name, df, project.id, user.id, db)
                    
                    results[sheet_name] = {
                        'imported': imported_count,
                        'errors': error_count,
                        'total_rows': len(df)
                    }
                    
                    total_imported += imported_count
                    total_errors += error_count
                    
                    # Commit after each sheet
                    db.commit()
                    
                except Exception as e:
                    results[sheet_name] = {
                        'imported': 0,
                        'errors': 0,
                        'total_rows': 0,
                        'error': str(e)
                    }
                    db.rollback()
            
            return jsonify({
                'success': True,
                'project_id': project.id,
                'user_id': user.id,
                'results': results,
                'total_imported': total_imported,
                'total_errors': total_errors
            })
            
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)})
        finally:
            db.close()
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 