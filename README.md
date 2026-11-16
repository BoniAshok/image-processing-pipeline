# Python Image Processing Pipeline

A **versatile command-line tool** for batch processing and transforming image datasets.  
This script allows you to apply various transformations (like grayscale, resize, and flipping) to an entire folder of images — perfect for **machine learning dataset preparation** or general image manipulation tasks.

---

## Features

- **Batch Processing** – Apply transformations to hundreds of images at once.  
- **Grayscale Conversion** – Convert images from color to grayscale.  
- **Image Resizing** – Resize all images to a specified width and height.  
- **Flipping** – Flip images either horizontally or vertically.  
- **Multiple Format Support** – Works with `.png`, `.jpg`, `.jpeg`.

---

## Requirements

- **Python 3.6+**
- **Pillow** (Python Imaging Library)

Install Pillow using pip:

```bash
pip install Pillow
 ```


## Installation
```bash
git clone https://github.com/bonilokesh/image-processing-pipeline.git
cd image-processing-pipeline
```

## Usage
```bash
python image-pipeline.py -i <input_folder> -o <output_folder> [options]
```

## Command-Line Arguments

| Argument | Short Form | Description |
|-----------|-------------|-------------|
| `--input_dir <path>` | `-i <path>` | **(Required)** Path to the folder of source images. |
| `--output_dir <path>` | `-o <path>` | **(Required)** Path to the folder to save processed images. |
| `--grayscale` |  | Converts images to grayscale. |
| `--resize <W> <H>` |  | Resizes images to a specific width and height. |
| `--flip_horizontal` |  | Flips images horizontally. |
| `--flip_vertical` |  | Flips images vertically. |
