"""Data exporter interface definition."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataExporterInterface(ABC):
    """Abstract interface for data export operations."""
    
    @abstractmethod
    def export(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Export data to specified format and location.
        
        Args:
            data: Data to export
            output_path: Path where to save the exported data
            
        Raises:
            PermissionError: If cannot write to output path
            ValueError: If data format is invalid
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Get the file extension for this exporter.
        
        Returns:
            File extension (e.g., '.json', '.xml')
        """
        pass
    
    @abstractmethod
    def validate_output_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate data before export.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid for export
        """
        pass

