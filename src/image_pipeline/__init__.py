"""
Image Processing Pipeline - A fast, modular CLI tool and library for batch image transformations.
"""

__version__ = "1.0.0"

from image_pipeline.core import (
    ImagePipeline,
    TransformConfig,
    process_single_image,
)

__all__ = ["ImagePipeline", "TransformConfig", "process_single_image", "__version__"]
