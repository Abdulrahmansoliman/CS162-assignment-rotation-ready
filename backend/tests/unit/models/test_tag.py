"""
Unit tests for Tag model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.tag import Tag


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
    session.rollback()
    session.query(Tag).delete()
    session.commit()
    session.close()


class TestTag:
    """Test cases for Tag model"""

    def test_create_tag(self, session):
        """Test creating a tag"""
        tag = Tag(
            name="Price",
            value_type="numerical",
            can_add_new_value=True
        )
        session.add(tag)
        session.commit()

        assert tag.tag_id is not None
        assert tag.name == "Price"
        assert tag.value_type == "numerical"
        assert tag.can_add_new_value is True

    def test_tag_with_boolean_type(self, session):
        """Test creating tag with boolean value type"""
        tag = Tag(
            name="Is Open",
            value_type="boolean",
            can_add_new_value=False
        )
        session.add(tag)
        session.commit()

        assert tag.value_type == "boolean"
        assert tag.can_add_new_value is False

    def test_tag_with_name_type(self, session):
        """Test creating tag with name value type"""
        tag = Tag(
            name="Color",
            value_type="name",
            can_add_new_value=True
        )
        session.add(tag)
        session.commit()

        assert tag.value_type == "name"

    def test_unique_tag_name(self, session):
        """Test that tag names must be unique"""
        tag1 = Tag(name="Hours", value_type="name")
        session.add(tag1)
        session.commit()

        tag2 = Tag(name="Hours", value_type="numerical")
        session.add(tag2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_tag_id_auto_increment(self, session):
        """Test that tag_id auto-increments"""
        tag1 = Tag(name="Rating", value_type="numerical")
        tag2 = Tag(name="Status", value_type="name")
        session.add_all([tag1, tag2])
        session.commit()

        assert tag1.tag_id != tag2.tag_id

    def test_repr_method(self, session):
        """Test string representation"""
        tag = Tag(name="WiFi", value_type="boolean")
        session.add(tag)
        session.commit()

        repr_str = repr(tag)
        assert "Tag" in repr_str
        assert "WiFi" in repr_str
