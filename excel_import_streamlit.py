#!/usr/bin/env python3
"""
Dynamic Streamlit Excel Import System with Automatic Table Mapping
"""
import streamlit as st
import pandas as pd
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
import json
import time
import io
import re

# Add src to path and load environment
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
load_dotenv()

def clean_dataframe(df):
    """Clean dataframe by removing empty rows and handling NaN values"""
    df = df.dropna(how='all')
    df = df.replace({np.nan: None})
    return df

def get_table_mapping(sheet_name):
    """Get the database table name for a given sheet name"""
    # Convert sheet name to table name format
    table_name = re.sub(r'[^a-zA-Z0-9]', '_', sheet_name.lower())
    table_name = re.sub(r'_+', '_', table_name).strip('_')
    
    # Add prefix to avoid conflicts
    table_name = f"project_{table_name}"
    
    return table_name

def extract_project_name(filename):
    """Extract project name from Excel file name"""
    # Remove file extension
    name_without_ext = os.path.splitext(filename)[0]
    
    # Remove common suffixes like "(1)", "(2)", etc.
    name_clean = re.sub(r'\s*\(\d+\)\s*$', '', name_without_ext)
    
    # Remove common words like "in Excel", "data", etc.
    name_clean = re.sub(r'\s+(in\s+)?(Excel|data|file|sheet)\s*', ' ', name_clean, flags=re.IGNORECASE)
    
    # Take the first word as project name
    project_name = name_clean.strip().split()[0] if name_clean.strip() else "Excel Import"
    
    return project_name

def create_dynamic_table_model(table_name, columns):
    """Dynamically create a SQLAlchemy model for a table"""
    from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, MetaData, Table
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.sql import func
    
    # Create a new metadata instance for each model to avoid conflicts
    metadata = MetaData()
    
    # Define reserved keywords to skip
    reserved_keywords = {
        'id', 'project_id', 'user_id', 'created_at', 'updated_at',
        'total', 'sum', 'count', 'avg', 'min', 'max', 'select', 'from', 'where',
        'order', 'group', 'by', 'having', 'join', 'left', 'right', 'inner',
        'outer', 'on', 'as', 'and', 'or', 'not', 'null', 'true', 'false',
        'index', 'key', 'primary', 'foreign', 'unique', 'check', 'default',
        'constraint', 'table', 'database', 'schema', 'view', 'procedure',
        'function', 'trigger', 'sequence', 'user', 'password', 'grant',
        'revoke', 'commit', 'rollback', 'transaction', 'lock', 'deadlock'
    }
    
    # Create table definition directly
    table_columns = [
        Column('id', Integer, primary_key=True, index=True),
        Column('project_id', Integer, ForeignKey("projects.id"), nullable=False),
        Column('user_id', Integer, ForeignKey("users.id"), nullable=False),
        Column('created_at', DateTime(timezone=True), server_default=func.now()),
        Column('updated_at', DateTime(timezone=True), onupdate=func.now())
    ]
    
    # Add columns for each Excel column
    for col in columns:
        # Clean column name
        clean_col = re.sub(r'[^a-zA-Z0-9]', '_', col.lower())
        clean_col = re.sub(r'_+', '_', clean_col).strip('_')
        
        # Handle reserved keywords by adding prefix
        if clean_col in reserved_keywords:
            clean_col = f"excel_{clean_col}"
        elif not clean_col:
            continue
            
        # Add the column as Text type to handle any data
        table_columns.append(Column(clean_col, Text))
    
    # Create the table
    table = Table(table_name, metadata, *table_columns, extend_existing=True)
    
    return table

def import_sheet_data_dynamic(sheet_name, df, project_id, user_id, db, table_name):
    """Import data from a sheet into a dynamically created table"""
    try:
        # Define reserved keywords to skip
        reserved_keywords = {
            'id', 'project_id', 'user_id', 'created_at', 'updated_at',
            'total', 'sum', 'count', 'avg', 'min', 'max', 'select', 'from', 'where',
            'order', 'group', 'by', 'having', 'join', 'left', 'right', 'inner',
            'outer', 'on', 'as', 'and', 'or', 'not', 'null', 'true', 'false',
            'index', 'key', 'primary', 'foreign', 'unique', 'check', 'default',
            'constraint', 'table', 'database', 'schema', 'view', 'procedure',
            'function', 'trigger', 'sequence', 'user', 'password', 'grant',
            'revoke', 'commit', 'rollback', 'transaction', 'lock', 'deadlock'
        }
        
        # Get valid and skipped columns for debugging
        valid_columns, skipped_columns = get_valid_columns(df.columns)
        
        # Show debugging info
       
       
        
        # Check if we have any valid columns
        if not valid_columns:
          
            return 0, len(df)
        
        # Create dynamic table for this sheet
        table = create_dynamic_table_model(table_name, df.columns)
        
        # Debug: Show table structure
        
        # Use existing table structure if table exists
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.bind)
            existing_tables = inspector.get_table_names()
           
            if table_name in existing_tables:
                
                
                # Get existing table columns
                existing_columns = []
                for column in inspector.get_columns(table_name):
                    existing_columns.append(column['name'])
                
                
                
                # Use existing table instead of creating new one
                from sqlalchemy import Table as SQLTable, MetaData
                metadata = MetaData()
                existing_table = SQLTable(table_name, metadata, autoload_with=db.bind)
                table = existing_table
                
            else:
                # Create new table only if it doesn't exist
               
                table.create(db.bind, checkfirst=True)
                
        except Exception as table_error:
            
            return 0, len(df)
        
        imported_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # Skip rows that have "Total" in their name or first column value
                skip_row = False
                
                # Check if the row index or first column contains "Total"
                if isinstance(index, str) and 'total' in str(index).lower():
                    skip_row = True
                    
                elif len(row) > 0:
                    first_value = str(row.iloc[0]).lower() if pd.notna(row.iloc[0]) else ""
                    if 'total' in first_value:
                        skip_row = True
                       
                
                if skip_row:
                    error_count += 1
                    continue
                
                # Prepare data for insertion
                data = {
                    'project_id': project_id,
                    'user_id': user_id
                }
                
                valid_data_found = False
                
                # Debug: Show first few rows being processed
                if index < 3:  # Only show first 3 rows for debugging
                    st.write(f"🔍 Processing row {index}: {list(row.head(3).values)}")
                
                # Add each column value
                for col in df.columns:
                    clean_col = re.sub(r'[^a-zA-Z0-9]', '_', col.lower())
                    clean_col = re.sub(r'_+', '_', clean_col).strip('_')
                    
                    # Handle reserved keywords by adding prefix
                    if clean_col in reserved_keywords:
                        clean_col = f"excel_{clean_col}"
                    elif not clean_col:
                        continue
                    
                    # Check if column exists in the table
                    if hasattr(table, 'columns') and clean_col in [c.name for c in table.columns]:
                        # Convert value to string
                        value = row[col]
                        if pd.notna(value):
                            data[clean_col] = str(value)
                            valid_data_found = True
                        else:
                            data[clean_col] = None
                    # else:
                    #     # Skip columns that don't exist in the table
                    #     if index < 3:  # Only show for first few rows
                    #         st.write(f"⚠️ Skipping column '{clean_col}' (not in table)")
                
                # Only insert if we have valid data columns
                if valid_data_found and len(data) > 2:  # More than just project_id and user_id
                    try:
                        db.execute(table.insert().values(**data))
                        imported_count += 1
                        # if imported_count % 10 == 0:  # Show progress every 10 rows
                        #     st.write(f"✅ Imported {imported_count} rows so far...")
                    except Exception as insert_error:
                        st.error(f"❌ Insert error on row {index}: {insert_error}")
                        error_count += 1
                        continue
                else:
                    st.write(f"⚠️ Skipping row {index} (no valid data found)")
                    error_count += 1
                    continue
                
            except Exception as e:
                error_count += 1
                continue
        
        return imported_count, error_count
        
    except Exception as e:
        st.error(f"Error creating/importing to table {table_name}: {e}")
        return 0, 0

def import_sheet_data(sheet_name, df, project_id, user_id, db):
    """Import data from a specific sheet with dynamic table mapping"""
    # Get the table name for this sheet
    table_name = get_table_mapping(sheet_name)
    
    # Use dynamic import for all sheets
    return import_sheet_data_dynamic(sheet_name, df, project_id, user_id, db, table_name)

def get_reserved_keywords():
    """Get list of reserved keywords that will be skipped"""
    return {
        'id', 'project_id', 'user_id', 'created_at', 'updated_at',
        'total', 'sum', 'count', 'avg', 'min', 'max', 'select', 'from', 'where',
        'order', 'group', 'by', 'having', 'join', 'left', 'right', 'inner',
        'outer', 'on', 'as', 'and', 'or', 'not', 'null', 'true', 'false',
        'index', 'key', 'primary', 'foreign', 'unique', 'check', 'default',
        'constraint', 'table', 'database', 'schema', 'view', 'procedure',
        'function', 'trigger', 'sequence', 'user', 'password', 'grant',
        'revoke', 'commit', 'rollback', 'transaction', 'lock', 'deadlock'
    }

def get_valid_columns(columns):
    """Get list of valid columns after filtering reserved keywords"""
    reserved_keywords = get_reserved_keywords()
    valid_columns = []
    skipped_columns = []
    
    for col in columns:
        clean_col = re.sub(r'[^a-zA-Z0-9]', '_', col.lower())
        clean_col = re.sub(r'_+', '_', clean_col).strip('_')
        
        if clean_col in reserved_keywords or not clean_col:
            # Instead of skipping, add a prefix to make it valid
            if clean_col in reserved_keywords:
                clean_col = f"excel_{clean_col}"
            skipped_columns.append(col)
            valid_columns.append(col)  # Add the original column name to valid columns
        else:
            valid_columns.append(col)
    
    return valid_columns, skipped_columns

def examine_excel_file(uploaded_file):
    """Examine the uploaded Excel file structure"""
    if uploaded_file is None:
        st.error("No file uploaded")
        return None
    
    try:
        # Read the uploaded file
        excel_file_obj = pd.ExcelFile(uploaded_file)
        sheets_info = {}
        
        for sheet_name in excel_file_obj.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            df = clean_dataframe(df)
            
            # Get the table name for this sheet
            table_name = get_table_mapping(sheet_name)
            
            # Get valid and skipped columns
            valid_columns, skipped_columns = get_valid_columns(df.columns)
            
            sheets_info[sheet_name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'valid_columns': valid_columns,
                'skipped_columns': skipped_columns,
                'sample_data': df.head(3).to_dict('records'),
                'data_types': df.dtypes.to_dict(),
                'non_null_counts': df.count().to_dict(),
                'table_name': table_name
            }
        
        return sheets_info
    except Exception as e:
        st.error(f"Error examining Excel file: {e}")
        return None

def get_db_session():
    """Get database session from session state or create new one"""
    if 'db_session' not in st.session_state:
        from src.database import SessionLocal, test_connection
        if test_connection():
            st.session_state.db_session = SessionLocal()
        else:
            st.error("Database connection failed")
            return None
    return st.session_state.db_session

def close_db_session():
    """Close database session if it exists"""
    if 'db_session' in st.session_state and st.session_state.db_session:
        try:
            st.session_state.db_session.close()
            del st.session_state.db_session
        except:
            pass

def import_excel_data(uploaded_file, selected_sheets):
    """Import Excel data from uploaded file"""
    if uploaded_file is None:
        st.error("No file uploaded")
        return None
    
    try:
        from src.models import User, Project
        
        # Get existing database session
        db = get_db_session()
        if db is None:
            return None
        
        try:
            user = db.query(User).first()
            if not user:
                st.error("No users found in database")
                return None
            
            # Extract project name from file name
            project_name = extract_project_name(uploaded_file.name)
            
            project = Project(
                name=project_name,
                description=f"Excel import from {uploaded_file.name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                    df = clean_dataframe(df)
                    imported_count, error_count = import_sheet_data(sheet_name, df, project.id, user.id, db)
                    results[sheet_name] = {
                        'imported': imported_count,
                        'errors': error_count,
                        'total_rows': len(df),
                        'table_name': get_table_mapping(sheet_name)
                    }
                    total_imported += imported_count
                    total_errors += error_count
                    db.commit()
                except Exception as e:
                    results[sheet_name] = {
                        'imported': 0,
                        'errors': 0,
                        'total_rows': 0,
                        'table_name': get_table_mapping(sheet_name),
                        'error': str(e)
                    }
                    db.rollback()
            
            return {
                'project_id': project.id,
                'user_id': user.id,
                'results': results,
                'total_imported': total_imported,
                'total_errors': total_errors,
                'filename': uploaded_file.name
            }
        
        except Exception as e:
            db.rollback()
            st.error(f"Error during import: {e}")
            return None
    
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.set_page_config(
        page_title="Dynamic Excel Import System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-card {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .upload-area {
        border: 2px dashed #007bff;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    .table-info {
        background: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dynamic Excel Import System</h1>
        <p>Upload Excel files and automatically create database tables with matching names</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Controls")
    
    # Database Connection Status
    db_session = get_db_session()
    if db_session:
        st.sidebar.success("✅ Database Connected")
        if st.sidebar.button("🔌 Close DB Connection"):
            close_db_session()
            st.sidebar.info("Database connection closed")
            st.rerun()
    else:
        st.sidebar.error("❌ Database Disconnected")
        if st.sidebar.button("🔗 Reconnect Database"):
            close_db_session()
            st.rerun()
    
    # Show reserved keywords info
    with st.sidebar.expander("🔍 Reserved Keywords (Renamed)"):
        st.write("These keywords are automatically renamed with 'excel_' prefix:")
        reserved_keywords = get_reserved_keywords()
        # Group keywords for better display
        sql_keywords = ['select', 'from', 'where', 'order', 'group', 'by', 'having', 'join', 'left', 'right', 'inner', 'outer', 'on', 'as', 'and', 'or', 'not']
        db_keywords = ['id', 'project_id', 'user_id', 'created_at', 'updated_at', 'index', 'key', 'primary', 'foreign', 'unique', 'check', 'default']
        function_keywords = ['total', 'sum', 'count', 'avg', 'min', 'max']
        other_keywords = ['null', 'true', 'false', 'constraint', 'table', 'database', 'schema', 'view', 'procedure', 'function', 'trigger', 'sequence', 'user', 'password', 'grant', 'revoke', 'commit', 'rollback', 'transaction', 'lock', 'deadlock']
        
        st.write("**SQL Keywords:**")
        st.write(", ".join(sql_keywords))
        st.write("**Database Keywords:**")
        st.write(", ".join(db_keywords))
        st.write("**Function Keywords:**")
        st.write(", ".join(function_keywords))
        st.write("**Other Keywords:**")
        st.write(", ".join(other_keywords))
    
    # Initialize session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'sheets_data' not in st.session_state:
        st.session_state.sheets_data = None
    if 'selected_sheets' not in st.session_state:
        st.session_state.selected_sheets = []
    if 'db_session' not in st.session_state:
        st.session_state.db_session = None
    
    # File Upload Section
    st.subheader("📁 Upload Excel File")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload an Excel file (.xlsx or .xls) to import data"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        
        # Extract and display project name
        project_name = extract_project_name(uploaded_file.name)
        
        # Display file info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("File Name", uploaded_file.name)
        with col2:
            st.metric("Project Name", project_name)
        with col3:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col4:
            st.metric("File Type", uploaded_file.type)
        
        # Examine Excel File Button
        if st.sidebar.button("🔍 Examine Excel File", type="primary"):
            with st.spinner("Examining Excel file..."):
                st.session_state.sheets_data = examine_excel_file(uploaded_file)
                if st.session_state.sheets_data:
                    st.success("✅ Excel file examined successfully!")
                    st.rerun()
    
    # Display sheets information
    if st.session_state.sheets_data:
        st.subheader("📋 Available Sheets & Table Mappings")
        
        # Create columns for sheet cards
        cols = st.columns(3)
        
        for i, (sheet_name, sheet_info) in enumerate(st.session_state.sheets_data.items()):
            col = cols[i % 3]
            
            with col:
                # Show warning if columns are renamed
                warning_text = ""
                if sheet_info['skipped_columns']:
                    warning_text = f"⚠️ {len(sheet_info['skipped_columns'])} columns renamed"
                
                # Add info about row skipping
                row_info = "📋 Rows with 'Total' will be skipped"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{sheet_name}</h4>
                    <p><strong>Rows:</strong> {sheet_info['shape'][0]}</p>
                    <p><strong>Columns:</strong> {len(sheet_info['valid_columns'])} valid / {sheet_info['shape'][1]} total</p>
                    <div class="table-info">
                        <strong>Table:</strong> {sheet_info['table_name']}
                    </div>
                    {f'<div style="color: #856404; background: #fff3cd; padding: 0.25rem; border-radius: 3px; margin-top: 0.5rem; font-size: 0.8em;">{warning_text}</div>' if warning_text else ''}
                    <div style="color: #0c5460; background: #d1ecf1; padding: 0.25rem; border-radius: 3px; margin-top: 0.5rem; font-size: 0.8em;">{row_info}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox for selection
                if st.checkbox(f"Select {sheet_name}", key=f"check_{sheet_name}"):
                    if sheet_name not in st.session_state.selected_sheets:
                        st.session_state.selected_sheets.append(sheet_name)
                else:
                    if sheet_name in st.session_state.selected_sheets:
                        st.session_state.selected_sheets.remove(sheet_name)
                
                # View details button
                if st.button(f"View Details", key=f"view_{sheet_name}"):
                    st.subheader(f"📊 Sheet: {sheet_name}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Table Mapping:**")
                        st.info(f"Sheet: `{sheet_name}` → Table: `{sheet_info['table_name']}`")
                    
                    with col2:
                        st.write("**Valid Columns:**")
                        for col in sheet_info['valid_columns']:
                            st.write(f"✅ {col}")
                        
                        if sheet_info['skipped_columns']:
                            st.write("**Renamed Columns (Reserved Keywords):**")
                            for col in sheet_info['skipped_columns']:
                                clean_col = re.sub(r'[^a-zA-Z0-9]', '_', col.lower())
                                clean_col = re.sub(r'_+', '_', clean_col).strip('_')
                                renamed_col = f"excel_{clean_col}"
                                st.write(f"🔄 {col} → {renamed_col}")
                    
                    with col3:
                        st.write("**Sample Data:**")
                        sample_df = pd.DataFrame(sheet_info['sample_data'])
                        st.dataframe(sample_df, use_container_width=True)
        
        # Import button
        if st.session_state.selected_sheets:
            st.subheader("🚀 Import Data")
            
            # Show project name that will be created
            project_name = extract_project_name(st.session_state.uploaded_file.name)
            st.info(f"📁 **Project Name:** {project_name}")
            
            st.write(f"Selected sheets: {', '.join(st.session_state.selected_sheets)}")
            
            # Show table mappings
            st.write("**Table Mappings:**")
            for sheet_name in st.session_state.selected_sheets:
                table_name = st.session_state.sheets_data[sheet_name]['table_name']
                st.info(f"📋 `{sheet_name}` → `{table_name}`")
            
            if st.button("📥 Import Selected Sheets", type="primary"):
                with st.spinner("Importing data..."):
                    result = import_excel_data(st.session_state.uploaded_file, st.session_state.selected_sheets)
                    
                    if result:
                        st.markdown("""
                        <div class="success-card">
                            <h3>✅ Import Completed Successfully!</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display results
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Project ID", result['project_id'])
                        
                        with col2:
                            st.metric("Total Imported", result['total_imported'])
                        
                        with col3:
                            st.metric("Total Errors", result['total_errors'])
                        
                        with col4:
                            st.metric("File", result['filename'])
                        
                        # Detailed results table
                        st.subheader("📊 Detailed Results")
                        
                        results_data = []
                        for sheet_name, sheet_result in result['results'].items():
                            status = "✅ Success" if sheet_result.get('error') is None else "❌ Error"
                            results_data.append({
                                "Sheet": sheet_name,
                                "Table": sheet_result['table_name'],
                                "Total Rows": sheet_result['total_rows'],
                                "Imported": sheet_result['imported'],
                                "Errors": sheet_result['errors'],
                                "Status": status
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Show errors if any
                        for sheet_name, sheet_result in result['results'].items():
                            if sheet_result.get('error'):
                                st.error(f"Error in {sheet_name}: {sheet_result['error']}")
        else:
            st.info("👆 Select sheets above to import data")
    
    elif st.session_state.uploaded_file is None:
        st.info("👆 Upload an Excel file above to get started")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Dynamic Excel Import System - Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 