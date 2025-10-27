"""
Shared validation helpers for Pydantic error handling.
Provides user-friendly error messages for common validation errors.
"""

from pydantic import ValidationError, BaseModel
from pydantic.fields import FieldInfo
from typing import Dict, Type, Optional


def get_user_friendly_error_message(field_name: str, error_type: str, field_info: Optional[FieldInfo] = None) -> Optional[str]:
    """
    Generate user-friendly error messages based on field name, error type, and field constraints.

    Args:
        field_name: The name of the field that failed validation
        error_type: The Pydantic error type (e.g., 'string_too_short', 'string_pattern_mismatch')
        field_info: Optional Pydantic FieldInfo containing field metadata and constraints

    Returns:
        User-friendly error message or None to use default
    """
    # Handle email-specific patterns
    if field_name == "email" and "pattern" in error_type:
        return "Please enter a valid email address"

    # Handle string length constraints
    if "string_too_short" in error_type:
        if field_info and hasattr(field_info, 'metadata'):
            # Try to extract min_length from metadata
            for constraint in field_info.metadata:
                if hasattr(constraint, 'min_length'):
                    min_len = constraint.min_length
                    return f"{field_name.replace('_', ' ').title()} must be at least {min_len} characters long"

        # Fallback to generic message
        return f"{field_name.replace('_', ' ').title()} is too short"

    if "string_too_long" in error_type:
        if field_info and hasattr(field_info, 'metadata'):
            for constraint in field_info.metadata:
                if hasattr(constraint, 'max_length'):
                    max_len = constraint.max_length
                    return f"{field_name.replace('_', ' ').title()} must be no more than {max_len} characters long"

        return f"{field_name.replace('_', ' ').title()} is too long"

    # Return None to use the default Pydantic message
    return None


def parse_validation_errors(
    validation_error: ValidationError,
    model_class: Optional[Type[BaseModel]] = None
) -> Dict[str, str]:
    """
    Parse Pydantic ValidationError into a dictionary of field names to user-friendly error messages.

    Args:
        validation_error: The Pydantic ValidationError exception
        model_class: Optional Pydantic model class to extract field information for better error messages

    Returns:
        Dictionary mapping field names to error messages
    """
    errors_dict = {}

    # Get model fields if model class is provided
    model_fields = {}
    if model_class:
        model_fields = model_class.model_fields

    for error in validation_error.errors():
        field_name = error["loc"][0] if error["loc"] else None
        error_type = error.get("type", "")
        default_msg = error["msg"]

        # Skip if no field name or field name is not a string
        if not field_name or not isinstance(field_name, str):
            continue

        # Get field info from model if available
        field_info = model_fields.get(field_name) if model_fields else None

        # Try to get a user-friendly message
        friendly_msg = get_user_friendly_error_message(field_name, error_type, field_info)

        # Use friendly message if available, otherwise use default
        errors_dict[field_name] = friendly_msg if friendly_msg else default_msg

    return errors_dict
