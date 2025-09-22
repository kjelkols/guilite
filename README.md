
# guilite

Et lettvekts Python-bibliotek for simulering, rapportgenerering og webbasert input/output.

## Installasjon

Installer avhengigheter og biblioteket lokalt:

```bash
pip install .
```

## Grunnleggende bruk

Definer dine egne simulator-klasser ved å arve fra `SimulatorBase` og implementere `run` og `generate_report`.

Eksempel (se også `examples/mysimulator.py`):

```python
from typing import Type
from pydantic import BaseModel, Field
from reportgenerator.simulatorbase import SimulatorBase
from reportgenerator.engine import Engine

class MyInput(BaseModel):
	x: float = Field(1.0, title="X-verdi")
	y: float = Field(2.0, title="Y-verdi")

class MyResult(BaseModel):
	sum: float = Field(..., title="Sum")

class MySimulator(SimulatorBase):
	input_model = MyInput
	result_model = MyResult
	name = "Addisjon"

	@staticmethod
	def run(input_data: BaseModel) -> BaseModel:
		data = input_data if isinstance(input_data, MyInput) else MyInput(**input_data.model_dump())
		return MyResult(sum=data.x + data.y)

	@staticmethod
	def generate_report(input_data: BaseModel, result_data: BaseModel) -> str:
		eng = Engine()
		eng.write_header("Addisjon", level=2)
		eng.write_model(input_data)
		eng.write_model(result_data)
		return eng.get_html()
```

## Starte web-app med egne simulatorer

Se `examples/run_simulator_app.py`:

```python
from reportgenerator.simulatorapp import SimulatorApp
from examples.mysimulator import MySimulator1, MySimulator2

if __name__ == "__main__":
	simulators = {
		"add": MySimulator1,
		"mult": MySimulator2,
	}
	app = SimulatorApp(simulators=simulators)
	app.run(debug=True)
```

Kjør fra prosjektroten:
```bash
python -m examples.run_simulator_app
```

## Funksjoner
- Automatisk webgrensesnitt for input og rapport
- Støtte for flere simulatorer
- Input/rapport kan lastes opp/ned som JSON
- Brukeren trenger ikke forholde seg til Flask eller templates

## Demo og eksempler
Se `examples/`-mappen for komplette demoer.

## Lisens
MIT License. Se LICENSE.
