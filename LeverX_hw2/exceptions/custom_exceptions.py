from typing import List
"""Custom exception classes for the application."""

class StudentRoomManagerError(Exception):
    """Base exception for Student Room Manager application."""
    pass


class DataLoadError(StudentRoomManagerError):
    """Exception raised when data loading fails."""
    
    def __init__(self, message: str, file_path: str = None):
        self.file_path = file_path
        super().__init__(message)


class DataExportError(StudentRoomManagerError):
    """Exception raised when data export fails."""
    
    def __init__(self, message: str, output_path: str = None):
        self.output_path = output_path
        super().__init__(message)


class ValidationError(StudentRoomManagerError):
    """Exception raised when data validation fails."""
    pass


class UnsupportedFormatError(StudentRoomManagerError):
    """Exception raised when unsupported format is requested."""
    
    def __init__(self, format_name: str, supported_formats: List[str]):
        self.format_name = format_name
        self.supported_formats = supported_formats
        message = f"Unsupported format '{format_name}'. Supported formats: {', '.join(supported_formats)}"
        super().__init__(message)

