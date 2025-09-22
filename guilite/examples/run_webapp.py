from guilite.reportgenerator.simulatorapp import SimulatorApp
from guilite.examples.add_and_multiply_simulators import MySimulator1, MySimulator2

if __name__ == "__main__":
    simulators = {
        "add": MySimulator1,
        "mult": MySimulator2,
    }
    app = SimulatorApp(simulators=simulators)
    app.run(debug=True)
