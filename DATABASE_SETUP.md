# Database Setup Guide

This guide explains how to configure your database connection for different database types.

## Supported Database Types

- **SQLite** (default) - File-based database, no setup required
- **MySQL** - Popular open-source database
- **PostgreSQL** - Advanced open-source database
- **Supabase** - PostgreSQL-based cloud database

## Quick Setup

1. **Copy the environment template**:
   ```bash
   cp env.example .env
   ```

2. **Edit your `.env` file** with your database configuration (see examples below)

3. **Test your connection**:
   ```bash
   python test_db_connection.py
   ```

4. **Run migrations**:
   ```bash
   python manage_migrations.py upgrade
   ```

## Database Configuration Examples

### SQLite (Default)
```env
DB_TYPE=sqlite
DATABASE_URL=sqlite:///./app.db
```

### MySQL
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ddmacbot
DB_USER=your_username
DB_PASSWORD=your_password
```

### PostgreSQL
```env
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ddmacbot
DB_USER=your_username
DB_PASSWORD=your_password
DB_SSL_MODE=prefer
```

### Supabase
```env
DB_TYPE=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

## Installation Requirements

### For MySQL
```bash
pip install pymysql cryptography
```

### For PostgreSQL
```bash
pip install psycopg2-binary
```

### For Supabase
```bash
pip install psycopg2-binary
```

## Database Setup Instructions

### MySQL Setup

1. **Install MySQL Server**:
   - Windows: Download from MySQL website
   - macOS: `brew install mysql`
   - Ubuntu: `sudo apt install mysql-server`

2. **Start MySQL Service**:
   ```bash
   # Windows
   net start mysql
   
   # macOS
   brew services start mysql
   
   # Ubuntu
   sudo systemctl start mysql
   ```

3. **Create Database and User**:
   ```sql
   CREATE DATABASE ddmacbot;
   CREATE USER 'ddmacbot_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON ddmacbot.* TO 'ddmacbot_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Configure .env**:
   ```env
   DB_TYPE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ddmacbot
   DB_USER=ddmacbot_user
   DB_PASSWORD=your_password
   ```

### PostgreSQL Setup

1. **Install PostgreSQL**:
   - Windows: Download from PostgreSQL website
   - macOS: `brew install postgresql`
   - Ubuntu: `sudo apt install postgresql postgresql-contrib`

2. **Start PostgreSQL Service**:
   ```bash
   # Windows
   net start postgresql
   
   # macOS
   brew services start postgresql
   
   # Ubuntu
   sudo systemctl start postgresql
   ```

3. **Create Database and User**:
   ```sql
   CREATE DATABASE ddmacbot;
   CREATE USER ddmacbot_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE ddmacbot TO ddmacbot_user;
   ```

4. **Configure .env**:
   ```env
   DB_TYPE=postgresql
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ddmacbot
   DB_USER=ddmacbot_user
   DB_PASSWORD=your_password
   ```

### Supabase Setup

1. **Create Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Wait for the project to be ready

2. **Get Connection Details**:
   - Go to Settings > Database
   - Copy the connection string or individual values

3. **Configure .env**:
   ```env
   DB_TYPE=supabase
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   ```

## Testing Your Setup

### Test Database Connection
```bash
python test_db_connection.py
```

### Test Migration System
```bash
# Test connection before migrations
python manage_migrations.py test

# Create a test migration
python manage_migrations.py create "Test migration"

# Apply migrations
python manage_migrations.py upgrade

# Check status
python manage_migrations.py status
```

## Troubleshooting

### Common Issues

1. **Connection Refused**:
   - Ensure the database server is running
   - Check if the port is correct
   - Verify firewall settings

2. **Authentication Failed**:
   - Double-check username and password
   - Ensure the user has proper permissions
   - For MySQL, check if the user can connect from your host

3. **Database Not Found**:
   - Create the database first
   - Check the database name spelling

4. **SSL Issues (PostgreSQL/Supabase)**:
   - Try different SSL modes: `prefer`, `require`, `disable`
   - For local development, you can use `disable`

### MySQL Specific Issues

- **Access Denied**: Make sure the user has proper privileges
- **Connection Timeout**: Check if MySQL is running on the correct port
- **Character Set Issues**: Add `?charset=utf8mb4` to the connection URL

### PostgreSQL Specific Issues

- **Peer Authentication**: Edit `pg_hba.conf` to allow password authentication
- **Connection Limit**: Check `max_connections` in `postgresql.conf`
- **SSL Issues**: For local development, you can disable SSL

### Supabase Specific Issues

- **Connection Timeout**: Check if your Supabase project is active
- **SSL Required**: Supabase requires SSL, ensure `sslmode=require`
- **Rate Limiting**: Check your Supabase plan limits

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_TYPE` | Database type (sqlite, mysql, postgresql, supabase) | sqlite |
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | (auto-detected) |
| `DB_NAME` | Database name | ddmacbot |
| `DB_USER` | Database username | - |
| `DB_PASSWORD` | Database password | - |
| `DB_SSL_MODE` | SSL mode for PostgreSQL | prefer |
| `SUPABASE_URL` | Supabase project URL | - |
| `SUPABASE_KEY` | Supabase anon key | - |
| `SQL_ECHO` | Enable SQL query logging | false |

## Migration Commands

```bash
# Test database connection
python manage_migrations.py test

# Create a new migration
python manage_migrations.py create "Description of changes"

# Apply all pending migrations
python manage_migrations.py upgrade

# Revert the last migration
python manage_migrations.py downgrade

# Show current migration version
python manage_migrations.py current

# Show migration history
python manage_migrations.py history

# Show migration status
python manage_migrations.py status

# Reset database (drop all tables and recreate)
python manage_migrations.py reset
``` 