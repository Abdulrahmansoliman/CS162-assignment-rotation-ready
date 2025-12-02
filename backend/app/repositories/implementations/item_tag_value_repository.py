"""Item-Tag-Value junction repository."""
from app import db
from app.models.item_tag_value import ItemTagValue


class ItemTagValueRepository:
    """Repository for item-tag-value junction table operations."""

    def add_tag_value_to_item(self, item_id: int, value_id: int) -> ItemTagValue:
        """Link a tag value to an item."""
        item_tag_value = ItemTagValue(
            item_id=item_id,
            value_id=value_id
        )
        db.session.add(item_tag_value)
        return item_tag_value

    def add_tag_values_to_item(self, item_id: int, value_ids: list[int]) -> None:
        """Link multiple tag values to an item."""
        for value_id in value_ids:
            self.add_tag_value_to_item(item_id, value_id)
        db.session.commit()
