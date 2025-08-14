"""Combined room data model for output."""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class CombinedRoom:
    """
    Combined room model containing room info and assigned students.
    
    Attributes:
        id: Room identifier (None for unassigned students)
        name: Room name
        students: List of students assigned to this room
    """
    id: Optional[int]
    name: str
    students: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'students': self.students
        }
    
    def add_student(self, student_id: int, student_name: str) -> None:
        """Add a student to this room."""
        student_data = {
            'id': student_id,
            'name': student_name
        }
        self.students.append(student_data)
    
    def get_student_count(self) -> int:
        """Get number of students in this room."""
        return len(self.students)

