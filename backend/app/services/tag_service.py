"""Tag service for business logic."""
from typing import List
from app.models.tag import Tag
from app.repositories.implementations.tag_repository import TagRepository


class TagService:
    """Service for tag-related operations.
    
    Handles business logic for managing tags that can be applied to items.
    """

    def __init__(self, tag_repository: TagRepository = None):
        """Initialize service with optional dependency injection.
        
        Args:
            tag_repository: Optional TagRepository instance for testing/DI
        """
        self.tag_repository = tag_repository or TagRepository()

    def get_all_tags(self) -> List[Tag]:
        """Retrieve all available tags.
        
        Returns:
            List of all Tag objects ordered alphabetically by name
        """
        return self.tag_repository.get_all_tags()
