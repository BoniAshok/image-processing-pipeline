from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}


@dataclass
class TransformConfig:
    grayscale: bool = False
    resize_dims: Optional[Tuple[int, int]] = None
    preserve_aspect_ratio: bool = False
    flip_horizontal: bool = False
    flip_vertical: bool = False
    rotate: Optional[float] = None
    brightness: Optional[float] = None
    contrast: Optional[float] = None
    blur: Optional[float] = None
    output_format: Optional[str] = None
    auto_orient: bool = True
    quality: int = 90


def apply_transformations(img: Image.Image, config: TransformConfig) -> Image.Image:
    """Applies the configured transformations sequentially on an in-memory image."""
    result = img.copy()

    # 1. EXIF auto-orientation
    if config.auto_orient:
        try:
            result = ImageOps.exif_transpose(result) or result
        except Exception:
            pass

    # 2. Grayscale
    if config.grayscale:
        result = ImageOps.grayscale(result)

    # 3. Resizing
    if config.resize_dims:
        w, h = config.resize_dims
        if config.preserve_aspect_ratio:
            result.thumbnail((w, h), Image.Resampling.LANCZOS)
        else:
            result = result.resize((w, h), Image.Resampling.LANCZOS)

    # 4. Flips & Rotation
    if config.flip_horizontal:
        result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if config.flip_vertical:
        result = result.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if config.rotate is not None and config.rotate != 0:
        result = result.rotate(config.rotate, expand=True)

    # 5. Image Enhancements (Brightness, Contrast, Blur)
    if config.brightness is not None:
        enhancer = ImageEnhance.Brightness(result)
        result = enhancer.enhance(config.brightness)

    if config.contrast is not None:
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(config.contrast)

    if config.blur is not None and config.blur > 0:
        result = result.filter(ImageFilter.GaussianBlur(radius=config.blur))

    return result


def process_single_image(
    input_path: Path, output_path: Path, config: TransformConfig
) -> Tuple[bool, str]:
    """Processes a single image file and writes it to output_path.
    Returns (success, message).
    """
    try:
        with Image.open(input_path) as img:
            processed = apply_transformations(img, config)

            target_ext = output_path.suffix.lower()
            if target_ext in [".jpg", ".jpeg"] and processed.mode in ("RGBA", "P", "LA"):
                # Handle alpha channel when saving as JPEG
                rgb_img = Image.new("RGB", processed.size, (255, 255, 255))
                if processed.mode == "RGBA":
                    rgb_img.paste(processed, mask=processed.split()[3])
                else:
                    rgb_img.paste(processed.convert("RGB"))
                processed = rgb_img

            output_path.parent.mkdir(parents=True, exist_ok=True)
            save_kwargs = {}
            if target_ext in [".jpg", ".jpeg", ".webp"]:
                save_kwargs["quality"] = config.quality

            processed.save(output_path, **save_kwargs)
            return True, f"OK: {input_path.name} -> {output_path.name}"
    except Exception as e:
        return False, f"Failed {input_path.name}: {str(e)}"


class ImagePipeline:
    """High-level batch pipeline orchestrator."""

    def __init__(self, config: TransformConfig):
        self.config = config

    def discover_files(self, input_dir: Path, recursive: bool = False):
        pattern = "**/*" if recursive else "*"
        return sorted(
            [
                p
                for p in input_dir.glob(pattern)
                if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
        )

    def target_path(
        self, input_path: Path, input_dir: Path, output_dir: Path
    ) -> Path:
        rel_path = input_path.relative_to(input_dir)
        ext = (
            f".{self.config.output_format.lstrip('.').lower()}"
            if self.config.output_format
            else input_path.suffix.lower()
        )
        return output_dir / rel_path.with_suffix(ext)
