"""Application settings and configuration."""
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # Supported formats
    SUPPORTED_LOADER_FORMATS: List[str] = None
    SUPPORTED_EXPORTER_FORMATS: List[str] = None
    
    # Default values
    DEFAULT_OUTPUT_FORMAT: str = "json"
    DEFAULT_OUTPUT_FILENAME: str = "combined.json"
    
    # Validation settings
    VALIDATE_INPUT_DATA: bool = True
    VALIDATE_OUTPUT_DATA: bool = True
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = None
    
    def __post_init__(self):
        if self.SUPPORTED_LOADER_FORMATS is None:
            self.SUPPORTED_LOADER_FORMATS = ["json"]
        
        if self.SUPPORTED_EXPORTER_FORMATS is None:
            self.SUPPORTED_EXPORTER_FORMATS = ["json", "xml"]


# Global configuration instance
APP_CONFIG = AppConfig()