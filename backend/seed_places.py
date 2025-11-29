"""
Seed Script - Populate sample places in Retiro, Buenos Aires
"""
import os
from datetime import datetime, timedelta
from app import create_app, db
from app.models.item import Item
from app.models.category import Category
from app.models.category_item import CategoryItem
from app.models.user import User
from app.models.rotation_city import RotationCity
from app.models.tag import Tag
from app.models.value import Value
from app.models.item_tag_value import ItemTagValue

def seed_categories():
    """Create categories if they don't exist"""
    categories_data = [
        {'name': 'SIM/eSIM', 'pic': None},
        {'name': 'Groceries', 'pic': None},
        {'name': 'Pharmacy', 'pic': None},
        {'name': 'ATM/Banks', 'pic': None},
        {'name': 'Transport', 'pic': None},
        {'name': 'Gyms', 'pic': None},
        {'name': 'Study Spaces', 'pic': None},
        {'name': 'Eateries', 'pic': None},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category = db.session.query(Category).filter_by(name=cat_data['name']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            db.session.flush()
        categories[cat_data['name']] = category
    
    db.session.commit()
    return categories

def seed_tags():
    """Create tags if they don't exist"""
    tags_data = [
        {'name': 'English', 'value_type': 'boolean'},
        {'name': 'Foreign Cards', 'value_type': 'boolean'},
        {'name': 'Budget', 'value_type': 'text'},  # $, $$, $$$
    ]
    
    tags = {}
    for tag_data in tags_data:
        tag = db.session.query(Tag).filter_by(name=tag_data['name']).first()
        if not tag:
            tag = Tag(**tag_data)
            db.session.add(tag)
            db.session.flush()
        tags[tag_data['name']] = tag
    
    db.session.commit()
    return tags

def seed_places(categories, tags, user, buenos_aires):
    """Seed sample places in Retiro, Buenos Aires"""
    
    # Real places in Retiro, Buenos Aires
    places_data = [
        # SIM/eSIM
        {
            'name': 'Personal SIM Card Store',
            'location': 'Av. Santa Fe 1234, Retiro, Buenos Aires',
            'walking_distance': 0.3,
            'category': 'SIM/eSIM',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$',
            'verifications': 12,
            'days_ago': 2
        },
        {
            'name': 'Movistar Retiro',
            'location': 'Av. del Libertador 1200, Retiro, Buenos Aires',
            'walking_distance': 0.5,
            'category': 'SIM/eSIM',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 8,
            'days_ago': 5
        },
        
        # Groceries
        {
            'name': 'Carrefour Express',
            'location': 'Av. Córdoba 567, Retiro, Buenos Aires',
            'walking_distance': 0.5,
            'category': 'Groceries',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 8,
            'days_ago': 7
        },
        {
            'name': 'Disco Retiro',
            'location': 'Av. Leandro N. Alem 700, Retiro, Buenos Aires',
            'walking_distance': 0.4,
            'category': 'Groceries',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 15,
            'days_ago': 3
        },
        {
            'name': 'Supermercado Jumbo',
            'location': 'Av. del Libertador 1000, Retiro, Buenos Aires',
            'walking_distance': 0.6,
            'category': 'Groceries',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$$$',
            'verifications': 20,
            'days_ago': 1
        },
        
        # Pharmacy
        {
            'name': 'Farmacity',
            'location': 'Av. Callao 890, Retiro, Buenos Aires',
            'walking_distance': 0.4,
            'category': 'Pharmacy',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 15,
            'days_ago': 3
        },
        {
            'name': 'Farmacia Retiro',
            'location': 'Av. Santa Fe 1500, Retiro, Buenos Aires',
            'walking_distance': 0.2,
            'category': 'Pharmacy',
            'tags': {'English': False, 'Foreign Cards': False},
            'budget': '$',
            'verifications': 5,
            'days_ago': 10
        },
        
        # ATM/Banks
        {
            'name': 'Banco Santander',
            'location': 'Av. del Libertador 1100, Retiro, Buenos Aires',
            'walking_distance': 0.5,
            'category': 'ATM/Banks',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 10,
            'days_ago': 4
        },
        {
            'name': 'Banco Nación',
            'location': 'Av. Leandro N. Alem 500, Retiro, Buenos Aires',
            'walking_distance': 0.3,
            'category': 'ATM/Banks',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$',
            'verifications': 18,
            'days_ago': 2
        },
        
        # Transport
        {
            'name': 'Retiro Bus Terminal',
            'location': 'Av. Antártida Argentina, Retiro, Buenos Aires',
            'walking_distance': 0.8,
            'category': 'Transport',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$',
            'verifications': 25,
            'days_ago': 1
        },
        {
            'name': 'Retiro Train Station',
            'location': 'Av. Ramos Mejía 1350, Retiro, Buenos Aires',
            'walking_distance': 0.7,
            'category': 'Transport',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$',
            'verifications': 30,
            'days_ago': 0
        },
        
        # Gyms
        {
            'name': 'Megatlon Retiro',
            'location': 'Av. del Libertador 1300, Retiro, Buenos Aires',
            'walking_distance': 0.6,
            'category': 'Gyms',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$$',
            'verifications': 12,
            'days_ago': 5
        },
        {
            'name': 'Smart Fit Retiro',
            'location': 'Av. Santa Fe 1800, Retiro, Buenos Aires',
            'walking_distance': 0.9,
            'category': 'Gyms',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 8,
            'days_ago': 6
        },
        
        # Study Spaces
        {
            'name': 'Biblioteca Nacional',
            'location': 'Agüero 2502, Retiro, Buenos Aires',
            'walking_distance': 1.2,
            'category': 'Study Spaces',
            'tags': {'English': False, 'Foreign Cards': False},
            'budget': '$',
            'verifications': 22,
            'days_ago': 2
        },
        {
            'name': 'Starbucks Retiro',
            'location': 'Av. del Libertador 1000, Retiro, Buenos Aires',
            'walking_distance': 0.6,
            'category': 'Study Spaces',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 15,
            'days_ago': 1
        },
        
        # Eateries
        {
            'name': 'McDonald\'s Retiro',
            'location': 'Av. del Libertador 1200, Retiro, Buenos Aires',
            'walking_distance': 0.5,
            'category': 'Eateries',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$',
            'verifications': 35,
            'days_ago': 0
        },
        {
            'name': 'La Parolaccia',
            'location': 'Av. Santa Fe 1400, Retiro, Buenos Aires',
            'walking_distance': 0.4,
            'category': 'Eateries',
            'tags': {'English': False, 'Foreign Cards': True},
            'budget': '$$$',
            'verifications': 18,
            'days_ago': 3
        },
        {
            'name': 'Café Martínez',
            'location': 'Av. Leandro N. Alem 600, Retiro, Buenos Aires',
            'walking_distance': 0.3,
            'category': 'Eateries',
            'tags': {'English': True, 'Foreign Cards': True},
            'budget': '$$',
            'verifications': 20,
            'days_ago': 2
        },
    ]
    
    for place_data in places_data:
        # Check if place already exists
        existing = db.session.query(Item).filter_by(
            name=place_data['name'],
            rotation_city_id=buenos_aires.city_id
        ).first()
        
        if existing:
            continue
        
        # Create item
        item = Item(
            name=place_data['name'],
            location=place_data['location'],
            walking_distance=place_data['walking_distance'],
            added_by_user_id=user.user_id,
            rotation_city_id=buenos_aires.city_id,
            number_of_verifications=place_data['verifications'],
            last_verified_date=datetime.utcnow() - timedelta(days=place_data['days_ago'])
        )
        db.session.add(item)
        db.session.flush()
        
        # Add to category
        category = categories[place_data['category']]
        category_item = CategoryItem(
            item_id=item.item_id,
            category_id=category.category_id
        )
        db.session.add(category_item)
        
        # Add tags
        for tag_name, tag_value in place_data['tags'].items():
            if tag_name in tags:
                tag = tags[tag_name]
                # Find or create value
                value = db.session.query(Value).filter_by(
                    tag_id=tag.tag_id,
                    boolean_val=tag_value
                ).first()
                if not value:
                    value = Value(tag_id=tag.tag_id, boolean_val=tag_value)
                    db.session.add(value)
                    db.session.flush()
                
                item_tag_value = ItemTagValue(
                    item_id=item.item_id,
                    value_id=value.value_id
                )
                db.session.add(item_tag_value)
        
        # Add budget tag
        if 'budget' in place_data:
            budget_tag = tags['Budget']
            budget_value = db.session.query(Value).filter_by(
                tag_id=budget_tag.tag_id,
                name_val=place_data['budget']
            ).first()
            if not budget_value:
                budget_value = Value(tag_id=budget_tag.tag_id, name_val=place_data['budget'])
                db.session.add(budget_value)
                db.session.flush()
            
            item_tag_value = ItemTagValue(
                item_id=item.item_id,
                value_id=budget_value.value_id
            )
            db.session.add(item_tag_value)
    
    db.session.commit()
    print(f"✅ Successfully seeded {len(places_data)} places")

def main():
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        print("=" * 60)
        print("🌱 Seeding Places in Retiro, Buenos Aires")
        print("=" * 60)
        
        # Get Buenos Aires city
        buenos_aires = db.session.query(RotationCity).filter_by(name='Buenos Aires').first()
        if not buenos_aires:
            print("❌ Buenos Aires rotation city not found. Please seed cities first.")
            return
        
        # Get or create test user
        user = db.session.query(User).filter_by(email='haya@uni.minerva.edu').first()
        if not user:
            print("❌ Test user not found. Please create user first.")
            return
        
        # Seed categories
        print("📁 Seeding categories...")
        categories = seed_categories()
        print(f"✅ Created/found {len(categories)} categories")
        
        # Seed tags
        print("🏷️  Seeding tags...")
        tags = seed_tags()
        print(f"✅ Created/found {len(tags)} tags")
        
        # Seed places
        print("📍 Seeding places...")
        seed_places(categories, tags, user, buenos_aires)
        
        print("=" * 60)
        print("✅ Seeding completed successfully!")
        print("=" * 60)

if __name__ == '__main__':
    main()

