import os
import unittest

class TestVideoGeneration(unittest.TestCase):
    def test_video_file_generated(self):
        """Ensure the final video file is created"""
        assert os.path.exists("data/testing-input-output/simulation_final_video_no_blender.mp4"), "Video file missing!"

if __name__ == "__main__":
    unittest.main()
