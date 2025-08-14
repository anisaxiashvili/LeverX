"""Student data model."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from ..utils.validation import validate_positive_integer, validate_non_empty_string


@dataclass
class Student:
    """
    Student data model with validation.
    
    Attributes:
        id: Unique student identifier
        name: Student's full name
        room: Optional room assignment ID
    """
    id: int
    name: str
    room: Optional[int] = None
    
    def __post_init__(self):
        """Validate student data after initialization."""
        validate_positive_integer(self.id, "Student ID")
        validate_non_empty_string(self.name, "Student name")
        if self.room is not None:
            validate_positive_integer(self.room, "Room ID")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert student to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'room': self.room
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Create Student instance from dictionary."""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            room=data.get('room')
        )
