"""
Simple script to add a test user
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.rotation_city import RotationCity
from app.models.verification_stutus_enum import VerificationStatusEnum

def main():
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    with app.app_context():
        # Get Buenos Aires rotation city
        buenos_aires = db.session.query(RotationCity).filter_by(name='Buenos Aires').first()
        
        if not buenos_aires:
            print("❌ Buenos Aires rotation city not found. Please seed the database first.")
            return
        
        # Check if user already exists
        existing_user = db.session.query(User).filter_by(email='haya@uni.minerva.edu').first()
        if existing_user:
            print(f"ℹ️  User with email 'haya@uni.minerva.edu' already exists (ID: {existing_user.user_id})")
            # Update user details to match requirements
            existing_user.first_name = 'Haya'
            existing_user.last_name = 'Elmizwghi'
            existing_user.rotation_city_id = buenos_aires.city_id
            existing_user.is_verified = True
            existing_user.status = VerificationStatusEnum.VERIFIED.code
            db.session.commit()
            print("✅ User updated and marked as verified")
            return
        
        # Create new user
        new_user = User(
            first_name='Haya',
            last_name='Elmizwghi',
            email='haya@uni.minerva.edu',
            rotation_city_id=buenos_aires.city_id,
            is_verified=True,
            status=VerificationStatusEnum.VERIFIED.code
        )
        
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        
        print("=" * 60)
        print("✅ User created successfully!")
        print("=" * 60)
        print(f"Name: {new_user.first_name} {new_user.last_name}")
        print(f"Email: {new_user.email}")
        print(f"Rotation City: {buenos_aires.name}")
        print(f"User ID: {new_user.user_id}")
        print(f"Verified: {new_user.is_verified}")
        print("=" * 60)
        print("You can now login with: haya@uni.minerva.edu")
        print("=" * 60)

if __name__ == '__main__':
    main()

