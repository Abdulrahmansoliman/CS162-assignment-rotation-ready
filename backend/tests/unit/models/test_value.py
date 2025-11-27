"""
Unit tests for Value model
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.value import Value
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
    session.query(Value).delete()
    session.query(Tag).delete()
    session.commit()
    session.close()


@pytest.fixture
def tags(session):
    """Create test tags"""
    tag_bool = Tag(
        name="HasParking",
        value_type="boolean"
    )
    tag_name = Tag(
        name="Cuisine",
        value_type="name"
    )
    tag_num = Tag(
        name="Price",
        value_type="numerical"
    )
    session.add_all([tag_bool, tag_name, tag_num])
    session.commit()
    return {
        'boolean': tag_bool,
        'name': tag_name,
        'numerical': tag_num
    }


class TestValue:
    """Test cases for Value model"""

    def test_create_boolean_value(self, session, tags):
        """Test creating a boolean value"""
        value = Value(
            tag_id=tags['boolean'].tag_id,
            boolean_val=True
        )
        session.add(value)
        session.commit()

        assert value.value_id is not None
        assert value.boolean_val is True
        assert value.name_val is None
        assert value.numerical_value is None

    def test_create_name_value(self, session, tags):
        """Test creating a name value"""
        value = Value(
            tag_id=tags['name'].tag_id,
            name_val="Italian"
        )
        session.add(value)
        session.commit()

        assert value.value_id is not None
        assert value.name_val == "Italian"
        assert value.boolean_val is None
        assert value.numerical_value is None

    def test_create_numerical_value(self, session, tags):
        """Test creating a numerical value"""
        value = Value(
            tag_id=tags['numerical'].tag_id,
            numerical_value=25.50
        )
        session.add(value)
        session.commit()

        assert value.value_id is not None
        assert value.numerical_value == 25.50
        assert value.boolean_val is None
        assert value.name_val is None

    def test_relationship_to_tag(self, session, tags):
        """Test relationship with Tag"""
        value = Value(
            tag_id=tags['name'].tag_id,
            name_val="Mexican"
        )
        session.add(value)
        session.commit()

        assert value.tag.name == "Cuisine"
        assert value.tag.value_type == "name"

    def test_value_id_auto_increment(self, session, tags):
        """Test that value_id auto-increments"""
        val1 = Value(tag_id=tags['boolean'].tag_id, boolean_val=True)
        val2 = Value(tag_id=tags['boolean'].tag_id, boolean_val=False)
        session.add_all([val1, val2])
        session.commit()

        assert val1.value_id != val2.value_id

    def test_repr_method(self, session, tags):
        """Test string representation"""
        value = Value(
            tag_id=tags['numerical'].tag_id,
            numerical_value=100
        )
        session.add(value)
        session.commit()

        repr_str = repr(value)
        assert "Value" in repr_str
