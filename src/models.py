from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
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
    description = Column(Text, nullable=True)
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

class ProjectLbfac(Base):
    __tablename__ = "project_lbesc"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Labor Escalation fields
    escalation_period = Column(Text)
    description = Column(Text)
    percent_of_contract = Column(Text)
    labor_hours = Column(Text)
    escalation_percent = Column(Text)
    escalation_amount = Column(Text)
    financing_percent = Column(Text)
    total = Column(Text)
    code = Column(Text)
    type = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProjectDirlib(Base):
    __tablename__ = "project_dirlb"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Direct Labor fields
    labor_type = Column(Text)
    crew = Column(Text)
    hours = Column(Text)
    rate = Column(Text)
    sub_total = Column(Text)
    brdn = Column(Text)
    frng = Column(Text)
    brdn_total = Column(Text)
    frng_total = Column(Text)
    total = Column(Text)
    full_rate = Column(Text)
    code = Column(Text)
    type = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProjectInclb(Base):
    __tablename__ = "project_inclb"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Incidental Labor fields
    incidental_labor = Column(Text)
    hours = Column(Text)
    rate = Column(Text)
    sub_total = Column(Text)
    brdn = Column(Text)
    frng = Column(Text)
    brdn_total = Column(Text)
    frng_total = Column(Text)
    total = Column(Text)
    full_rate = Column(Text)
    code = Column(Text)
    type = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProjectIndlb(Base):
    __tablename__ = "project_indlb"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Indirect Labor fields
    indirect_labor = Column(Text)
    labor_percent = Column(Text)
    hours = Column(Text)
    rate = Column(Text)
    sub_total = Column(Text)
    brdn = Column(Text)
    frng = Column(Text)
    brdn_total = Column(Text)
    frng_total = Column(Text)
    total = Column(Text)
    full_rate = Column(Text)
    code = Column(Text)
    type = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 