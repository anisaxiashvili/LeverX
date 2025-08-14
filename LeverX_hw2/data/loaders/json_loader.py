"""JSON data loader implementation."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from ...interfaces.data_loader_interface import DataLoaderInterface
from ...exceptions.custom_exceptions import DataLoadError, ValidationError
from ...utils.validation import validate_file_path, validate_students_data, validate_rooms_data


class JSONDataLoader(DataLoaderInterface):
    """JSON implementation of the data loader interface."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load students data from JSON file.
        
        Args:
            file_path: Path to the JSON file containing students data
            
        Returns:
            List of student dictionaries
            
        Raises:
            DataLoadError: If file cannot be loaded or parsed
        """
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading students from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise DataLoadError(f"Students file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if self.validate_data_format(data, 'students'):
                self.logger.info(f"Successfully loaded {len(data)} students")
                return data
            
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON format in students file: {e}", file_path)
        except Exception as e:
            raise DataLoadError(f"Failed to load students data: {e}", file_path)
    
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load rooms data from JSON file.
        
        Args:
            file_path: Path to the JSON file containing rooms data
            
        Returns:
            List of room dictionaries
            
        Raises:
            DataLoadError: If file cannot be loaded or parsed
        """
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading rooms from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise DataLoadError(f"Rooms file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if self.validate_data_format(data, 'rooms'):
                self.logger.info(f"Successfully loaded {len(data)} rooms")
                return data
            
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Invalid JSON format in rooms file: {e}", file_path)
        except Exception as e:
            raise DataLoadError(f"Failed to load rooms data: {e}", file_path)
    
    def validate_data_format(self, data: List[Dict[str, Any]], data_type: str) -> bool:
        """
        Validate loaded data format.
        
        Args:
            data: Loaded data to validate
            data_type: Type of data ('students' or 'rooms')
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If data format is invalid
        """
        try:
            if data_type == 'students':
                validate_students_data(data)
            elif data_type == 'rooms':
                validate_rooms_data(data)
            else:
                raise ValidationError(f"Unknown data type: {data_type}")
            
            return True
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Data validation failed: {e}")

