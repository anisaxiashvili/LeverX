"""Factory for creating data exporters."""
from typing import Dict, Type, List
from ...interfaces.data_exporter_interface import DataExporterInterface
from ...exceptions.custom_exceptions import UnsupportedFormatError
from .json_exporter import JSONExporter
from .xml_exporter import XMLExporter


class DataExporterFactory:
    """Factory for creating appropriate data exporter instances."""
    
    _exporters: Dict[str, Type[DataExporterInterface]] = {
        'json': JSONExporter,
        'xml': XMLExporter,
    }
    
    @classmethod
    def create_exporter(cls, format_name: str) -> DataExporterInterface:
        """
        Create a data exporter for the specified format.
        
        Args:
            format_name: Format name (e.g., 'json', 'xml')
            
        Returns:
            DataExporterInterface implementation
            
        Raises:
            UnsupportedFormatError: If format is not supported
        """
        format_lower = format_name.lower()
        exporter_class = cls._exporters.get(format_lower)
        
        if not exporter_class:
            supported = list(cls._exporters.keys())
            raise UnsupportedFormatError(format_name, supported)
        
        return exporter_class()
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Get list of supported exporter formats."""
        return list(cls._exporters.keys())
    
    @classmethod
    def register_exporter(cls, format_name: str, exporter_class: Type[DataExporterInterface]) -> None:
        """
        Register a new exporter format.
        
        Args:
            format_name: Format name
            exporter_class: Exporter class implementing DataExporterInterface
        """
        cls._exporters[format_name.lower()] = exporter_class
