"""Service interface definition."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class RoomStudentServiceInterface(ABC):
    """Interface for room-student business logic operations."""
    
    @abstractmethod
    def combine_data(self, students: List[Dict[str, Any]], rooms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine students and rooms data according to business rules.
        
        Args:
            students: List of student data
            rooms: List of room data
            
        Returns:
            Combined data structure
        """
        pass
    
    @abstractmethod
    def validate_input_data(self, students: List[Dict[str, Any]], rooms: List[Dict[str, Any]]) -> bool:
        """
        Validate input data before processing.
        
        Args:
            students: Students data to validate
            rooms: Rooms data to validate
            
        Returns:
            True if data is valid
        """
        pass