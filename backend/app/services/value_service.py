from app.models.value import Value


class ValueService:
    @staticmethod
    def get_value(value_id: int):
        """Get value by ID"""
        value = Value.query.filter_by(value_id=value_id).first()
        return value