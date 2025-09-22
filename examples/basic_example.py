"""
Example usage of the Guilite library.

This example demonstrates:
1. Creating Pydantic models for input and output
2. Defining a computation function
3. Setting up a simulator
4. Running the web interface
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from guilite import ReportGenerator, Simulator, WebInterface


# Define input and output models using Pydantic
class CalculationInput(BaseModel):
    """Input model for mathematical calculations."""
    numbers: List[float] = Field(..., description="List of numbers to process")
    operation: str = Field(..., description="Operation to perform (sum, mean, max, min)")
    precision: Optional[int] = Field(2, description="Number of decimal places for result")


class CalculationOutput(BaseModel):
    """Output model for calculation results."""
    result: float = Field(..., description="Result of the calculation")
    operation: str = Field(..., description="Operation that was performed")
    input_count: int = Field(..., description="Number of input values")
    summary: str = Field(..., description="Human-readable summary")


class DataAnalysisInput(BaseModel):
    """Input model for data analysis."""
    dataset_name: str = Field(..., description="Name of the dataset")
    values: List[float] = Field(..., description="Numerical values to analyze")
    include_variance: bool = Field(True, description="Whether to calculate variance")


class DataAnalysisOutput(BaseModel):
    """Output model for data analysis results."""
    dataset_name: str
    count: int
    mean: float
    median: float
    std_deviation: Optional[float] = None
    variance: Optional[float] = None
    min_value: float
    max_value: float
    range_value: float


# Define computation functions
def math_calculator(input_data: CalculationInput) -> CalculationOutput:
    """Perform mathematical calculations on a list of numbers."""
    numbers = input_data.numbers
    operation = input_data.operation.lower()
    
    if not numbers:
        raise ValueError("No numbers provided")
    
    if operation == "sum":
        result = sum(numbers)
    elif operation == "mean":
        result = sum(numbers) / len(numbers)
    elif operation == "max":
        result = max(numbers)
    elif operation == "min":
        result = min(numbers)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    # Apply precision
    if input_data.precision is not None:
        result = round(result, input_data.precision)
    
    summary = f"Calculated {operation} of {len(numbers)} numbers: {result}"
    
    return CalculationOutput(
        result=result,
        operation=operation,
        input_count=len(numbers),
        summary=summary
    )


def data_analyzer(input_data: DataAnalysisInput) -> DataAnalysisOutput:
    """Perform statistical analysis on a dataset."""
    values = input_data.values
    
    if not values:
        raise ValueError("No values provided for analysis")
    
    # Calculate basic statistics
    count = len(values)
    mean = sum(values) / count
    sorted_values = sorted(values)
    
    # Calculate median
    if count % 2 == 0:
        median = (sorted_values[count//2-1] + sorted_values[count//2]) / 2
    else:
        median = sorted_values[count//2]
    
    min_value = min(values)
    max_value = max(values)
    range_value = max_value - min_value
    
    # Calculate variance and standard deviation if requested
    variance = None
    std_deviation = None
    
    if input_data.include_variance and count > 1:
        variance = sum((x - mean) ** 2 for x in values) / (count - 1)
        std_deviation = variance ** 0.5
    
    return DataAnalysisOutput(
        dataset_name=input_data.dataset_name,
        count=count,
        mean=round(mean, 4),
        median=median,
        std_deviation=round(std_deviation, 4) if std_deviation else None,
        variance=round(variance, 4) if variance else None,
        min_value=min_value,
        max_value=max_value,
        range_value=range_value
    )


def main():
    """Main function to set up and run the web interface."""
    
    # Create simulators
    calculator_sim = Simulator(
        name="Math Calculator",
        description="Performs basic mathematical operations (sum, mean, max, min) on a list of numbers.",
        input_model=CalculationInput,
        output_model=CalculationOutput,
        computation_func=math_calculator
    )
    
    analyzer_sim = Simulator(
        name="Data Analyzer",
        description="Performs statistical analysis on numerical datasets including mean, median, variance, and more.",
        input_model=DataAnalysisInput,
        output_model=DataAnalysisOutput,
        computation_func=data_analyzer
    )
    
    # Create web interface and register simulators
    web_interface = WebInterface()
    web_interface.register_simulator(calculator_sim)
    web_interface.register_simulator(analyzer_sim)
    
    print("Starting Guilite web interface...")
    print("Available simulators:")
    print("- Math Calculator: Basic mathematical operations")
    print("- Data Analyzer: Statistical analysis of datasets")
    print("\nOpen your browser and go to: http://127.0.0.1:5000")
    
    # Run the web interface
    web_interface.run(debug=True)


if __name__ == "__main__":
    main()