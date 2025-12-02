"""
Value and Tag Fixtures
"""
import pytest
from app.models import Tag, Value


@pytest.fixture
def boolean_tag(db_session):
    """Create a boolean type tag."""
    tag = Tag(
        name='Available',
        value_type='boolean',
        can_add_new_value=True
    )
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


@pytest.fixture
def text_tag(db_session):
    """Create a text type tag."""
    tag = Tag(
        name='Color',
        value_type='text',
        can_add_new_value=True
    )
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


@pytest.fixture
def numeric_tag(db_session):
    """Create a numeric type tag."""
    tag = Tag(
        name='Size',
        value_type='numeric',
        can_add_new_value=True
    )
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    return tag


@pytest.fixture
def boolean_value(db_session, boolean_tag):
    """Create a boolean value."""
    value = Value(
        tag_id=boolean_tag.tag_id,
        boolean_val=True,
        name_val=None,
        numerical_value=None
    )
    db_session.add(value)
    db_session.commit()
    db_session.refresh(value)
    return value


@pytest.fixture
def text_value(db_session, text_tag):
    """Create a text value."""
    value = Value(
        tag_id=text_tag.tag_id,
        boolean_val=None,
        name_val='Red',
        numerical_value=None
    )
    db_session.add(value)
    db_session.commit()
    db_session.refresh(value)
    return value


@pytest.fixture
def numeric_value(db_session, numeric_tag):
    """Create a numeric value."""
    value = Value(
        tag_id=numeric_tag.tag_id,
        boolean_val=None,
        name_val=None,
        numerical_value=42.5
    )
    db_session.add(value)
    db_session.commit()
    db_session.refresh(value)
    return value
