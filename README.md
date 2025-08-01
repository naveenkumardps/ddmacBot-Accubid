# Database Migration Demo App

This is a Streamlit application that demonstrates how to use database migrations with SQLAlchemy and Alembic.

## Project Structure

```
ddmacBot-Accubid/
├── src/
│   ├── app.py           # Main Streamlit application
│   ├── database.py      # Database configuration
│   └── models.py        # SQLAlchemy models
├── migrations/          # Alembic migration files
│   ├── versions/        # Migration version files
│   ├── env.py           # Alembic environment configuration
│   └── script.py.mako   # Migration template
├── alembic.ini          # Alembic configuration
├── manage_migrations.py # Migration management script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Features

- **Database Migrations**: Uses Alembic for managing database schema changes
- **User Management**: Add and view users with username, email, and status
- **Project Management**: Add and view projects with name, description, and status
- **Real-time Data Display**: View current data in the database
- **Migration Management**: Easy-to-use script for managing migrations

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ddmacBot-Accubid
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (optional):
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your_secret_key_here
   API_URL=your_api_url_here
   DATABASE_URL=sqlite:///./app.db
   ```

## Database Setup

### Initial Setup

1. **Apply the initial migration**:
   ```bash
   python manage_migrations.py upgrade
   ```
   This will create the database tables based on your models.

### Managing Migrations

The project includes a convenient script for managing migrations:

```bash
# Create a new migration
python manage_migrations.py create "Add new table"

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

### Manual Alembic Commands

You can also use Alembic commands directly:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Revert migrations
alembic downgrade -1

# Check current version
alembic current
```

## Running the App

Start the Streamlit application:

```bash
streamlit run src/app.py
```

The app will be available at `http://localhost:8501`.

## Database Models

### User Model
- `id`: Primary key
- `username`: Unique username (required)
- `email`: Unique email address (required)
- `full_name`: Full name (optional)
- `is_active`: Active status (default: True)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Project Model
- `id`: Primary key
- `name`: Project name (required)
- `description`: Project description (optional)
- `status`: Project status (active, completed, on-hold)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Adding New Models

1. **Define the model** in `src/models.py`:
   ```python
   class NewModel(Base):
       __tablename__ = "new_models"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False)
       # Add other fields as needed
   ```

2. **Create a migration**:
   ```bash
   python manage_migrations.py create "Add new model"
   ```

3. **Apply the migration**:
   ```bash
   python manage_migrations.py upgrade
   ```

## Database Configuration

The app supports multiple database backends:

- **SQLite** (default): `sqlite:///./app.db`
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql://user:password@localhost/dbname`

Set the `DATABASE_URL` environment variable to change the database.

## Migration Best Practices

1. **Always create migrations for schema changes**: Don't modify the database directly
2. **Use descriptive migration messages**: Make it clear what the migration does
3. **Test migrations**: Always test both upgrade and downgrade operations
4. **Backup before major changes**: Create a backup before applying migrations in production
5. **Review generated migrations**: Check the generated migration files before applying them

## Troubleshooting

### Common Issues

1. **Migration not found**: Make sure you're in the correct directory and the migration file exists
2. **Database connection errors**: Check your `DATABASE_URL` environment variable
3. **Import errors**: Ensure all required packages are installed
4. **Permission errors**: Make sure you have write permissions in the project directory

### Reset Database

To completely reset the database:

1. Delete the database file: `rm app.db` (SQLite)
2. Delete all migration files in `migrations/versions/`
3. Recreate the initial migration: `python manage_migrations.py create "Initial migration"`
4. Apply the migration: `python manage_migrations.py upgrade`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Create migrations for any database changes
5. Test your changes
6. Submit a pull request

## License

This project is licensed under the MIT License.