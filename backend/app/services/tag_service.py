"""Tag service for business logic."""
from typing import List
from app.models.tag import Tag
from app.repositories.implementations.tag_repository import TagRepository


class TagService:
    """Service for tag-related operations."""

    def __init__(self, tag_repository: TagRepository = None):
        self.tag_repository = tag_repository or TagRepository()

    def get_all_tags(self) -> List[Tag]:
        """Get all available tags."""
        return self.tag_repository.get_all_tags()
