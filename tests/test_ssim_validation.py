import cv2
import numpy as np
import unittest
from skimage.metrics import structural_similarity as ssim

class TestVisualAccuracy(unittest.TestCase):
    def setUp(self):
        """Load video file and reference image"""
        self.video = cv2.VideoCapture("data/testing-input-output/simulation_final_video_no_blender.mp4")
        self.reference_frame = cv2.imread("data/reference_images/expected_frame.jpg")

    def test_ssim_consistency(self):
        """Measure visual similarity using SSIM"""
        success, frame = self.video.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        reference_gray = cv2.cvtColor(self.reference_frame, cv2.COLOR_BGR2GRAY)

        similarity = ssim(gray_frame, reference_gray)
        assert similarity > 0.9, "Structural deviation detected!"

if __name__ == "__main__":
    unittest.main()
