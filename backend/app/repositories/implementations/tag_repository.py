"""Tag repository implementation."""
from typing import List, Optional, Union
from app import db
from app.models.tag import Tag, TagValueType
from app.repositories.base.tag_repository_interface import TagRepositoryInterface


class TagRepository(TagRepositoryInterface):
    """Repository for tag operations."""

    def get_all_tags(self) -> List[Tag]:
        """Get all tags."""
        return db.session.execute(
            db.select(Tag).order_by(Tag.name)
        ).scalars().all()

    def get_tag_by_id(self, tag_id: int) -> Optional[Tag]:
        """Get tag by ID."""
        return db.session.execute(
            db.select(Tag).filter_by(tag_id=tag_id)
        ).scalar_one_or_none()

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name (case-insensitive)."""
        return db.session.execute(
            db.select(Tag).filter(Tag.name.ilike(name))
        ).scalar_one_or_none()

    def create_tag(self, name: str, value_type: Union[str, int]) -> Tag:
        """Create a new tag.
        
        Args:
            name: Tag name
            value_type: Either integer code (0, 1, 2) or string label ("boolean", "text", "numeric")
        """
        # Convert string labels to integer codes if needed
        if isinstance(value_type, str):
            value_type = TagValueType.from_label(value_type).code
        
        tag = Tag(name=name, value_type=value_type)
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)
        return tag
