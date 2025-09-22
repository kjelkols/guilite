# Guilite

A very lightweight GUI library for input-output oriented programs.

## Features

Guilite provides a simple framework for creating web-based interfaces for computational programs using:

- **HTML Report Generation**: Generate beautiful HTML reports from Pydantic data structures
- **Simulator Framework**: Create standardized interfaces for programs with validated input/output using Pydantic models
- **Web Interface**: Minimal Flask application for GUI access to your simulators

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from pydantic import BaseModel, Field
from guilite import Simulator, WebInterface

# Define your data models
class CalculationInput(BaseModel):
    numbers: list[float] = Field(..., description="Numbers to process")
    operation: str = Field(..., description="Operation (sum, mean, max, min)")

class CalculationOutput(BaseModel):
    result: float = Field(..., description="Calculation result")
    summary: str = Field(..., description="Summary of the operation")

# Define your computation function
def calculate(input_data: CalculationInput) -> CalculationOutput:
    numbers = input_data.numbers
    op = input_data.operation.lower()
    
    if op == "sum":
        result = sum(numbers)
    elif op == "mean":
        result = sum(numbers) / len(numbers)
    elif op == "max":
        result = max(numbers)
    elif op == "min":
        result = min(numbers)
    else:
        raise ValueError(f"Unknown operation: {op}")
    
    return CalculationOutput(
        result=result,
        summary=f"Calculated {op} of {len(numbers)} numbers: {result}"
    )

# Create and register simulator
simulator = Simulator(
    name="Calculator",
    description="Basic mathematical operations",
    input_model=CalculationInput,
    output_model=CalculationOutput,
    computation_func=calculate
)

# Set up web interface
web = WebInterface()
web.register_simulator(simulator)
web.run()
```

Then open your browser to `http://127.0.0.1:5000` to access the web interface.

## Examples

See the `examples/` directory for complete working examples:

- `basic_example.py`: Demonstrates math calculator and data analysis simulators

To run the example:

```bash
cd examples
python basic_example.py
```

## Architecture

### Report Generator
- Converts Pydantic models to structured HTML reports
- Customizable templates using Jinja2
- Automatic type detection and formatting

### Simulator Framework  
- Standardized interface for computational programs
- Input/output validation using Pydantic
- Error handling and execution timing
- Schema introspection and example generation

### Web Interface
- Flask-based web application
- Interactive forms for input data
- Real-time result display with HTML reports
- RESTful API for programmatic access

## Testing

Run tests with:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python tests/test_report_generator.py
python tests/test_simulator.py
```

## License

MIT License - see LICENSE file for details.
