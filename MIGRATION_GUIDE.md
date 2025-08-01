# Database Migration System - Complete Setup Guide

## What Was Created

I've successfully set up a complete database migration system for your Streamlit application using SQLAlchemy and Alembic. Here's what was implemented:

### 1. Database Configuration (`src/database.py`)
- SQLAlchemy engine setup with support for multiple database types
- Session management with dependency injection
- Environment variable support for database URL

### 2. Database Models (`src/models.py`)
- **User Model**: id, username, email, full_name, role, is_active, created_at, updated_at
- **Project Model**: id, name, description, status, created_at, updated_at
- Proper indexing and constraints

### 3. Migration System
- **Alembic Configuration** (`alembic.ini`): Configured for SQLite with proper settings
- **Migration Environment** (`migrations/env.py`): Set up to work with your models
- **Migration Template** (`migrations/script.py.mako`): Template for generating migrations
- **Migration Management Script** (`manage_migrations.py`): Easy-to-use wrapper for common operations

### 4. Generated Migrations
- **Initial Migration** (`61aec3747f55_initial_migration.py`): Creates users and projects tables
- **Role Field Migration** (`136fbc07d6ce_add_role_field_to_users_table.py`): Adds role field to users table

### 5. Updated Application (`src/app.py`)
- Enhanced Streamlit app with database integration
- User and project management forms
- Real-time data display
- Migration information in sidebar

## Current Migration Status

```
Current migration version: 136fbc07d6ce (head)
```

This means all migrations have been applied and your database is up to date.

## How to Use the Migration System

### Basic Commands

```bash
# Create a new migration
python manage_migrations.py create "Description of changes"

# Apply all pending migrations
python manage_migrations.py upgrade

# Revert the last migration
python manage_migrations.py downgrade

# Check current migration version
python manage_migrations.py current

# View migration history
python manage_migrations.py history

# Check migration status
python manage_migrations.py status
```

### Workflow Example

1. **Make changes to your models** in `src/models.py`
2. **Create a migration**:
   ```bash
   python manage_migrations.py create "Add new field to users"
   ```
3. **Review the generated migration** in `migrations/versions/`
4. **Apply the migration**:
   ```bash
   python manage_migrations.py upgrade
   ```

### Adding New Models

1. **Define the model** in `src/models.py`:
   ```python
   class NewModel(Base):
       __tablename__ = "new_models"
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False)
   ```

2. **Create and apply migration**:
   ```bash
   python manage_migrations.py create "Add new model"
   python manage_migrations.py upgrade
   ```

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique, Required)
- `email` (Unique, Required)
- `full_name` (Optional)
- `role` (Default: "user")
- `is_active` (Default: True)
- `created_at` (Auto-generated)
- `updated_at` (Auto-updated)

### Projects Table
- `id` (Primary Key)
- `name` (Required)
- `description` (Optional)
- `status` (Default: "active")
- `created_at` (Auto-generated)
- `updated_at` (Auto-updated)

## Running the Application

```bash
streamlit run src/app.py
```

The app will be available at `http://localhost:8501` and includes:
- User management forms
- Project management forms
- Real-time data display
- Migration information

## Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key_here
API_URL=your_api_url_here
DATABASE_URL=sqlite:///./app.db
```

## Supported Databases

- **SQLite** (default): `sqlite:///./app.db`
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql://user:password@localhost/dbname`

## Best Practices

1. **Always create migrations** for schema changes
2. **Use descriptive migration messages**
3. **Test both upgrade and downgrade** operations
4. **Backup before major changes** in production
5. **Review generated migrations** before applying

## Troubleshooting

### Common Issues

1. **"Target database is not up to date"**: Apply pending migrations first
2. **"Table already exists"**: Use `alembic stamp head` to mark as applied
3. **Import errors**: Ensure all dependencies are installed
4. **Permission errors**: Check file permissions

### Reset Database

To completely reset:

```bash
# Delete database and migrations
rm app.db
rm -rf migrations/versions/*

# Recreate initial migration
python manage_migrations.py create "Initial migration"
python manage_migrations.py upgrade
```

## Next Steps

1. **Test the application** by adding users and projects
2. **Create additional models** as needed
3. **Add more complex relationships** between models
4. **Implement data validation** and business logic
5. **Add authentication** and authorization

Your migration system is now fully functional and ready for development! 