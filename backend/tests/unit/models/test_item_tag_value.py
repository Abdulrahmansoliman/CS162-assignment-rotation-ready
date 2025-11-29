"""
Unit tests for ItemTagValue model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.item_tag_value import ItemTagValue
from app.models.item import Item
from app.models.tag import Tag
from app.models.value import Value
from app.models.user import User
from app.models.rotation_city import RotationCity


@pytest.fixture(scope='module')
def engine():
    """Create test database engine"""
    engine = create_engine('sqlite:///:memory:')
    db.Model.metadata.create_all(engine)
    yield engine
    db.Model.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope='function')
def session(engine):
    """Create a new database session for a test"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.query(ItemTagValue).delete()
    session.query(Value).delete()
    session.query(Tag).delete()
    session.query(Item).delete()
    session.query(User).delete()
    session.query(RotationCity).delete()
    session.commit()
    session.close()


@pytest.fixture
def test_data(session):
    """Create test data"""
    # Create city, user, and item
    city = RotationCity(name="TagCity", time_zone="UTC")
    session.add(city)
    session.commit()
    
    user = User(
        rotation_city_id=city.city_id,
        first_name="Tag",
        last_name="User",
        email="tag@example.com"
    )
    session.add(user)
    session.commit()
    
    item = Item(
        added_by_user_id=user.user_id,
        rotation_city_id=city.city_id,
        name="Restaurant",
        location="Downtown"
    )
    session.add(item)
    session.commit()
    
    # Create tag and value
    tag = Tag(name="Rating", value_type="numerical")
    session.add(tag)
    session.commit()
    
    value = Value(
        tag_id=tag.tag_id,
        numerical_value=4.5
    )
    session.add(value)
    session.commit()
    
    return {
        'city': city,
        'user': user,
        'item': item,
        'tag': tag,
        'value': value
    }


class TestItemTagValue:
    """Test cases for ItemTagValue junction table"""

    def test_create_item_tag_value(self, session, test_data):
        """Test creating an item-tag-value relationship"""
        itv = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=test_data['value'].value_id
        )
        session.add(itv)
        session.commit()

        assert itv.item_tag_value_id is not None
        assert itv.item_id == test_data['item'].item_id
        assert itv.value_id == test_data['value'].value_id

    def test_relationships(self, session, test_data):
        """Test relationships to item and value"""
        itv = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=test_data['value'].value_id
        )
        session.add(itv)
        session.commit()

        assert itv.item.name == "Restaurant"
        assert itv.value.numerical_value == 4.5

    def test_multiple_tags_per_item(self, session, test_data):
        """Test that an item can have multiple tag-value pairs"""
        # Create another tag and value
        tag2 = Tag(name="PriceRange", value_type="name")
        session.add(tag2)
        session.commit()
        
        value2 = Value(tag_id=tag2.tag_id, name_val="$$")
        session.add(value2)
        session.commit()
        
        # Create two item-tag-value relationships
        itv1 = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=test_data['value'].value_id
        )
        itv2 = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=value2.value_id
        )
        session.add_all([itv1, itv2])
        session.commit()

        item_tag_values = session.query(ItemTagValue).filter_by(
            item_id=test_data['item'].item_id
        ).all()
        assert len(item_tag_values) == 2

    def test_item_tag_value_id_auto_increment(self, session, test_data):
        """Test that item_tag_value_id auto-increments"""
        # Create another value
        value2 = Value(tag_id=test_data['tag'].tag_id, numerical_value=5.0)
        session.add(value2)
        session.commit()
        
        itv1 = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=test_data['value'].value_id
        )
        itv2 = ItemTagValue(
            item_id=test_data['item'].item_id,
            value_id=value2.value_id
        )
        session.add_all([itv1, itv2])
        session.commit()

        assert itv1.item_tag_value_id != itv2.item_tag_value_id
