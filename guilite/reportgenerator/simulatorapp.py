from flask import Flask, request, render_template
from typing import Dict, Type
from pydantic import BaseModel

import os

class SimulatorApp:
    def __init__(self, simulators: Dict[str, Type]):
        self.simulators = simulators
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "static"))
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        self.app.secret_key = 'dev'
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                selected_simulator_key = request.form.get('simulator', list(self.simulators.keys())[0])
                prev_sim = request.form.get('prev_sim', selected_simulator_key)
                sim_class = self.simulators[selected_simulator_key]
                input_model = sim_class.input_model
                if selected_simulator_key != prev_sim:
                    input_data = input_model()
                    result = None
                else:
                    data = {k: v for k, v in request.form.items() if k not in ('simulator', 'prev_sim')}
                    input_data = input_model(**data)
                    result = sim_class.run(input_data)
            else:
                selected_simulator_key = list(self.simulators.keys())[0]
                sim_class = self.simulators[selected_simulator_key]
                input_model = sim_class.input_model
                input_data = input_model()
                result = None

            input_html = sim_class.generate_inputform(input_data)
            report_html = sim_class.generate_report(input_data, result) if result is not None else ""
            input_json = input_data.model_dump()
            input_fields = list(input_json.keys())
            return render_template(
                "index.html",
                selected_simulator_key=selected_simulator_key,
                simulators=self.simulators,
                input_html=input_html,
                report_html=report_html,
                input_json=input_json,
                input_fields=input_fields
            )

    def run(self, **kwargs):
        self.app.run(**kwargs)
