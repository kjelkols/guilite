
from typing import Type
from pydantic import BaseModel, Field
try:
	from guilite.reportgenerator.simulatorbase import SimulatorBase
	from guilite.reportgenerator.engine import Engine
except ModuleNotFoundError as e:
	print("\n[FEIL] Kunne ikke importere 'reportgenerator'.\nKjør dette skriptet fra prosjektroten, f.eks. med:\n    python -m examples.mysimulator\neller\n    python -m examples.run_simulator_app\n")
	raise e

class MyInput1(BaseModel):
	x: float = Field(1.0, title="X-verdi")
	y: float = Field(2.0, title="Y-verdi")

class MyResult1(BaseModel):
	sum: float = Field(..., title="Sum")

class MySimulator1(SimulatorBase):
	input_model = MyInput1
	result_model = MyResult1
	name = "Addisjon"

	@staticmethod
	def run(input_data: BaseModel) -> BaseModel:
		data = input_data if isinstance(input_data, MyInput1) else MyInput1(**input_data.model_dump())
	# Filen er nå flyttet og omdøpt til add_and_multiply_simulators.py

	@staticmethod
	def generate_report(input_data: BaseModel, result_data: BaseModel) -> str:
		eng = Engine()
		eng.write_header("Addisjon", level=2)
		eng.write_model(input_data)
		eng.write_model(result_data)
		return eng.get_html()

class MyInput2(BaseModel):
	a: float = Field(3.0, title="Første verdi")
	b: float = Field(4.0, title="Andre verdi")

class MyResult2(BaseModel):
	produkt: float = Field(..., title="Produkt")

class MySimulator2(SimulatorBase):
	input_model = MyInput2
	result_model = MyResult2
	name = "Multiplikasjon"

	@staticmethod
	def run(input_data: BaseModel) -> BaseModel:
		data = input_data if isinstance(input_data, MyInput2) else MyInput2(**input_data.model_dump())
		return MyResult2(produkt=data.a * data.b)

	@staticmethod
	def generate_report(input_data: BaseModel, result_data: BaseModel) -> str:
		data = input_data if isinstance(input_data, MyInput2) else MyInput2(**input_data.model_dump())
		result = result_data if isinstance(result_data, MyResult2) else MyResult2(**result_data.model_dump())
		html = ["<h2>Resultat for Multiplikasjon. Denne teksten er skrevet manuelt som direkte html.</h2>"]
		html.append(f"<p>Første verdi: <b>{data.a}</b></p>")
		html.append(f"<p>Andre verdi: <b>{data.b}</b></p>")
		html.append(f"<p>Produkt: <span class='result-block'><b>{result.produkt}</b></span></p>")
		return '\n'.join(html)
