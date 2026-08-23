import timeit
import unittest
from src.fluid_simulation import run_simulation
from src.render_frames import generate_frames
from src.video_processing import create_video

class TestPerformance(unittest.TestCase):
    def test_simulation_speed(self):
        """Ensure fluid simulation completes within acceptable time"""
        exec_time = timeit.timeit("run_simulation()", globals=globals(), number=1)
        assert exec_time < 10, "Fluid simulation took too long!"

    def test_frame_generation_speed(self):
        """Ensure animation frames are generated efficiently"""
        exec_time = timeit.timeit("generate_frames()", globals=globals(), number=5)
        assert exec_time < 1.0, "Frame rendering is too slow!"

    def test_video_assembly_speed(self):
        """Ensure video assembly completes efficiently"""
        exec_time = timeit.timeit("create_video()", globals=globals(), number=2)
        assert exec_time < 2.0, "Video assembly is inefficient!"

if __name__ == "__main__":
    unittest.main()
