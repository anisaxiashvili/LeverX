__version__ = "1.2.0"
__author__ = "Student Room Manager Team"
__description__ = "Combine student and room data with flexible output formats"

from .services.room_student_service import RoomStudentService
from .data.loaders.loader_factory import DataLoaderFactory
from .data.exporters.exporter_factory import DataExporterFactory
from .cli.cli_controller import CLIController
from .models.student import Student
from .models.room import Room
from .models.combined_room import CombinedRoom

__all__ = [
    'RoomStudentService',
    'DataLoaderFactory', 
    'DataExporterFactory',
    'CLIController',
    'Student',
    'Room',
    'CombinedRoom',
    '__version__'
]
