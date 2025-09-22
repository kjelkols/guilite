from typing import Type
from pydantic import BaseModel, Field
from simulator import SimulatorProtocol

class DemoInput(BaseModel):
    x: float = Field(1.0, title="x-verdi")

class DemoResult(BaseModel):
    y: float = Field(2.0, title="y-verdi")

class DemoSimulator:
    input_model: Type[BaseModel] = DemoInput
    result_model: Type[BaseModel] = DemoResult

    def run(self, input_data: BaseModel) -> BaseModel:
        return DemoResult(y=input_data.x * 2)

def main():
    sim = DemoSimulator()
    inp = DemoInput(x=3)
    res = sim.run(inp)
    print(f"Input: {inp}")
    # Filen er nå flyttet og omdøpt til simulator_protocol_demo.py

if __name__ == "__main__":
    main()
