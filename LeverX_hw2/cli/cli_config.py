"""CLI configuration settings."""
from dataclasses import dataclass
from typing import List


@dataclass
class CLIConfig:
    """Configuration for CLI options and defaults."""
    
    # Default values
    DEFAULT_OUTPUT_FORMAT: str = "json"
    DEFAULT_OUTPUT_FILE: str = "combined.json"
    
    # Supported formats
    SUPPORTED_OUTPUT_FORMATS: List[str] = None
    
    # Program metadata
    PROGRAM_NAME: str = "student-room-manager"
    PROGRAM_DESCRIPTION: str = "Combine student and room data with flexible output formats"
    PROGRAM_VERSION: str = "1.2.0"
    
    # Help messages
    STUDENTS_HELP: str = "Path to JSON file containing students data"
    ROOMS_HELP: str = "Path to JSON file containing rooms data"
    OUTPUT_HELP: str = "Output file path (default: combined.json)"
    FORMAT_HELP: str = "Output format: json or xml (default: json)"
    
    def __post_init__(self):
        if self.SUPPORTED_OUTPUT_FORMATS is None:
            self.SUPPORTED_OUTPUT_FORMATS = ["json", "xml"]
