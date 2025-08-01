from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to project items
    project_items = relationship("ProjectItem", back_populates="user")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to project items
    project_items = relationship("ProjectItem", back_populates="project")

class ProjectItem(Base):
    __tablename__ = "project_ext"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic item information
    description = Column(Text, nullable=False)
    quantity = Column(Float, default=1.0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Pricing information
    trade_price = Column(Float)
    price_unit = Column(String(50))
    discount_percent = Column(Float, default=0.0)
    link_price = Column(Float)
    cost_adjustment_percent = Column(Float, default=0.0)
    net_cost = Column(Float)
    
    # Labor information
    db_labor = Column(Float)
    labor = Column(Float)
    labor_unit = Column(String(50))
    labor_adjustment_percent = Column(Float, default=0.0)
    
    # Totals
    total_material = Column(Float)
    total_hours = Column(Float)
    
    # Conditions
    material_condition = Column(String(100))
    labor_condition = Column(String(100))
    
    # Weight information
    weight = Column(Float)
    weight_unit = Column(String(20))
    total_weight = Column(Float)
    
    # Manufacturer and catalog information
    manufacturer_name = Column(String(200))
    catalog_number = Column(String(100))
    price_code = Column(String(50))
    reference = Column(String(200))
    
    # Supplier information
    supplier_name = Column(String(200))
    supplier_code = Column(String(100))
    
    # Sort codes
    sort_code_1 = Column(String(100))
    sort_code_2 = Column(String(100))
    sort_code_3 = Column(String(100))
    sort_code_4 = Column(String(100))
    sort_code_5 = Column(String(100))
    sort_code_6 = Column(String(100))
    sort_code_7 = Column(String(100))
    sort_code_8 = Column(String(100))
    
    # Quick takeoff
    quick_takeoff_code = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="project_items")
    user = relationship("User", back_populates="project_items") 