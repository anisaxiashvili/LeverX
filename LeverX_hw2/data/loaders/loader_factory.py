"""Factory for creating data loaders."""
from typing import Dict, Type, List
from ...interfaces.data_loader_interface import DataLoaderInterface
from ...exceptions.custom_exceptions import UnsupportedFormatError
from .json_loader import JSONDataLoader


class DataLoaderFactory:
    """Factory for creating appropriate data loader instances."""
    
    _loaders: Dict[str, Type[DataLoaderInterface]] = {
        'json': JSONDataLoader,
    }
    
    @classmethod
    def create_loader(cls, format_name: str) -> DataLoaderInterface:
        """
        Create a data loader for the specified format.
        
        Args:
            format_name: Format name (e.g., 'json')
            
        Returns:
            DataLoaderInterface implementation
            
        Raises:
            UnsupportedFormatError: If format is not supported
        """
        format_lower = format_name.lower()
        loader_class = cls._loaders.get(format_lower)
        
        if not loader_class:
            supported = list(cls._loaders.keys())
            raise UnsupportedFormatError(format_name, supported)
        
        return loader_class()
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Get list of supported loader formats."""
        return list(cls._loaders.keys())
    
    @classmethod
    def register_loader(cls, format_name: str, loader_class: Type[DataLoaderInterface]) -> None:
        """
        Register a new loader format.
        
        Args:
            format_name: Format name
            loader_class: Loader class implementing DataLoaderInterface
        """
        cls._loaders[format_name.lower()] = loader_class


