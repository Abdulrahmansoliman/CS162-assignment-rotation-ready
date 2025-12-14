"""
Seed Script - Populate Initial Data
Standalone script to populate rotation cities and other initial data.
Run this once to set up the database with seed data.

Usage:
    cd backend
    python seed/seed.py
    # or
    .venv\Scripts\python.exe seed/seed.py
"""
import os
import sys
import base64

# Add backend directory to path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models.rotation_city import RotationCity
from app.models.category import Category
from app.models.tag import Tag, TagValueType
from app.models.value import Value
from app.models.item import Item
from app.models.category_item import CategoryItem
from app.models.item_tag_value import ItemTagValue
from app.models.user import User


def load_image_as_base64(image_path):
    """Load an image file and convert to base64 string."""
    try:
        # Get the path relative to seed directory
        full_path = os.path.join(os.path.dirname(__file__), image_path)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                image_data = f.read()
                return base64.b64encode(image_data).decode('utf-8')
        else:
            print(f"⚠️  Image not found: {full_path}")
            return None
    except Exception as e:
        print(f"⚠️  Error loading image {image_path}: {str(e)}")
        return None


def seed_rotation_cities():
    """Populate rotation cities."""
    print("🌍 Seeding rotation cities...")
    
    # Check if cities already exist
    existing_count = db.session.query(RotationCity).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} rotation cities already exist. Skipping.")
        return
    
    # Define rotation cities
    cities = [
        {
            'name': 'San Francisco',
            'time_zone': 'America/Los_Angeles',
            'res_hall_location': '16 Turk St, San Francisco, CA'
        },
        {
            'name': 'Taipei',
            'time_zone': 'Asia/Taipei',
            'res_hall_location': 'Xinyi District, Taipei, Taiwan'
        },
        {
            'name': 'Seoul',
            'time_zone': 'Asia/Seoul',
            'res_hall_location': 'Gangnam-gu, Seoul, South Korea'
        },
        {
            'name': 'Buenos Aires',
            'time_zone': 'America/Argentina/Buenos_Aires',
            'res_hall_location': '920 Esmeralda St, Buenos Aires, Argentina'
        },
        {
            'name': 'Hyderabad',
            'time_zone': 'India/Kolkata',
            'res_hall_location': 'Hitech City, Hyderabad, India'
        },
        {
            'name': 'Berlin',
            'time_zone': 'Europe/Berlin',
            'res_hall_location': 'Mitte, Berlin, Germany'
        },
    ]
    
    # Create and add cities
    for city_data in cities:
        city = RotationCity(**city_data)
        db.session.add(city)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(cities)} rotation cities")
    
    # Print added cities
    for i, city in enumerate(db.session.query(RotationCity).all(), 1):
        print(f"   {i}. {city.name} (ID: {city.city_id}) - {city.time_zone}")


def seed_categories():
    """Populate item categories with images stored in database."""
    print("📂 Seeding item categories with images...")
    
    # Check if categories already exist
    existing_count = db.session.query(Category).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} categories already exist. Skipping.")
        return
    
    # Define categories with image paths to be loaded
    categories = [
        {
            'category_name': 'SIM/eSIM',
            'image_path': 'categories-icons/Sim.png'
        },
        {
            'category_name': 'Groceries',
            'image_path': 'categories-icons/groceries.png'
        },
        {
            'category_name': 'Pharmacy',
            'image_path': 'categories-icons/Pharamacy.png'
        },
        {
            'category_name': 'ATM/Banks',
            'image_path': 'categories-icons/atm-banks.png'
        },
        {
            'category_name': 'Transport',
            'image_path': 'categories-icons/transportation.png'
        },
        {
            'category_name': 'Gyms',
            'image_path': 'categories-icons/gym.png'
        },
        {
            'category_name': 'Study Spaces',
            'image_path': 'categories-icons/study-places.png'
        },
        {
            'category_name': 'Eateries',
            'image_path': 'categories-icons/eateries.png'
        },
    ]
    
    # Create and add categories
    for cat_data in categories:
        image_path = cat_data.pop('image_path')
        
        # Load image as base64
        image_base64 = load_image_as_base64(image_path)
        
        # Create category with base64 encoded image
        category = Category(
            category_name=cat_data['category_name'],
            category_pic=image_base64
        )
        db.session.add(category)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(categories)} categories with images")
    
    # Print added categories
    for i, category in enumerate(db.session.query(Category).all(), 1):
        has_image = "✓" if category.category_pic else "✗"
        print(f"   {i}. {category.category_name} (ID: {category.category_id}) [{has_image} image]")


def seed_tags():
    """Populate tags with different value types."""
    print("🏷️  Seeding tags...")
    
    # Check if tags already exist
    existing_count = db.session.query(Tag).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} tags already exist. Skipping.")
        return
    
    # Define tags with their value types
    tags = [
        {'name': 'Condition', 'value_type': TagValueType.TEXT.code},
        {'name': 'Availability', 'value_type': TagValueType.BOOLEAN.code},
        {'name': 'Distance (meters)', 'value_type': TagValueType.NUMERIC.code},
        {'name': 'Operating Hours', 'value_type': TagValueType.TEXT.code},
        {'name': 'Price Range', 'value_type': TagValueType.TEXT.code},
        {'name': 'Open 24/7', 'value_type': TagValueType.BOOLEAN.code},
    ]
    
    # Create and add tags
    for tag_data in tags:
        tag = Tag(**tag_data)
        db.session.add(tag)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(tags)} tags")
    
    # Print added tags
    for i, tag in enumerate(db.session.query(Tag).all(), 1):
        print(f"   {i}. {tag.name} (ID: {tag.tag_id}) - {tag.value_type_label}")


def seed_values():
    """Populate values for tags."""
    print("💎 Seeding tag values...")
    
    # Check if values already exist
    existing_count = db.session.query(Value).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} values already exist. Skipping.")
        return
    
    # Get tags
    tags = db.session.query(Tag).all()
    tag_dict = {tag.name: tag for tag in tags}
    
    # Define values for different tags
    values = [
        # Condition values
        {'tag_id': tag_dict['Condition'].tag_id, 'name_val': 'Excellent', 'tag': tag_dict['Condition']},
        {'tag_id': tag_dict['Condition'].tag_id, 'name_val': 'Good', 'tag': tag_dict['Condition']},
        {'tag_id': tag_dict['Condition'].tag_id, 'name_val': 'Fair', 'tag': tag_dict['Condition']},
        
        # Operating Hours values
        {'tag_id': tag_dict['Operating Hours'].tag_id, 'name_val': 'Morning (6AM-12PM)', 'tag': tag_dict['Operating Hours']},
        {'tag_id': tag_dict['Operating Hours'].tag_id, 'name_val': 'Afternoon (12PM-6PM)', 'tag': tag_dict['Operating Hours']},
        {'tag_id': tag_dict['Operating Hours'].tag_id, 'name_val': 'Evening (6PM-12AM)', 'tag': tag_dict['Operating Hours']},
        
        # Price Range values
        {'tag_id': tag_dict['Price Range'].tag_id, 'name_val': 'Budget', 'tag': tag_dict['Price Range']},
        {'tag_id': tag_dict['Price Range'].tag_id, 'name_val': 'Mid-Range', 'tag': tag_dict['Price Range']},
        {'tag_id': tag_dict['Price Range'].tag_id, 'name_val': 'Premium', 'tag': tag_dict['Price Range']},
    ]
    
    # Create and add values
    for val_data in values:
        tag_obj = val_data.pop('tag')
        value = Value(**val_data)
        db.session.add(value)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(values)} tag values")


def seed_items_argentina():
    """Populate items for Buenos Aires, Argentina."""
    print("🍔 Seeding items for Argentina...")
    
    # Check if items already exist
    existing_count = db.session.query(Item).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} items already exist. Skipping.")
        return
    
    # Get Buenos Aires city
    buenos_aires = db.session.query(RotationCity).filter_by(name='Buenos Aires').first()
    if not buenos_aires:
        print("⚠️  Buenos Aires city not found. Skipping items.")
        return
    
    # Get or create a test user for Argentina
    user = db.session.query(User).filter_by(email='admin@minerva.ar').first()
    if not user:
        user = User(
            first_name='Admin',
            last_name='Minerva',
            email='admin@minerva.ar',
            is_verified=True,
            rotation_city_id=buenos_aires.city_id
        )
        db.session.add(user)
        db.session.flush()
    
    # Get categories and tags
    categories = {cat.category_name: cat for cat in db.session.query(Category).all()}
    tags = {tag.name: tag for tag in db.session.query(Tag).all()}
    values = db.session.query(Value).all()
    value_dict = {val.name_val: val for val in values if val.name_val}
    
    # Define items for Argentina
    items_data = [
        {
            'name': 'Librería Ateneo Grand Splendid',
            'location': 'Av. Santa Fe 1860, Buenos Aires',
            'walking_distance': 450.0,
            'categories': ['Study Spaces', 'Eateries'],
            'tags': [
                {'tag': 'Condition', 'value': 'Excellent'},
                {'tag': 'Operating Hours', 'value': 'Morning (6AM-12PM)'},
            ]
        },
        {
            'name': 'Farmacia del Dr. Sótero del Río',
            'location': 'Corrientes 1234, Buenos Aires',
            'walking_distance': 250.0,
            'categories': ['Pharmacy'],
            'tags': [
                {'tag': 'Availability', 'value': True},
                {'tag': 'Open 24/7', 'value': True},
            ]
        },
        {
            'name': 'Banco Nación Argentina',
            'location': 'Bartolomé Mitre 326, Buenos Aires',
            'walking_distance': 180.0,
            'categories': ['ATM/Banks'],
            'tags': [
                {'tag': 'Condition', 'value': 'Good'},
                {'tag': 'Operating Hours', 'value': 'Morning (6AM-12PM)'},
            ]
        },
        {
            'name': 'SuperMercado Carrefour',
            'location': 'Garay 1299, Buenos Aires',
            'walking_distance': 380.0,
            'categories': ['Groceries'],
            'tags': [
                {'tag': 'Price Range', 'value': 'Mid-Range'},
                {'tag': 'Operating Hours', 'value': 'Afternoon (12PM-6PM)'},
            ]
        },
        {
            'name': 'Centro de Gimnasia Smart Fit',
            'location': 'México 2150, Buenos Aires',
            'walking_distance': 550.0,
            'categories': ['Gyms'],
            'tags': [
                {'tag': 'Condition', 'value': 'Excellent'},
                {'tag': 'Distance (meters)', 'value': 550.0},
            ]
        },
        {
            'name': 'Restaurante El Chupetín',
            'location': 'San Martín 945, Buenos Aires',
            'walking_distance': 220.0,
            'categories': ['Eateries'],
            'tags': [
                {'tag': 'Price Range', 'value': 'Budget'},
                {'tag': 'Operating Hours', 'value': 'Evening (6PM-12AM)'},
            ]
        },
    ]
    
    # Create and add items
    for item_data in items_data:
        item_cats = item_data.pop('categories')
        item_tags = item_data.pop('tags')
        
        item = Item(
            added_by_user_id=user.user_id,
            rotation_city_id=buenos_aires.city_id,
            **item_data
        )
        db.session.add(item)
        db.session.flush()
        
        # Add categories to item
        for cat_name in item_cats:
            if cat_name in categories:
                cat_item = CategoryItem(
                    item_id=item.item_id,
                    category_id=categories[cat_name].category_id
                )
                db.session.add(cat_item)
        
        # Add tags to item
        for tag_info in item_tags:
            tag_name = tag_info['tag']
            tag_value = tag_info['value']
            
            if tag_name in tags:
                tag_obj = tags[tag_name]
                
                # Create value if needed (for boolean/numeric)
                if isinstance(tag_value, bool):
                    value = Value(
                        tag_id=tag_obj.tag_id,
                        boolean_val=tag_value
                    )
                elif isinstance(tag_value, (int, float)):
                    value = Value(
                        tag_id=tag_obj.tag_id,
                        numerical_value=tag_value
                    )
                else:
                    # Use existing value if available
                    value = value_dict.get(tag_value)
                    if not value:
                        value = Value(
                            tag_id=tag_obj.tag_id,
                            name_val=tag_value
                        )
                
                db.session.add(value)
                db.session.flush()
                
                # Link value to item
                itv = ItemTagValue(
                    item_id=item.item_id,
                    value_id=value.value_id
                )
                db.session.add(itv)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(items_data)} items for Argentina")
    
    # Print added items
    for i, item in enumerate(db.session.query(Item).all(), 1):
        print(f"   {i}. {item.name} (ID: {item.item_id}) - {item.location}")


def main():
    """Main seed function."""
    # Get environment from OS variable, default to 'development'
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create the Flask app
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 60)
        print("🌱 Database Seeding Script")
        print("=" * 60)
        print(f"Environment: {config_name}")
        print(f"Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print()
        
        # Run seed functions
        seed_rotation_cities()
        print()
        seed_categories()
        print()
        seed_tags()
        print()
        seed_values()
        print()
        seed_items_argentina()
        
        print()
        print("=" * 60)
        print("✅ Seeding completed successfully!")
        print("=" * 60)


if __name__ == '__main__':
    main()
