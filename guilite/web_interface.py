"""
Web Interface - Minimal Flask application for GUI access to simulators
"""

from flask import Flask, request, render_template_string, jsonify, redirect, url_for
from typing import Optional, Dict, Any
import json

from .simulator import Simulator, SimulatorRegistry, SimulationResult
from .report_generator import ReportGenerator


class WebInterface:
    """Minimal Flask web interface for GUI access to simulators."""
    
    def __init__(self, app: Optional[Flask] = None):
        """
        Initialize the web interface.
        
        Args:
            app: Optional Flask app instance. If None, creates a new one.
        """
        self.app = app or Flask(__name__)
        self.registry = SimulatorRegistry()
        self.report_generator = ReportGenerator()
        
        # Configure routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page showing available simulators."""
            simulators = self.registry.list_simulators()
            return render_template_string(self._get_index_template(), 
                                        simulators=simulators)
        
        @self.app.route('/simulator/<simulator_name>')
        def simulator_page(simulator_name: str):
            """Page for a specific simulator."""
            simulator = self.registry.get(simulator_name)
            if not simulator:
                return f"Simulator '{simulator_name}' not found", 404
            
            example_input = simulator.create_example_input()
            return render_template_string(
                self._get_simulator_template(),
                simulator=simulator,
                example_input=json.dumps(example_input, indent=2)
            )
        
        @self.app.route('/run/<simulator_name>', methods=['POST'])
        def run_simulation(simulator_name: str):
            """Run a simulation and return results."""
            simulator = self.registry.get(simulator_name)
            if not simulator:
                return jsonify({"error": f"Simulator '{simulator_name}' not found"}), 404
            
            try:
                input_data = request.get_json()
                if not input_data:
                    return jsonify({"error": "No input data provided"}), 400
                
                result = simulator.run(input_data)
                
                if result.success:
                    # Generate HTML report
                    html_report = self.report_generator.generate_html(
                        result.output,
                        title=f"{simulator.name} - Results"
                    )
                    
                    return jsonify({
                        "success": True,
                        "output": result.output.model_dump(),
                        "html_report": html_report,
                        "execution_time": result.execution_time
                    })
                else:
                    return jsonify({
                        "success": False,
                        "error": result.error,
                        "execution_time": result.execution_time
                    })
                    
            except Exception as e:
                return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
        
        @self.app.route('/api/simulators')
        def api_simulators():
            """API endpoint to list all simulators."""
            return jsonify(self.registry.list_simulators())
        
        @self.app.route('/api/simulator/<simulator_name>/schema')
        def api_simulator_schema(simulator_name: str):
            """API endpoint to get simulator schemas."""
            simulator = self.registry.get(simulator_name)
            if not simulator:
                return jsonify({"error": f"Simulator '{simulator_name}' not found"}), 404
            
            return jsonify({
                "input_schema": simulator.get_input_schema(),
                "output_schema": simulator.get_output_schema()
            })
    
    def register_simulator(self, simulator: Simulator):
        """Register a simulator with the web interface."""
        self.registry.register(simulator)
    
    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = True):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug)
    
    def _get_index_template(self) -> str:
        """Return the HTML template for the index page."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guilite - Simulator Interface</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .simulator-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .simulator-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: #f8f9fa;
            transition: box-shadow 0.3s ease;
        }
        .simulator-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .simulator-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .simulator-description {
            color: #555;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        .btn {
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #2980b9;
        }
        .no-simulators {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Guilite - Simulator Interface</h1>
        <p>Welcome to the Guilite interface. Select a simulator below to run computations with validated input/output.</p>
        
        {% if simulators %}
            <div class="simulator-grid">
                {% for name, info in simulators.items() %}
                <div class="simulator-card">
                    <div class="simulator-name">{{ name }}</div>
                    <div class="simulator-description">{{ info.description }}</div>
                    <a href="{{ url_for('simulator_page', simulator_name=name) }}" class="btn">
                        Run Simulator
                    </a>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="no-simulators">
                <h3>No simulators registered</h3>
                <p>Register simulators using the WebInterface.register_simulator() method.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>"""
    
    def _get_simulator_template(self) -> str:
        """Return the HTML template for simulator pages."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ simulator.name }} - Guilite</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .description {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
            font-style: italic;
        }
        .form-section {
            margin-bottom: 30px;
        }
        .form-section h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 14px;
            background: #f8f9fa;
        }
        .btn {
            background: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #2980b9;
        }
        .btn-secondary {
            background: #95a5a6;
        }
        .btn-secondary:hover {
            background: #7f8c8d;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            border-radius: 5px;
            display: none;
        }
        .results.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .results.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .report-container {
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }
        .back-link {
            color: #3498db;
            text-decoration: none;
            margin-bottom: 20px;
            display: inline-block;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="{{ url_for('index') }}" class="back-link">← Back to Simulators</a>
        
        <h1>{{ simulator.name }}</h1>
        
        <div class="description">
            {{ simulator.description }}
        </div>
        
        <div class="form-section">
            <h3>Input Parameters (JSON)</h3>
            <textarea id="inputData" placeholder="Enter JSON input data...">{{ example_input }}</textarea>
            <br><br>
            <button class="btn" onclick="runSimulation()">Run Simulation</button>
            <button class="btn btn-secondary" onclick="loadExample()">Load Example</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Running simulation...</p>
        </div>
        
        <div class="results" id="results">
            <h3>Results</h3>
            <div id="resultsContent"></div>
        </div>
    </div>
    
    <script>
        const exampleInput = {{ example_input|safe }};
        
        function loadExample() {
            document.getElementById('inputData').value = JSON.stringify(exampleInput, null, 2);
        }
        
        function runSimulation() {
            const inputData = document.getElementById('inputData').value;
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');
            
            // Show loading, hide results
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const data = JSON.parse(inputData);
                
                fetch('/run/{{ simulator.name }}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(result => {
                    loading.style.display = 'none';
                    results.style.display = 'block';
                    
                    if (result.success) {
                        results.className = 'results success';
                        resultsContent.innerHTML = `
                            <p><strong>Execution time:</strong> ${result.execution_time.toFixed(3)} seconds</p>
                            <div class="report-container">
                                ${result.html_report}
                            </div>
                        `;
                    } else {
                        results.className = 'results error';
                        resultsContent.innerHTML = `
                            <h4>Error occurred:</h4>
                            <pre>${result.error}</pre>
                            <p><strong>Execution time:</strong> ${result.execution_time.toFixed(3)} seconds</p>
                        `;
                    }
                })
                .catch(error => {
                    loading.style.display = 'none';
                    results.style.display = 'block';
                    results.className = 'results error';
                    resultsContent.innerHTML = `<h4>Network Error:</h4><pre>${error.message}</pre>`;
                });
                
            } catch (e) {
                loading.style.display = 'none';
                results.style.display = 'block';
                results.className = 'results error';
                resultsContent.innerHTML = `<h4>JSON Parse Error:</h4><pre>${e.message}</pre>`;
            }
        }
    </script>
</body>
</html>"""