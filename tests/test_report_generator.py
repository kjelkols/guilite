"""
Test for the report generator functionality
"""

import pytest
from pydantic import BaseModel, Field
from guilite.report_generator import ReportGenerator


class SampleData(BaseModel):
    name: str = Field(..., description="Name of the item")
    value: int = Field(..., description="Numerical value")
    active: bool = Field(True, description="Whether the item is active")
    tags: list[str] = Field(default_factory=list, description="List of tags")


def test_report_generator_basic():
    """Test basic HTML generation from Pydantic model."""
    generator = ReportGenerator()
    
    data = SampleData(
        name="Test Item",
        value=42,
        active=True,
        tags=["important", "test"]
    )
    
    html = generator.generate_html(data, "Test Report")
    
    # Verify HTML structure
    assert "<!DOCTYPE html>" in html
    assert "Test Report" in html
    assert "Test Item" in html
    assert "42" in html
    assert "True" in html
    assert "important" in html
    assert "test" in html
    assert "SampleData" in html


def test_report_generator_empty_model():
    """Test HTML generation from empty model."""
    
    class EmptyModel(BaseModel):
        pass
    
    generator = ReportGenerator()
    data = EmptyModel()
    
    html = generator.generate_html(data, "Empty Report")
    
    assert "Empty Report" in html
    assert "EmptyModel" in html


def test_report_generator_nested_data():
    """Test HTML generation with nested data structures."""
    
    class NestedData(BaseModel):
        simple_field: str
        nested_dict: dict
        nested_list: list
    
    generator = ReportGenerator()
    data = NestedData(
        simple_field="test",
        nested_dict={"key1": "value1", "key2": 123},
        nested_list=[1, 2, {"nested": "value"}]
    )
    
    html = generator.generate_html(data, "Nested Report")
    
    assert "test" in html
    assert "Key1" in html  # Keys are converted to title case
    assert "value1" in html
    assert "123" in html
    assert "Nested" in html  # Keys are converted to title case


if __name__ == "__main__":
    # Run a simple test
    test_report_generator_basic()
    test_report_generator_empty_model()
    test_report_generator_nested_data()
    print("All report generator tests passed!")