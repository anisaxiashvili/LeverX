"""Room-student business logic service."""
import logging
from typing import List, Dict, Any

from ..interfaces.service_interface import RoomStudentServiceInterface
from ..models.combined_room import CombinedRoom
from ..exceptions.custom_exceptions import ValidationError
from ..utils.validation import validate_students_data, validate_rooms_data


class RoomStudentService(RoomStudentServiceInterface):
    """Service implementing room-student business logic."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def combine_data(self, students: List[Dict[str, Any]], rooms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine students and rooms data according to business rules.
        
        Business Rules:
        1. Students are assigned to rooms based on their 'room' field
        2. Students without room assignment go to 'Unassigned Students'
        3. Empty rooms are included in output with empty student list
        4. Room order is preserved from input
        
        Args:
            students: List of student data dictionaries
            rooms: List of room data dictionaries
            
        Returns:
            List of combined room dictionaries with assigned students
        """
        self.logger.info(f"Combining {len(students)} students with {len(rooms)} rooms")
        
        # Validate input data
        if self.validate_input_data(students, rooms):
            self.logger.debug("Input data validation passed")
        
        # Build room lookup for efficient access
        room_lookup = self._build_room_lookup(rooms)
        
        # Group students by room assignment
        students_by_room, unassigned_students = self._group_students_by_room(students, room_lookup)
        
        # Build result with rooms and their assigned students
        result = self._build_combined_rooms(rooms, students_by_room)
        
        # Add unassigned students if any exist
        if unassigned_students:
            unassigned_room = CombinedRoom(
                id=None,
                name='Unassigned Students',
                students=unassigned_students
            )
            result.append(unassigned_room.to_dict())
        
        self.logger.info(f"Successfully combined data into {len(result)} room groups")
        return result
    
    def validate_input_data(self, students: List[Dict[str, Any]], rooms: List[Dict[str, Any]]) -> bool:
        """
        Validate input data before processing.
        
        Args:
            students: Students data to validate
            rooms: Rooms data to validate
            
        Returns:
            True if data is valid
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            validate_students_data(students)
            validate_rooms_data(rooms)
            
            # Additional business logic validation
            self._validate_business_rules(students, rooms)
            
            return True
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Input validation failed: {e}")
    
    def _build_room_lookup(self, rooms: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        """Build efficient room lookup dictionary."""
        room_lookup = {}
        for room in rooms:
            room_id = room.get('id')
            if room_id is not None:
                room_lookup[room_id] = room
        return room_lookup
    
    def _group_students_by_room(self, students: List[Dict[str, Any]], room_lookup: Dict[int, Dict[str, Any]]) -> tuple:
        """Group students by their room assignment."""
        students_by_room = {}
        unassigned_students = []
        
        for student in students:
            room_id = student.get('room')
            student_data = {
                'id': student.get('id'),
                'name': student.get('name', 'Unknown')
            }
            
            if room_id is not None and room_id in room_lookup:
                # Student assigned to existing room
                if room_id not in students_by_room:
                    students_by_room[room_id] = []
                students_by_room[room_id].append(student_data)
            else:
                # Student unassigned or assigned to non-existent room
                unassigned_students.append(student_data)
        
        return students_by_room, unassigned_students
    
    def _build_combined_rooms(self, rooms: List[Dict[str, Any]], students_by_room: Dict[int, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Build final combined room structures."""
        result = []
        
        for room in rooms:
            room_id = room.get('id')
            combined_room = CombinedRoom(
                id=room_id,
                name=room.get('name', 'Unknown Room'),
                students=students_by_room.get(room_id, [])
            )
            result.append(combined_room.to_dict())
        
        return result
    
    def _validate_business_rules(self, students: List[Dict[str, Any]], rooms: List[Dict[str, Any]]) -> None:
        """Validate business-specific rules."""
        # Check for duplicate room IDs
        room_ids = [room.get('id') for room in rooms if room.get('id') is not None]
        if len(room_ids) != len(set(room_ids)):
            raise ValidationError("Duplicate room IDs found")
        
        # Check for duplicate student IDs
        student_ids = [student.get('id') for student in students if student.get('id') is not None]
        if len(student_ids) != len(set(student_ids)):
            raise ValidationError("Duplicate student IDs found")
