"""CLI controller orchestrating the application flow."""
import sys
import logging
from typing import Optional, List

from .argument_parser import ArgumentParser, ParsedArguments
from .cli_config import CLIConfig
from ..data.loaders.loader_factory import DataLoaderFactory
from ..data.exporters.exporter_factory import DataExporterFactory
from ..services.room_student_service import RoomStudentService
from ..exceptions.custom_exceptions import (
    StudentRoomManagerError,
    DataLoadError,
    DataExportError,
    UnsupportedFormatError,
    ValidationError
)
from ..utils.logging_config import setup_logging


class CLIController:
    """Main CLI controller coordinating application execution."""
    
    def __init__(self, config: CLIConfig = None):
        self.config = config or CLIConfig()
        self.argument_parser = ArgumentParser(self.config)
        self.logger = None  # Will be initialized after parsing args
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Execute the CLI application.
        
        Args:
            args: Optional command line arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        try:
            # Parse command line arguments
            parsed_args = self.argument_parser.parse(args)
            
            # Setup logging based on arguments
            self._setup_logging(parsed_args)
            
            # Execute main application logic
            self._execute_application(parsed_args)
            
            if not parsed_args.quiet:
                print(f"✅ Successfully processed data and saved to: {parsed_args.output_file}")
            
            return 0
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user", file=sys.stderr)
            return 130
        except SystemExit as e:
            return e.code if e.code is not None else 1
        except Exception as e:
            self._handle_error(e)
            return 1
    
    def _setup_logging(self, args: ParsedArguments) -> None:
        """Setup logging configuration based on CLI arguments."""
        if args.quiet:
            log_level = "ERROR"
        elif args.verbose:
            log_level = "DEBUG"
        else:
            log_level = "INFO"
        
        self.logger = setup_logging(log_level)
    
    def _execute_application(self, args: ParsedArguments) -> None:
        """Execute the main application logic."""
        self.logger.info(f"Starting {self.config.PROGRAM_NAME} v{self.config.PROGRAM_VERSION}")
        self.logger.debug(f"Arguments: {args}")
        
        # Load data
        students_data, rooms_data = self._load_input_data(args)
        
        # Process data
        combined_data = self._process_data(students_data, rooms_data)
        
        # Export results
        self._export_data(combined_data, args)
        
        self.logger.info("Application completed successfully")
    
    def _load_input_data(self, args: ParsedArguments) -> tuple:
        """Load students and rooms data from input files."""
        try:
            loader = DataLoaderFactory.create_loader('json')
            
            self.logger.info(f"Loading students from: {args.students_file}")
            students_data = loader.load_students(args.students_file)
            
            self.logger.info(f"Loading rooms from: {args.rooms_file}")
            rooms_data = loader.load_rooms(args.rooms_file)
            
            return students_data, rooms_data
            
        except DataLoadError as e:
            raise DataLoadError(f"Failed to load input data: {e}")
        except Exception as e:
            raise DataLoadError(f"Unexpected error during data loading: {e}")
    
    def _process_data(self, students_data: List, rooms_data: List) -> List:
        """Process and combine the loaded data."""
        try:
            service = RoomStudentService()
            
            self.logger.info("Processing and combining data...")
            combined_data = service.combine_data(students_data, rooms_data)
            
            self.logger.debug(f"Generated {len(combined_data)} combined room records")
            return combined_data
            
        except ValidationError as e:
            raise ValidationError(f"Data processing failed: {e}")
        except Exception as e:
            raise ValidationError(f"Unexpected error during data processing: {e}")
    
    def _export_data(self, data: List, args: ParsedArguments) -> None:
        """Export processed data to the specified format."""
        try:
            exporter = DataExporterFactory.create_exporter(args.output_format)
            
            self.logger.info(f"Exporting data in {args.output_format.upper()} format to: {args.output_file}")
            exporter.export(data, args.output_file)
            
        except DataExportError as e:
            raise DataExportError(f"Failed to export data: {e}")
        except UnsupportedFormatError as e:
            raise UnsupportedFormatError(e.format_name, e.supported_formats)
        except Exception as e:
            raise DataExportError(f"Unexpected error during data export: {e}")
    
    def _handle_error(self, error: Exception) -> None:
        """Handle and display errors appropriately."""
        error_prefix = "❌ Error:"
        
        if isinstance(error, DataLoadError):
            print(f"{error_prefix} {error}", file=sys.stderr)
            if error.file_path:
                print(f"   File: {error.file_path}", file=sys.stderr)
        elif isinstance(error, DataExportError):
            print(f"{error_prefix} {error}", file=sys.stderr)
            if error.output_path:
                print(f"   Output: {error.output_path}", file=sys.stderr)
        elif isinstance(error, ValidationError):
            print(f"{error_prefix} {error}", file=sys.stderr)
        elif isinstance(error, UnsupportedFormatError):
            print(f"{error_prefix} {error}", file=sys.stderr)
        elif isinstance(error, StudentRoomManagerError):
            print(f"{error_prefix} {error}", file=sys.stderr)
        else:
            print(f"{error_prefix} Unexpected error: {error}", file=sys.stderr)
        
        # Log full traceback in debug mode
        if self.logger and self.logger.isEnabledFor(logging.DEBUG):
            self.logger.exception("Full error traceback:")

