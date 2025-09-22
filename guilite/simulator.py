"""
Simulator Framework - Interface for programs with Pydantic input/output structures
"""

from typing import Type, Callable, Any, Dict, Optional
from pydantic import BaseModel, ValidationError
import inspect
import traceback


class SimulationResult:
    """Container for simulation results and metadata."""
    
    def __init__(self, 
                 success: bool,
                 output: Optional[BaseModel] = None,
                 error: Optional[str] = None,
                 execution_time: Optional[float] = None):
        self.success = success
        self.output = output
        self.error = error
        self.execution_time = execution_time


class Simulator:
    """
    Framework for creating interfaces to programs with Pydantic input/output structures.
    
    This class provides a standardized way to:
    - Define input and output data structures using Pydantic
    - Execute computations with validation
    - Handle errors gracefully
    - Generate reports from results
    """
    
    def __init__(self, 
                 name: str,
                 description: str,
                 input_model: Type[BaseModel],
                 output_model: Type[BaseModel],
                 computation_func: Callable[[BaseModel], BaseModel]):
        """
        Initialize the simulator.
        
        Args:
            name: Name of the simulator
            description: Description of what the simulator does
            input_model: Pydantic model class for input validation
            output_model: Pydantic model class for output validation
            computation_func: Function that performs the computation
        """
        self.name = name
        self.description = description
        self.input_model = input_model
        self.output_model = output_model
        self.computation_func = computation_func
        
        # Validate the computation function signature
        self._validate_computation_function()
    
    def _validate_computation_function(self):
        """Validate that the computation function has the correct signature."""
        sig = inspect.signature(self.computation_func)
        params = list(sig.parameters.values())
        
        if len(params) != 1:
            raise ValueError(
                f"Computation function must take exactly one parameter, got {len(params)}"
            )
        
        # Check if the function is annotated correctly
        param = params[0]
        if param.annotation != inspect.Parameter.empty:
            if not issubclass(param.annotation, BaseModel):
                raise ValueError(
                    f"Computation function parameter should be annotated with a BaseModel subclass"
                )
    
    def run(self, input_data: Dict[str, Any]) -> SimulationResult:
        """
        Run the simulation with given input data.
        
        Args:
            input_data: Dictionary containing input parameters
            
        Returns:
            SimulationResult containing the output or error information
        """
        import time
        start_time = time.time()
        
        try:
            # Validate and create input model instance
            validated_input = self.input_model(**input_data)
            
            # Execute computation
            result = self.computation_func(validated_input)
            
            # Validate output
            if not isinstance(result, self.output_model):
                if isinstance(result, BaseModel):
                    # Try to convert if it's a BaseModel but wrong type
                    validated_output = self.output_model(**result.model_dump())
                else:
                    # If result is not a BaseModel, assume it's a dict
                    validated_output = self.output_model(**result)
            else:
                validated_output = result
            
            execution_time = time.time() - start_time
            
            return SimulationResult(
                success=True,
                output=validated_output,
                execution_time=execution_time
            )
            
        except ValidationError as e:
            execution_time = time.time() - start_time
            error_msg = f"Validation error: {str(e)}"
            return SimulationResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Computation error: {str(e)}\n{traceback.format_exc()}"
            return SimulationResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def get_input_schema(self) -> Dict[str, Any]:
        """Get JSON schema for input model."""
        return self.input_model.model_json_schema()
    
    def get_output_schema(self) -> Dict[str, Any]:
        """Get JSON schema for output model."""
        return self.output_model.model_json_schema()
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the simulator."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.get_input_schema(),
            "output_schema": self.get_output_schema()
        }
    
    def create_example_input(self) -> Dict[str, Any]:
        """
        Create an example input based on the input model schema.
        
        Returns:
            Dictionary with example values for all required fields
        """
        schema = self.get_input_schema()
        example = {}
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for field_name, field_info in properties.items():
            field_type = field_info.get("type", "string")
            
            if field_type == "string":
                example[field_name] = f"example_{field_name}"
            elif field_type == "integer":
                example[field_name] = 42
            elif field_type == "number":
                example[field_name] = 3.14
            elif field_type == "boolean":
                example[field_name] = True
            elif field_type == "array":
                example[field_name] = []
            elif field_type == "object":
                example[field_name] = {}
            else:
                example[field_name] = None
        
        return example


class SimulatorRegistry:
    """Registry for managing multiple simulators."""
    
    def __init__(self):
        self._simulators: Dict[str, Simulator] = {}
    
    def register(self, simulator: Simulator):
        """Register a simulator."""
        self._simulators[simulator.name] = simulator
    
    def get(self, name: str) -> Optional[Simulator]:
        """Get a simulator by name."""
        return self._simulators.get(name)
    
    def list_simulators(self) -> Dict[str, Dict[str, Any]]:
        """List all registered simulators with their info."""
        return {name: sim.get_info() for name, sim in self._simulators.items()}
    
    def remove(self, name: str) -> bool:
        """Remove a simulator from registry."""
        if name in self._simulators:
            del self._simulators[name]
            return True
        return False