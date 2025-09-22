from pydantic import BaseModel, Field
from reportgenerator.engine import Engine

class DemoInput(BaseModel):
    mass_flow: float = Field(1.0, title="Massestrøm [kg/s]")
    temperature: float = Field(20.0, title="Temperatur [°C]")

class DemoResult(BaseModel):
    density: float = Field(1.2, title="Tetthet [kg/m³]")
    enthalpy: float = Field(42000, title="Entalpi [J/kg]")

def main():
    input_data = DemoInput(mass_flow=1.0, temperature=20.0)
    result_data = DemoResult(density=1.2, enthalpy=42000)

    engine = Engine()
    engine.write_header("Demo av Engine-rapport", 1)
    engine.write("<h2>Demo-rapport</h2>Dette er en demo-rapport generert av Engine-klassen.<br> ")
    engine.write_header("Input data", 2)
    engine.write_input(input_data)
    engine.write_header("Result data", 2)
    engine.write_model(result_data)
    engine.write_header("Resultater på tabell-form", 2)
    engine.write_model_table([result_data, result_data], headers=["Kolonne 1", "Kolonne 2"])
    html_output = engine.get_html()
    print(html_output)

if __name__ == "__main__":
    main()
