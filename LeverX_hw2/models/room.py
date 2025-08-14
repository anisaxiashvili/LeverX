"""Room data model."""
from dataclasses import dataclass
from typing import Dict, Any
from ..utils.validation import validate_positive_integer, validate_non_empty_string


@dataclass
class Room:
    """
    Room data model with validation.
    
    Attributes:
        id: Unique room identifier
        name: Room name/description
    """
    id: int
    name: str
    
    def __post_init__(self):
        """Validate room data after initialization."""
        validate_positive_integer(self.id, "Room ID")
        validate_non_empty_string(self.name, "Room name")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert room to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        """Create Room instance from dictionary."""
        return cls(
            id=data.get('id'),
            name=data.get('name', '')
        )
