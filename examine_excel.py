#!/usr/bin/env python3
"""
Examine Excel file structure for import
"""

import pandas as pd
import sys
import os
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def examine_excel_file():
    """Examine the Excel file structure"""
    
    excel_file = r"C:\Users\navee\Downloads\Schlegel Accubid in Excel (1).xlsx"
    
    print("🔍 Examining Excel File Structure")
    print("=" * 50)
    print(f"File: {excel_file}")
    
    try:
        # Read all sheets
        excel_file_obj = pd.ExcelFile(excel_file)
        print(f"\n📋 Sheets found: {excel_file_obj.sheet_names}")
        
        for sheet_name in excel_file_obj.sheet_names:
            print(f"\n📊 Sheet: {sheet_name}")
            print("-" * 30)
            
            # Read the sheet
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            print(f"Shape: {df.shape} (rows, columns)")
            print(f"Columns: {list(df.columns)}")
            
            # Show first few rows
            print("\nFirst 3 rows:")
            print(df.head(3).to_string())
            
            # Show data types
            print(f"\nData types:")
            print(df.dtypes.to_string())
            
            # Show non-null counts
            print(f"\nNon-null counts:")
            print(df.count().to_string())
            
            print("\n" + "="*50)
            
    except Exception as e:
        print(f"❌ Error examining Excel file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    examine_excel_file() 