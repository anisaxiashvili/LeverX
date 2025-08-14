"""Data loader interface definition."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol


class DataLoaderInterface(ABC):
    """Abstract interface for data loading operations."""
    
    @abstractmethod
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load students data from file.
        
        Args:
            file_path: Path to the students data file
            
        Returns:
            List of student dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        pass
    
    @abstractmethod
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load rooms data from file.
        
        Args:
            file_path: Path to the rooms data file
            
        Returns:
            List of room dictionaries
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        pass
    
    @abstractmethod
    def validate_data_format(self, data: List[Dict[str, Any]], data_type: str) -> bool:
        """
        Validate loaded data format.
        
        Args:
            data: Loaded data to validate
            data_type: Type of data ('students' or 'rooms')
            
        Returns:
            True if valid, False otherwise
        """
        pass
