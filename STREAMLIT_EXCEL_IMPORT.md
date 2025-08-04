# Dynamic Streamlit Excel Import System

## Overview

The Dynamic Streamlit Excel Import System provides a modern, user-friendly web interface for uploading and importing Excel data into your database. This system allows users to dynamically upload any Excel file and automatically process it according to the available sheets.

## Features

- **Dynamic File Upload**: Upload any Excel file (.xlsx or .xls) through the web interface
- **Automatic Sheet Detection**: Automatically detects and analyzes all sheets in the uploaded file
- **Modern UI**: Clean, responsive interface with Streamlit components
- **Excel File Examination**: Preview sheet structure, columns, and sample data
- **Selective Import**: Choose which sheets to import from the uploaded file
- **Real-time Progress**: Live feedback during import operations
- **Detailed Results**: Comprehensive import statistics and error reporting
- **Database Integration**: Seamless connection to your configured database
- **File Information Display**: Shows file name, size, and type

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App

```bash
streamlit run excel_import_streamlit.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Step 1: Upload Excel File

1. **Upload File**: Use the file uploader to select and upload your Excel file
2. **File Validation**: The system automatically validates the file format (.xlsx or .xls)
3. **File Information**: View file details including name, size, and type

### Step 2: Examine Excel File

1. Click the **"🔍 Examine Excel File"** button in the sidebar
2. The system will analyze the uploaded Excel file structure
3. View available sheets with their row/column counts

### Step 3: Select Sheets

1. Review the sheet information displayed in cards
2. Use checkboxes to select which sheets you want to import
3. Click **"View Details"** to see column names and sample data

### Step 4: Import Data

1. Click the **"📥 Import Selected Sheets"** button
2. Monitor the progress with the spinner
3. View detailed results including:
   - Project ID created
   - Total records imported
   - Error count
   - Per-sheet breakdown
   - Original filename

## Interface Components

### Header
- Beautiful gradient header with title and description
- Dynamic system that works with any Excel file

### File Upload Area
- Drag-and-drop or click-to-upload interface
- File type validation (.xlsx, .xls)
- File information display (name, size, type)

### Sidebar
- Control panel with main action buttons
- Clean, organized layout

### Main Area
- **File Information**: Display uploaded file details
- **Sheet Cards**: Visual representation of each Excel sheet
- **Selection Interface**: Checkboxes for sheet selection
- **Results Display**: Comprehensive import statistics
- **Error Reporting**: Detailed error messages for troubleshooting

## Database Tables Supported

The system automatically maps Excel sheets to database tables based on sheet names:

| Excel Sheet | Database Table | Description |
|-------------|----------------|-------------|
| `Ext` | `project_ext` | Project items with detailed specifications |
| `DirLb` | `project_dirlib` | Direct labor information |
| `IncLb` | `project_inclb` | Incidental labor data |
| `LbFac` | `project_lbfac` | Labor factoring details |
| `LbEsc` | `project_lbfac` | Labor escalation information |
| `IndLb` | `project_indlb` | Indirect labor data |

## Configuration

### File Upload Settings
- **Supported Formats**: .xlsx, .xls
- **File Size**: Limited by Streamlit's default settings (200MB)
- **Validation**: Automatic format checking

### Database Configuration
The system uses the same database configuration as your main application:
- Reads from `.env` file
- Supports SQLite, MySQL, PostgreSQL, and Supabase
- Automatically connects using your configured database type

## Error Handling

The system provides comprehensive error handling:

- **File Upload Errors**: Clear error messages for invalid file types
- **File Not Found**: Validation of uploaded file existence
- **Database Connection**: Validation of database connectivity
- **Import Errors**: Per-row error tracking and reporting
- **Data Validation**: Automatic handling of null/empty values
- **Sheet Processing**: Individual sheet error handling

## Performance Features

- **Streaming Upload**: Efficient file handling without saving to disk
- **Batch Processing**: Efficient handling of large datasets
- **Progress Indicators**: Real-time feedback during operations
- **Memory Management**: Optimized data processing
- **Error Recovery**: Continues processing even if individual rows fail

## Customization

### Styling
The app includes custom CSS for:
- Gradient headers
- Metric cards
- Success/error states
- Upload area styling
- Responsive layout

### Data Processing
- Custom data cleaning functions
- Type conversion handling
- Null value management
- Dynamic sheet mapping

## Troubleshooting

### Common Issues

1. **File Upload Failed**
   - Verify the file is in .xlsx or .xls format
   - Check file size (should be under 200MB)
   - Ensure the file is not corrupted

2. **Database Connection Failed**
   - Check your `.env` configuration
   - Verify database server is running
   - Test connection with `test_db_connection.py`

3. **Import Errors**
   - Check data types in Excel file
   - Verify required columns are present
   - Review error messages for specific issues

4. **Sheet Mapping Issues**
   - Ensure sheet names match expected table names
   - Check column headers match expected field names
   - Verify data format in Excel sheets

### Debug Mode

To run in debug mode:
```bash
streamlit run excel_import_streamlit.py --logger.level debug
```

## Comparison with Previous Version

| Feature | Dynamic Upload | Hardcoded Path |
|---------|----------------|----------------|
| File Selection | User uploads any file | Fixed file path |
| Flexibility | Works with any Excel file | Limited to specific file |
| User Experience | Interactive upload | Requires file placement |
| Deployment | Works anywhere | Requires specific file location |
| Scalability | Multiple users, multiple files | Single file only |

## Advanced Features

### Automatic Sheet Detection
- Detects all sheets in uploaded Excel files
- Provides sheet information (rows, columns)
- Shows sample data for verification

### Smart Data Mapping
- Automatically maps Excel columns to database fields
- Handles data type conversions
- Manages null values appropriately

### Project Tracking
- Creates unique projects for each import
- Tracks import metadata (filename, timestamp)
- Links imported data to specific projects

## Next Steps

1. **Test the Interface**: Run the app and test with various Excel files
2. **Import Data**: Start with a single sheet to verify functionality
3. **Monitor Results**: Check the database for imported data
4. **Scale Up**: Import additional sheets as needed
5. **Customize**: Modify sheet-to-table mappings if needed

## Support

For issues or questions:
1. Check the error messages in the Streamlit interface
2. Review the database connection status
3. Verify Excel file format and content
4. Check the console output for detailed error information
5. Ensure sheet names match expected table names

---

**Note**: This dynamic version provides much more flexibility than the previous hardcoded version, allowing users to upload any Excel file and automatically process it according to the available sheets and database schema. 