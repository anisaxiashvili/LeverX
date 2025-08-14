"""Validation utility functions."""
from typing import Any, List, Dict
from ..exceptions.custom_exceptions import ValidationError


def validate_positive_integer(value: Any, field_name: str) -> None:
    """
    Validate that value is a positive integer.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field_name} must be a positive integer, got: {value}")


def validate_non_empty_string(value: Any, field_name: str) -> None:
    """
    Validate that value is a non-empty string.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string, got: {value}")


def validate_file_path(file_path: str) -> None:
    """
    Validate file path format.
    
    Args:
        file_path: Path to validate
        
    Raises:
        ValidationError: If path is invalid
    """
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValidationError("File path must be a non-empty string")


def validate_students_data(students: List[Dict[str, Any]]) -> None:
    """
    Validate students data structure.
    
    Args:
        students: Students data to validate
        
    Raises:
        ValidationError: If data is invalid
    """
    if not isinstance(students, list):
        raise ValidationError("Students data must be a list")
    
    for i, student in enumerate(students):
        if not isinstance(student, dict):
            raise ValidationError(f"Student at index {i} must be a dictionary")
        
        if 'id' not in student:
            raise ValidationError(f"Student at index {i} missing required 'id' field")
        
        if 'name' not in student:
            raise ValidationError(f"Student at index {i} missing required 'name' field")


def validate_rooms_data(rooms: List[Dict[str, Any]]) -> None:
    """
    Validate rooms data structure.
    
    Args:
        rooms: Rooms data to validate
        
    Raises:
        ValidationError: If data is invalid
    """
    if not isinstance(rooms, list):
        raise ValidationError("Rooms data must be a list")
    
    for i, room in enumerate(rooms):
        if not isinstance(room, dict):
            raise ValidationError(f"Room at index {i} must be a dictionary")
        
        if 'id' not in room:
            raise ValidationError(f"Room at index {i} missing required 'id' field")
        
        if 'name' not in room:
            raise ValidationError(f"Room at index {i} missing required 'name' field")
