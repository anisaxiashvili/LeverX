"""XML data exporter implementation."""
import logging
from pathlib import Path
from typing import List, Dict, Any
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from ...interfaces.data_exporter_interface import DataExporterInterface
from ...exceptions.custom_exceptions import DataExportError


class XMLExporter(DataExporterInterface):
    """XML implementation of the data exporter interface."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def export(self, data: List[Dict[str, Any]], output_path: str) -> None:
        """
        Export data to XML format.
        
        Args:
            data: Data to export
            output_path: Path where to save the XML file
            
        Raises:
            DataExportError: If export fails
        """
        try:
            self.logger.info(f"Exporting data to XML: {output_path}")
            
            if self.validate_output_data(data):
                xml_content = self._generate_xml(data)
                
                # Ensure directory exists
                output_path_obj = Path(output_path)
                output_path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path_obj, 'w', encoding='utf-8') as file:
                    file.write(xml_content)
                
                self.logger.info(f"Successfully exported {len(data)} records to XML")
            
        except Exception as e:
            raise DataExportError(f"Failed to export XML data: {e}", output_path)
    
    def get_file_extension(self) -> str:
        """Get XML file extension."""
        return '.xml'
    
    def validate_output_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate data before XML export.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid for export
            
        Raises:
            DataExportError: If validation fails
        """
        if not isinstance(data, list):
            raise DataExportError("Data must be a list for XML export")
        
        for i, record in enumerate(data):
            if not isinstance(record, dict):
                raise DataExportError(f"Record at index {i} must be a dictionary")
            
            required_fields = ['id', 'name', 'students']
            for field in required_fields:
                if field not in record:
                    raise DataExportError(f"Record at index {i} missing required field: {field}")
        
        return True
    
    def _generate_xml(self, data: List[Dict[str, Any]]) -> str:
        """
        Generate XML content from data.
        
        Args:
            data: Data to convert to XML
            
        Returns:
            Formatted XML string
        """
        root = Element('rooms')
        
        for room_data in data:
            room_element = SubElement(root, 'room')
            
            # Room ID
            id_element = SubElement(room_element, 'id')
            room_id = room_data.get('id')
            id_element.text = str(room_id) if room_id is not None else ''
            
            # Room name
            name_element = SubElement(room_element, 'name')
            name_element.text = self._escape_xml_content(str(room_data.get('name', '')))
            
            # Students
            students_element = SubElement(room_element, 'students')
            for student in room_data.get('students', []):
                student_element = SubElement(students_element, 'student')
                
                student_id_element = SubElement(student_element, 'id')
                student_id_element.text = str(student.get('id', ''))
                
                student_name_element = SubElement(student_element, 'name')
                student_name_element.text = self._escape_xml_content(str(student.get('name', '')))
        
        # Pretty print
        rough_string = tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent='  ')
    
    def _escape_xml_content(self, content: str) -> str:
        """
        Escape XML special characters.
        
        Args:
            content: Content to escape
            
        Returns:
            Escaped content
        """
        if not isinstance(content, str):
            content = str(content)
        
        # Basic XML escaping
        content = content.replace('&', '&amp;')
        content = content.replace('<', '&lt;')
        content = content.replace('>', '&gt;')
        content = content.replace('"', '&quot;')
        content = content.replace("'", '&apos;')
        
        return content