from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "ddmacbot")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_SSL_MODE = os.getenv("DB_SSL_MODE", "prefer")

def get_database_url():
    """
    Generate database URL based on DB_TYPE environment variable.
    Supports: sqlite, mysql, postgresql, supabase
    """
    if DB_TYPE == "sqlite":
        return os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    elif DB_TYPE == "mysql":
        if not all([DB_HOST, DB_NAME, DB_USER]) or DB_PASSWORD is None:
            logger.warning("MySQL configuration incomplete, falling back to SQLite")
            return "sqlite:///./app.db"
        
        port = f":{DB_PORT}" if DB_PORT else ""
        return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}{port}/{DB_NAME}"
    
    elif DB_TYPE == "postgresql":
        if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
            logger.warning("PostgreSQL configuration incomplete, falling back to SQLite")
            return "sqlite:///./app.db"
        
        port = f":{DB_PORT}" if DB_PORT else ":5432"
        ssl_mode = f"?sslmode={DB_SSL_MODE}" if DB_SSL_MODE else ""
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}{port}/{DB_NAME}{ssl_mode}"
    
    elif DB_TYPE == "supabase":
        # Supabase uses PostgreSQL with specific configuration
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not all([supabase_url, supabase_key]):
            logger.warning("Supabase configuration incomplete, falling back to SQLite")
            return "sqlite:///./app.db"
        
        # Extract host from Supabase URL
        # Example: https://xyz.supabase.co -> xyz.supabase.co
        host = supabase_url.replace("https://", "").replace("http://", "")
        
        return f"postgresql://postgres:{supabase_key}@{host}:5432/postgres?sslmode=require"
    
    else:
        logger.warning(f"Unknown DB_TYPE: {DB_TYPE}, falling back to SQLite")
        return "sqlite:///./app.db"

# Get the database URL
DATABASE_URL = get_database_url()

# Create SQLAlchemy engine with appropriate configuration
def create_engine_with_config():
    """Create SQLAlchemy engine with database-specific configurations"""
    
    if DB_TYPE == "sqlite":
        return create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    
    elif DB_TYPE == "mysql":
        return create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    
    elif DB_TYPE in ["postgresql", "supabase"]:
        return create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    
    else:
        return create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )

# Create engine
engine = create_engine_with_config()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1"))
            result.fetchone()  # Consume the result
            logger.info(f"Database connection successful! Using {DB_TYPE}")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        return False

if __name__ == "__main__":
    # Test the connection when run directly
    test_connection() 