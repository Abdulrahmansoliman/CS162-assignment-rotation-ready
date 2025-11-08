from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class RotationCity(Base):
    """
    Represents a rotation city where users are assigned
    Contains city information and residential hall location
    """
    __tablename__ = 'rotation_city'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    time_zone = Column(String(50), nullable=False)
    res_hall_location = Column(String(200), nullable=True)
    
    # Relationship to users in this rotation city
    users = relationship("User", back_populates="rotation_city")


class User(Base):
    """
    Represents a user in the system
    Each user belongs to a rotation city and can add/verify items
    """
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    rotation_city_id = Column(Integer, ForeignKey('rotation_city.id'), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile_picture = Column(String(200), nullable=True)  # URL or file path
    
    # Relationships
    rotation_city = relationship("RotationCity", back_populates="users")
    added_items = relationship("Item", back_populates="added_by_user")
    verifications = relationship("Verification", back_populates="user")


class Category(Base):
    """
    Categories for organizing items (e.g., Electronics, Furniture, etc.)
    """
    __tablename__ = 'category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    pic = Column(String(200), nullable=True)  # Category icon/image URL
    
    # Relationship to category_item junction table
    category_items = relationship("CategoryItem", back_populates="category")


class Item(Base):
    """
    Items that can be found/verified in rotation cities
    Each item belongs to categories through the junction table
    """
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    location = Column(String(500), nullable=False)  # Where the item can be found
    walking_distance = Column(Float, nullable=True)  # Distance in minutes/km
    last_verified_date = Column(DateTime, nullable=True)
    added_by = Column(Integer, ForeignKey('user.id'), nullable=False)  # FK to user who added item
    created_at = Column(DateTime, default=datetime.utcnow)
    number_of_verifications = Column(Integer, default=0)
    
    # Relationships
    added_by_user = relationship("User", back_populates="added_items")
    category_items = relationship("CategoryItem", back_populates="item")
    verifications = relationship("Verification", back_populates="item")
    item_tag_values = relationship("ItemTagValue", back_populates="item")


class CategoryItem(Base):
    """
    Junction table linking items to categories (many-to-many relationship)
    An item can belong to multiple categories
    """
    __tablename__ = 'category_item'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    
    # Relationships
    item = relationship("Item", back_populates="category_items")
    category = relationship("Category", back_populates="category_items")


class Verification(Base):
    """
    Records when users verify that an item still exists/is available
    Helps keep item information current
    """
    __tablename__ = 'verification'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    items_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, nullable=True)  # Optional verification notes
    
    # Relationships
    user = relationship("User", back_populates="verifications")
    item = relationship("Item", back_populates="verifications")


class Tag(Base):
    """
    Tags that can be applied to items for additional metadata
    Supports different value types (boolean, text, numeric)
    """
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    value_type = Column(String(20), nullable=False)  # 'boolean', 'text', 'numeric'
    can_add_new_value = Column(Boolean, default=True)  # Whether users can add custom values
    
    # Relationships
    values = relationship("Value", back_populates="tag")


class Value(Base):
    """
    Possible values for tags
    Supports different data types through separate columns
    """
    __tablename__ = 'value'
    
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    boolean_val = Column(Boolean, nullable=True)
    name_val = Column(String(200), nullable=True)  # Text values
    numerical_value = Column(Float, nullable=True)
    
    # Relationships
    tag = relationship("Tag", back_populates="values")
    item_tag_values = relationship("ItemTagValue", back_populates="value")


class ItemTagValue(Base):
    """
    Junction table linking items to specific tag values
    Associates items with their tag metadata
    """
    __tablename__ = 'item_tag_value'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    value_id = Column(Integer, ForeignKey('value.id'), nullable=False)
    
    # Relationships
    item = relationship("Item", back_populates="item_tag_values")
    value = relationship("Value", back_populates="item_tag_values")


# Database setup
engine = create_engine("sqlite+pysqlite:///rotation_finder.db", echo=True, future=True)

# Create all tables
Base.metadata.create_all(engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)