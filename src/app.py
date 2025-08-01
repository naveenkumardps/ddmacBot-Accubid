import streamlit as st
from dotenv import load_dotenv
import os
from database import get_db, engine
from models import Base, User, Project
from sqlalchemy.orm import Session

load_dotenv()  # Loads variables from .env

secret_key = os.getenv("SECRET_KEY")
api_url = os.getenv("API_URL")

# Create database tables
Base.metadata.create_all(bind=engine)

def main():
    st.title("Database Migration Demo App")
    st.write("Welcome to the database migration demonstration!")
    
    # Sidebar for database operations
    st.sidebar.header("Database Operations")
    
    # User input section
    st.header("User Management")
    
    with st.form("user_form"):
        username = st.text_input("Username:")
        email = st.text_input("Email:")
        full_name = st.text_input("Full Name:")
        role = st.selectbox("Role", ["user", "admin", "moderator"])
        is_active = st.checkbox("Active", value=True)
        
        if st.form_submit_button("Add User"):
            if username and email:
                # Get database session
                db = next(get_db())
                try:
                    new_user = User(
                        username=username,
                        email=email,
                        full_name=full_name,
                        role=role,
                        is_active=is_active
                    )
                    db.add(new_user)
                    db.commit()
                    st.success(f"User {username} added successfully!")
                except Exception as e:
                    st.error(f"Error adding user: {e}")
                    db.rollback()
                finally:
                    db.close()
            else:
                st.error("Username and email are required!")
    
    # Project input section
    st.header("Project Management")
    
    with st.form("project_form"):
        project_name = st.text_input("Project Name:")
        description = st.text_area("Description:")
        status = st.selectbox("Status", ["active", "completed", "on-hold"])
        
        if st.form_submit_button("Add Project"):
            if project_name:
                # Get database session
                db = next(get_db())
                try:
                    new_project = Project(
                        name=project_name,
                        description=description,
                        status=status
                    )
                    db.add(new_project)
                    db.commit()
                    st.success(f"Project {project_name} added successfully!")
                except Exception as e:
                    st.error(f"Error adding project: {e}")
                    db.rollback()
                finally:
                    db.close()
            else:
                st.error("Project name is required!")
    
    # Display data
    st.header("Current Data")
    
    # Display users
    st.subheader("Users")
    db = next(get_db())
    try:
        users = db.query(User).all()
        if users:
            user_data = []
            for user in users:
                user_data.append({
                    "ID": user.id,
                    "Username": user.username,
                    "Email": user.email,
                    "Full Name": user.full_name,
                    "Role": user.role,
                    "Active": user.is_active,
                    "Created": user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else "N/A"
                })
            st.dataframe(user_data)
        else:
            st.info("No users found in database.")
    finally:
        db.close()
    
    # Display projects
    st.subheader("Projects")
    db = next(get_db())
    try:
        projects = db.query(Project).all()
        if projects:
            project_data = []
            for project in projects:
                project_data.append({
                    "ID": project.id,
                    "Name": project.name,
                    "Description": project.description,
                    "Status": project.status,
                    "Created": project.created_at.strftime("%Y-%m-%d %H:%M:%S") if project.created_at else "N/A"
                })
            st.dataframe(project_data)
        else:
            st.info("No projects found in database.")
    finally:
        db.close()
    
    # Environment variables display
    st.sidebar.header("Environment Variables")
    st.sidebar.write(f"Secret Key: {secret_key}")
    st.sidebar.write(f"API URL: {api_url}")
    
    # Migration info
    st.sidebar.header("Migration Info")
    st.sidebar.info("""
    This app uses Alembic for database migrations.
    
    To manage migrations:
    - `python manage_migrations.py create "message"`
    - `python manage_migrations.py upgrade`
    - `python manage_migrations.py downgrade`
    """)

if __name__ == "__main__":
    main()