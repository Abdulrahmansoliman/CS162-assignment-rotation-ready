"""
Request validation schemas for user endpoints.

Uses Pydantic for input validation with custom validators to ensure
data integrity and prevent malicious input.
"""
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class UpdateUserRequest(BaseModel):
    """
    Schema for updating user profile information.
    
    All fields are optional since users can update individual fields.
    Validates:
    - Names are not empty and contain only valid characters
    - Names don't exceed reasonable length
    - City ID is positive
    
    Rejects any unknown fields to prevent injection attacks.
    """
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    rotation_city_id: Optional[int] = None

    model_config = ConfigDict(
        str_strip_whitespace=True,  # Automatically strip leading/trailing whitespace
        extra='forbid'  # Reject any fields not defined in schema (security)
    )

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate name fields are not empty and contain valid characters.
        
        Rules:
        - Cannot be empty string (after stripping whitespace)
        - Cannot exceed 100 characters
        - Must contain only letters, spaces, hyphens, and apostrophes
        
        Args:
            v: Name value to validate
            
        Returns:
            Validated name string
            
        Raises:
            ValueError: If validation fails
        """
        if v is not None:
            # Check not empty after stripping
            if len(v) == 0:
                raise ValueError('Name cannot be empty')
            
            # Check length limit
            if len(v) > 100:
                raise ValueError('Name cannot exceed 100 characters')
            
            # Allow letters, spaces, hyphens, and apostrophes (for names like O'Brien, Mary-Jane)
            allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")
            if not all(c in allowed_chars for c in v):
                raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
            
            # Must contain at least one letter
            if not any(c.isalpha() for c in v):
                raise ValueError('Name must contain at least one letter')
        
        return v

    @field_validator('rotation_city_id')
    @classmethod
    def validate_city_id(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate rotation city ID is a positive integer.
        
        The actual existence of the city is checked at the service layer
        where we have access to the database.
        
        Args:
            v: City ID to validate
            
        Returns:
            Validated city ID
            
        Raises:
            ValueError: If city ID is not positive
        """
        if v is not None and v <= 0:
            raise ValueError('rotation_city_id must be a positive integer')
        return v
