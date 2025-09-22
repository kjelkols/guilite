"""
Report Generator - Generate HTML reports from Pydantic data structures
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from jinja2 import Template


class ReportGenerator:
    """Generate HTML reports from Pydantic data structures."""
    
    def __init__(self, template: Optional[str] = None):
        """
        Initialize the report generator.
        
        Args:
            template: Optional custom HTML template. If None, uses default template.
        """
        self.template = template or self._get_default_template()
        self.jinja_template = Template(self.template)
    
    def generate_html(self, data: BaseModel, title: str = "Report") -> str:
        """
        Generate HTML report from Pydantic model.
        
        Args:
            data: Pydantic model instance containing the data
            title: Title for the HTML report
            
        Returns:
            HTML string representation of the data
        """
        if not isinstance(data, BaseModel):
            raise ValueError("Data must be a Pydantic BaseModel instance")
        
        # Convert Pydantic model to dictionary
        data_dict = data.model_dump()
        
        # Generate HTML table structure
        html_content = self._generate_table_from_dict(data_dict)
        
        return self.jinja_template.render(
            title=title,
            content=html_content,
            model_name=data.__class__.__name__
        )
    
    def _generate_table_from_dict(self, data: Dict[str, Any], level: int = 0) -> str:
        """
        Generate HTML table from dictionary data.
        
        Args:
            data: Dictionary containing the data
            level: Nesting level for styling
            
        Returns:
            HTML table string
        """
        if not data:
            return "<p>No data available</p>"
        
        indent = "  " * level
        table_class = f"level-{level}"
        
        html = f'{indent}<table class="data-table {table_class}">\n'
        
        for key, value in data.items():
            html += f'{indent}  <tr>\n'
            html += f'{indent}    <td class="key">{self._format_key(key)}</td>\n'
            html += f'{indent}    <td class="value">{self._format_value(value, level + 1)}</td>\n'
            html += f'{indent}  </tr>\n'
        
        html += f'{indent}</table>\n'
        return html
    
    def _format_key(self, key: str) -> str:
        """Format dictionary key for display."""
        # Convert snake_case to Title Case
        return key.replace('_', ' ').title()
    
    def _format_value(self, value: Any, level: int = 0) -> str:
        """
        Format value for HTML display.
        
        Args:
            value: Value to format
            level: Current nesting level
            
        Returns:
            Formatted HTML string
        """
        if value is None:
            return '<span class="null">None</span>'
        elif isinstance(value, bool):
            return f'<span class="boolean">{str(value)}</span>'
        elif isinstance(value, (int, float)):
            return f'<span class="number">{value}</span>'
        elif isinstance(value, str):
            return f'<span class="string">{self._escape_html(value)}</span>'
        elif isinstance(value, list):
            return self._format_list(value, level)
        elif isinstance(value, dict):
            return self._generate_table_from_dict(value, level)
        else:
            return f'<span class="other">{self._escape_html(str(value))}</span>'
    
    def _format_list(self, items: List[Any], level: int = 0) -> str:
        """Format list for HTML display."""
        if not items:
            return '<span class="empty-list">[]</span>'
        
        html = '<ul class="data-list">\n'
        for item in items:
            html += f'  <li>{self._format_value(item, level)}</li>\n'
        html += '</ul>'
        return html
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML characters in text."""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    def _get_default_template(self) -> str:
        """Return default HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .model-info {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-style: italic;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }
        .data-table.level-0 {
            border: 2px solid #3498db;
        }
        .data-table td {
            padding: 12px;
            border: 1px solid #ddd;
            vertical-align: top;
        }
        .data-table .key {
            background-color: #f8f9fa;
            font-weight: bold;
            width: 25%;
            color: #2c3e50;
        }
        .data-table .value {
            background-color: white;
        }
        .data-table tr:nth-child(even) .key {
            background-color: #e9ecef;
        }
        .data-list {
            margin: 0;
            padding-left: 20px;
        }
        .data-list li {
            margin-bottom: 5px;
        }
        .string { color: #27ae60; }
        .number { color: #e74c3c; font-weight: bold; }
        .boolean { color: #8e44ad; font-weight: bold; }
        .null { color: #95a5a6; font-style: italic; }
        .empty-list { color: #95a5a6; font-style: italic; }
        .other { color: #34495e; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <div class="model-info">
            Data from model: <strong>{{ model_name }}</strong>
        </div>
        {{ content|safe }}
    </div>
</body>
</html>"""