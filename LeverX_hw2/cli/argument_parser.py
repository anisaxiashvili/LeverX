"""Command line argument parsing."""
import argparse
from dataclasses import dataclass
from typing import List, Optional

from .cli_config import CLIConfig
from ..data.exporters.exporter_factory import DataExporterFactory


@dataclass
class ParsedArguments:
    """Container for parsed command line arguments."""
    students_file: str
    rooms_file: str
    output_file: str
    output_format: str
    verbose: bool = False
    quiet: bool = False


class ArgumentParser:
    """Handles command line argument parsing with validation."""
    
    def __init__(self, config: CLIConfig = None):
        self.config = config or CLIConfig()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            prog=self.config.PROGRAM_NAME,
            description=self.config.PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_epilog()
        )
        
        # Version argument
        parser.add_argument(
            '--version',
            action='version',
            version=f'{self.config.PROGRAM_NAME} {self.config.PROGRAM_VERSION}'
        )
        
        # Required arguments
        parser.add_argument(
            '--students',
            required=True,
            metavar='FILE',
            help=self.config.STUDENTS_HELP
        )
        
        parser.add_argument(
            '--rooms',
            required=True,
            metavar='FILE',
            help=self.config.ROOMS_HELP
        )
        
        # Optional arguments
        parser.add_argument(
            '--out',
            default=self.config.DEFAULT_OUTPUT_FILE,
            metavar='FILE',
            help=self.config.OUTPUT_HELP
        )
        
        parser.add_argument(
            '--format',
            default=self.config.DEFAULT_OUTPUT_FORMAT,
            choices=DataExporterFactory.get_supported_formats(),
            help=self.config.FORMAT_HELP
        )
        
        # Logging arguments
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        
        parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            help='Suppress non-error output'
        )
        
        return parser
    
    def parse(self, args: Optional[List[str]] = None) -> ParsedArguments:
        """
        Parse command line arguments.
        
        Args:
            args: Optional list of arguments (uses sys.argv if None)
            
        Returns:
            ParsedArguments object with validated arguments
        """
        parsed = self.parser.parse_args(args)
        
        # Validate argument combinations
        if parsed.verbose and parsed.quiet:
            self.parser.error("--verbose and --quiet are mutually exclusive")
        
        return ParsedArguments(
            students_file=parsed.students,
            rooms_file=parsed.rooms,
            output_file=parsed.out,
            output_format=parsed.format,
            verbose=parsed.verbose,
            quiet=parsed.quiet
        )
    
    def _get_epilog(self) -> str:
        """Get epilog text for help message."""
        supported_formats = ', '.join(DataExporterFactory.get_supported_formats())
        return f"""
Examples:
  {self.config.PROGRAM_NAME} --students data/students.json --rooms data/rooms.json
  {self.config.PROGRAM_NAME} --students students.json --rooms rooms.json --out result.xml --format xml
  {self.config.PROGRAM_NAME} --students students.json --rooms rooms.json --format json --verbose

Supported output formats: {supported_formats}
"""

