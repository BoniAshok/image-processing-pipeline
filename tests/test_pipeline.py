import unittest
from pathlib import Path
import tempfile
from PIL import Image

from image_pipeline.core import (
    TransformConfig,
    apply_transformations,
    process_single_image,
    ImagePipeline,
)
from image_pipeline.parallel import run_pipeline


class TestImagePipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_dir = Path(self.temp_dir.name) / "input"
        self.output_dir = Path(self.temp_dir.name) / "output"
        self.input_dir.mkdir()
        self.output_dir.mkdir()

        # Create sample test images
        self.img1_path = self.input_dir / "sample1.png"
        img1 = Image.new("RGBA", (200, 100), color=(255, 0, 0, 255))
        img1.save(self.img1_path)

        self.img2_path = self.input_dir / "sample2.jpg"
        img2 = Image.new("RGB", (100, 100), color=(0, 255, 0))
        img2.save(self.img2_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_apply_transformations_grayscale(self):
        img = Image.new("RGB", (50, 50), color=(100, 150, 200))
        cfg = TransformConfig(grayscale=True)
        res = apply_transformations(img, cfg)
        self.assertEqual(res.mode, "L")

    def test_apply_transformations_resize(self):
        img = Image.new("RGB", (200, 100), color=(10, 20, 30))
        cfg = TransformConfig(resize_dims=(80, 40))
        res = apply_transformations(img, cfg)
        self.assertEqual(res.size, (80, 40))

    def test_apply_transformations_flip(self):
        img = Image.new("RGB", (20, 20), color=(50, 50, 50))
        cfg = TransformConfig(flip_horizontal=True, flip_vertical=True)
        res = apply_transformations(img, cfg)
        self.assertEqual(res.size, (20, 20))

    def test_process_single_image_with_format_conversion(self):
        out_file = self.output_dir / "converted.jpg"
        cfg = TransformConfig(grayscale=True)
        success, msg = process_single_image(self.img1_path, out_file, cfg)
        self.assertTrue(success)
        self.assertTrue(out_file.exists())
        with Image.open(out_file) as im:
            self.assertEqual(im.format, "JPEG")

    def test_batch_run_pipeline(self):
        cfg = TransformConfig(resize_dims=(50, 50), output_format="png")
        success, failed = run_pipeline(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            config=cfg,
            workers=2,
        )
        self.assertEqual(success, 2)
        self.assertEqual(failed, 0)
        output_files = list(self.output_dir.glob("*.png"))
        self.assertEqual(len(output_files), 2)


if __name__ == "__main__":
    unittest.main()
