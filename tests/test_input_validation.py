import json
import unittest
from jsonschema import validate

class TestFluidSimulationInput(unittest.TestCase):
    def setUp(self):
        """Load input JSON"""
        with open("data/testing-input-output/fluid_simulation.json") as f:
            self.input_data = json.load(f)

    def test_json_schema(self):
        """Ensure input file follows correct JSON format"""
        schema = {
            "type": "object",
            "properties": {
                "simulation_info": {"type": "object"},
                "fluid_parameters": {"type": "object"},
                "velocity_fields": {"type": "array"}
            },
            "required": ["simulation_info", "fluid_parameters", "velocity_fields"]
        }
        validate(instance=self.input_data, schema=schema)

    def test_velocity_constraints(self):
        """Ensure velocity field values are physically valid"""
        for v in self.input_data["velocity_fields"]:
            assert -10 <= v["vx"] <= 10, "Velocity x out of bounds!"
            assert -10 <= v["vy"] <= 10, "Velocity y out of bounds!"
            assert -10 <= v["vz"] <= 10, "Velocity z out of bounds!"

if __name__ == "__main__":
    unittest.main()
