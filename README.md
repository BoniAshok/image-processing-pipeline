# Python Image Processing Pipeline

[![CI](https://github.com/BoniAshok/image-processing-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/BoniAshok/image-processing-pipeline/actions)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fast, modular, parallel CLI tool and Python library for batch processing and transforming image datasets.

Ideal for **machine learning dataset preparation**, computer vision preprocessing, and bulk image optimization tasks.

---

## Key Features

- ⚡ **Multi-Core Parallelism** – Process thousands of images quickly using multiprocessing workers.
- 🔄 **Extensive Transformations**:
  - Resizing (exact dimensions or aspect-ratio preserving)
  - Grayscale conversion
  - Horizontal and vertical flipping
  - Free angle rotation (`--rotate`)
  - Image adjustments: Brightness, Contrast, and Gaussian Blur
  - EXIF orientation auto-correction
- 📦 **Format Conversion** – Convert between PNG, JPEG, WebP, BMP, and TIFF with configurable quality settings.
- 🗂️ **Recursive Processing** – Traverse nested folder structures with `-r / --recursive`.
- 📊 **Progress Bar** – Live visual progress tracking using `tqdm`.
- 🐍 **Dual Usage** – Usable both as a standalone command-line executable (`image-pipeline`) and as a Python library (`import image_pipeline`).

---

## Installation

### From Source
```bash
git clone https://github.com/BoniAshok/image-processing-pipeline.git
cd image-processing-pipeline
pip install .
```

### For Development
```bash
pip install -e ".[dev]"
```

---

## Usage

### 1. Command-Line Interface (CLI)

```bash
# Basic grayscale & resize
image-pipeline -i ./dataset/raw -o ./dataset/processed --grayscale --resize 224 224

# Aspect ratio preserving resize with format conversion to WebP
image-pipeline -i ./images -o ./output --resize 800 600 --preserve-aspect-ratio --format webp --quality 85

# Parallel processing with custom worker count and adjustments
image-pipeline -i ./input -o ./output --workers 4 --contrast 1.2 --brightness 1.1 --rotate 90 -r
```

#### CLI Options

| Option | Short | Description |
|---|---|---|
| `--input_dir <path>` | `-i` | **(Required)** Path to input folder |
| `--output_dir <path>` | `-o` | **(Required)** Path to output folder |
| `--grayscale` | | Convert images to grayscale |
| `--resize <W> <H>` | | Resize to width and height |
| `--preserve-aspect-ratio`| | Preserve aspect ratio when resizing |
| `--flip-horizontal` | | Flip images horizontally |
| `--flip-vertical` | | Flip images vertically |
| `--rotate <deg>` | | Rotate clockwise by degrees |
| `--brightness <factor>` | | Adjust brightness (e.g. `1.2`) |
| `--contrast <factor>` | | Adjust contrast (e.g. `1.2`) |
| `--blur <radius>` | | Apply Gaussian blur with radius |
| `--format <ext>` | | Convert format (`jpg`, `png`, `webp`, etc.) |
| `--quality <1-100>` | | Quality for JPEG / WebP (default: 90) |
| `--recursive` | `-r` | Search subdirectories recursively |
| `--workers <int>` | `-w` | Number of worker processes (default: auto) |

---

### 2. Python Library Usage

```python
from pathlib import Path
from image_pipeline import TransformConfig
from image_pipeline.parallel import run_pipeline

config = TransformConfig(
    grayscale=True,
    resize_dims=(256, 256),
    preserve_aspect_ratio=True,
    output_format="webp",
    quality=85,
)

success, failed = run_pipeline(
    input_dir=Path("./raw_images"),
    output_dir=Path("./processed_images"),
    config=config,
    workers=4,
)
```

---

## Docker Usage

```bash
# Build the Docker image
docker build -t image-pipeline .

# Run batch processing via Docker volume mounts
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output image-pipeline -i /app/input -o /app/output --resize 512 512 --grayscale
```

---

## Running Tests

```bash
python3 -m unittest discover -s tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).
