"""
Seed Script - Populate Initial Data
Standalone script to populate rotation cities and other initial data.
Run this once to set up the database with seed data.

Usage:
    python seed.py
    # or
    .venv\Scripts\python.exe seed.py
"""
import os
from app import create_app, db
from app.models.rotation_city import RotationCity


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
            'res_hall_location': '123 Mission St, San Francisco, CA'
        },
        {
            'name': 'Berlin',
            'time_zone': 'Europe/Berlin',
            'res_hall_location': 'Kreuzberg District, Berlin, Germany'
        },
        {
            'name': 'Buenos Aires',
            'time_zone': 'America/Argentina/Buenos_Aires',
            'res_hall_location': 'San Telmo, Buenos Aires, Argentina'
        },
        {
            'name': 'Tokyo',
            'time_zone': 'Asia/Tokyo',
            'res_hall_location': 'Shibuya, Tokyo, Japan'
        },
        {
            'name': 'London',
            'time_zone': 'Europe/London',
            'res_hall_location': 'South Kensington, London, UK'
        }
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
        print("=" * 60)
        print("✅ Seeding completed successfully!")
        print("=" * 60)


if __name__ == '__main__':
    main()
