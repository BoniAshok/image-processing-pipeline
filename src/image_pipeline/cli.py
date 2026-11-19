import argparse
import sys
from pathlib import Path
from image_pipeline import __version__
from image_pipeline.core import TransformConfig
from image_pipeline.parallel import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="image-pipeline",
        description="Fast, parallel batch image processing and transformation CLI.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "-i",
        "--input_dir",
        type=Path,
        required=True,
        help="Path to source directory containing images.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=Path,
        required=True,
        help="Path to destination directory for processed images.",
    )

    # Core transformations
    transforms = parser.add_argument_group("Transformations")
    transforms.add_argument(
        "--grayscale",
        action="store_true",
        help="Convert images to grayscale.",
    )
    transforms.add_argument(
        "--resize",
        type=int,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        help="Resize images to target width and height.",
    )
    transforms.add_argument(
        "--preserve-aspect-ratio",
        action="store_true",
        help="Keep original aspect ratio when resizing (fits within width x height bounds).",
    )
    transforms.add_argument(
        "--flip-horizontal",
        action="store_true",
        help="Flip images horizontally.",
    )
    transforms.add_argument(
        "--flip-vertical",
        action="store_true",
        help="Flip images vertically.",
    )
    transforms.add_argument(
        "--rotate",
        type=float,
        default=None,
        metavar="DEGREES",
        help="Rotate images clockwise by specified degrees (e.g. 90, 180, 270).",
    )
    transforms.add_argument(
        "--brightness",
        type=float,
        default=None,
        metavar="FACTOR",
        help="Adjust brightness factor (e.g. 1.0 = original, 1.5 = +50%%, 0.8 = -20%%).",
    )
    transforms.add_argument(
        "--contrast",
        type=float,
        default=None,
        metavar="FACTOR",
        help="Adjust contrast factor (e.g. 1.0 = original, 1.2 = higher contrast).",
    )
    transforms.add_argument(
        "--blur",
        type=float,
        default=None,
        metavar="RADIUS",
        help="Apply Gaussian blur with given radius.",
    )

    # Output options
    output_opts = parser.add_argument_group("Output Options")
    output_opts.add_argument(
        "--format",
        type=str,
        default=None,
        choices=["jpg", "jpeg", "png", "webp", "bmp", "tiff"],
        help="Convert all images to target format.",
    )
    output_opts.add_argument(
        "--quality",
        type=int,
        default=90,
        metavar="1-100",
        help="Compression quality for JPG/WebP output (default: 90).",
    )
    output_opts.add_argument(
        "--no-auto-orient",
        action="store_true",
        help="Disable automatic EXIF orientation correction.",
    )

    # Execution controls
    execution = parser.add_argument_group("Execution Controls")
    execution.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively discover images in subdirectories.",
    )
    execution.add_argument(
        "-w",
        "--workers",
        type=int,
        default=0,
        help="Number of parallel worker processes (0 = auto-detect CPU count).",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.input_dir.exists():
        print(f"Error: Input directory does not exist: '{args.input_dir}'", file=sys.stderr)
        sys.exit(1)

    config = TransformConfig(
        grayscale=args.grayscale,
        resize_dims=tuple(args.resize) if args.resize else None,
        preserve_aspect_ratio=args.preserve_aspect_ratio,
        flip_horizontal=args.flip_horizontal,
        flip_vertical=args.flip_vertical,
        rotate=args.rotate,
        brightness=args.brightness,
        contrast=args.contrast,
        blur=args.blur,
        output_format=args.format,
        auto_orient=not args.no_auto_orient,
        quality=args.quality,
    )

    success, fail = run_pipeline(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        config=config,
        recursive=args.recursive,
        workers=args.workers,
    )

    if fail > 0 and success == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
