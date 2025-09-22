"""
Test for the simulator functionality
"""

import pytest
from pydantic import BaseModel, Field
from guilite.simulator import Simulator, SimulatorRegistry


class SimpleInput(BaseModel):
    x: int = Field(..., description="First number")
    y: int = Field(..., description="Second number")


class SimpleOutput(BaseModel):
    result: int = Field(..., description="Result of computation")
    operation: str = Field(..., description="Operation performed")


def simple_computation(input_data: SimpleInput) -> SimpleOutput:
    """Simple computation function for testing."""
    result = input_data.x + input_data.y
    return SimpleOutput(result=result, operation="addition")


def test_simulator_creation():
    """Test creating a simulator."""
    simulator = Simulator(
        name="Test Simulator",
        description="A test simulator",
        input_model=SimpleInput,
        output_model=SimpleOutput,
        computation_func=simple_computation
    )
    
    assert simulator.name == "Test Simulator"
    assert simulator.description == "A test simulator"
    assert simulator.input_model == SimpleInput
    assert simulator.output_model == SimpleOutput


def test_simulator_run_success():
    """Test successful simulation run."""
    simulator = Simulator(
        name="Test Simulator",
        description="A test simulator",
        input_model=SimpleInput,
        output_model=SimpleOutput,
        computation_func=simple_computation
    )
    
    result = simulator.run({"x": 5, "y": 3})
    
    assert result.success is True
    assert result.output.result == 8
    assert result.output.operation == "addition"
    assert result.execution_time is not None
    assert result.execution_time > 0


def test_simulator_run_validation_error():
    """Test simulation run with validation error."""
    simulator = Simulator(
        name="Test Simulator",
        description="A test simulator",
        input_model=SimpleInput,
        output_model=SimpleOutput,
        computation_func=simple_computation
    )
    
    result = simulator.run({"x": "invalid", "y": 3})
    
    assert result.success is False
    assert "Validation error" in result.error
    assert result.output is None


def test_simulator_registry():
    """Test simulator registry functionality."""
    registry = SimulatorRegistry()
    
    simulator = Simulator(
        name="Test Simulator",
        description="A test simulator",
        input_model=SimpleInput,
        output_model=SimpleOutput,
        computation_func=simple_computation
    )
    
    # Register simulator
    registry.register(simulator)
    
    # Test retrieval
    retrieved = registry.get("Test Simulator")
    assert retrieved is not None
    assert retrieved.name == "Test Simulator"
    
    # Test listing
    simulators = registry.list_simulators()
    assert "Test Simulator" in simulators
    assert simulators["Test Simulator"]["description"] == "A test simulator"
    
    # Test removal
    removed = registry.remove("Test Simulator")
    assert removed is True
    assert registry.get("Test Simulator") is None


def test_simulator_example_input():
    """Test example input generation."""
    simulator = Simulator(
        name="Test Simulator",
        description="A test simulator",
        input_model=SimpleInput,
        output_model=SimpleOutput,
        computation_func=simple_computation
    )
    
    example = simulator.create_example_input()
    
    assert "x" in example
    assert "y" in example
    assert isinstance(example["x"], int)
    assert isinstance(example["y"], int)


if __name__ == "__main__":
    # Run simple tests
    test_simulator_creation()
    test_simulator_run_success()
    test_simulator_run_validation_error()
    test_simulator_registry()
    test_simulator_example_input()
    print("All simulator tests passed!")