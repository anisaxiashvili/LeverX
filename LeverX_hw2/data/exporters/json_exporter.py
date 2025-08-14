"""JSON data exporter implementation."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from ...interfaces.data_exporter_interface import DataExporterInterface
from ...exceptions.custom_exceptions import DataExportError


class JSONExporter(DataExporterInterface):
    """JSON implementation of the data exporter interface."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def export(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Export data to JSON format.
        
        Args:
            data: Data to export
            output_path: Path where to save the JSON file
            
        Raises:
            DataExportError: If export fails
        """
        try:
            self.logger.info(f"Exporting data to JSON: {output_path}")
            
            if self.validate_output_data(data):
                # Ensure directory exists
                output_path_obj = Path(output_path)
                output_path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path_obj, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                
                self.logger.info(f"Successfully exported {len(data)} records to JSON")
            
        except Exception as e:
            raise DataExportError(f"Failed to export JSON data: {e}", output_path)
    
    def get_file_extension(self) -> str:
        """Get JSON file extension."""
        return '.json'
    
    def validate_output_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate data before JSON export.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid for export
            
        Raises:
            DataExportError: If validation fails
        """
        if not isinstance(data, list):
            raise DataExportError("Data must be a list for JSON export")
        
        # Validate each record
        for i, record in enumerate(data):
            if not isinstance(record, dict):
                raise DataExportError(f"Record at index {i} must be a dictionary")
            
            # Check for required fields
            required_fields = ['id', 'name', 'students']
            for field in required_fields:
                if field not in record:
                    raise DataExportError(f"Record at index {i} missing required field: {field}")
        
        return True
