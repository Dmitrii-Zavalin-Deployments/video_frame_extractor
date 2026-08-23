import os
import unittest

class TestFluidSimulation(unittest.TestCase):
    def test_simulation_execution(self):
        """Ensure fluid simulation runs correctly"""
        exit_code = os.system("python run_fluid_simulation.py")
        assert exit_code == 0, "Fluid simulation failed!"

    def test_output_files_exist(self):
        """Ensure simulation produces valid output files"""
        assert os.path.exists("data/testing-input-output/fluid_dynamics_animation.json"), "Simulation data missing!"

if __name__ == "__main__":
    unittest.main()
