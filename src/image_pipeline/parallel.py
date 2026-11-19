import concurrent.futures
import os
from pathlib import Path
from typing import List, Tuple
from image_pipeline.core import ImagePipeline, TransformConfig, process_single_image

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def _worker_task(args: Tuple[Path, Path, TransformConfig]) -> Tuple[bool, str]:
    input_file, output_file, config = args
    return process_single_image(input_file, output_file, config)


def run_pipeline(
    input_dir: Path,
    output_dir: Path,
    config: TransformConfig,
    recursive: bool = False,
    workers: int = 0,
) -> Tuple[int, int]:
    """Runs the batch processing pipeline over input_dir and saves to output_dir.

    Returns (success_count, fail_count).
    """
    pipeline = ImagePipeline(config)
    image_files = pipeline.discover_files(input_dir, recursive=recursive)

    if not image_files:
        print(f"No supported images found in '{input_dir}'.")
        return 0, 0

    print(f"Discovered {len(image_files)} image(s) to process.")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine worker count
    if workers <= 0:
        workers = min(os.cpu_count() or 4, len(image_files))

    tasks = [
        (img_path, pipeline.target_path(img_path, input_dir, output_dir), config)
        for img_path in image_files
    ]

    success_count = 0
    fail_count = 0

    # Sequential execution if only 1 image or single worker specified
    if workers <= 1 or len(tasks) == 1:
        iterator = tqdm(tasks, desc="Processing images", unit="img") if HAS_TQDM else tasks
        for idx, item in enumerate(iterator):
            success, msg = _worker_task(item)
            if not HAS_TQDM:
                print(f"[{idx+1}/{len(tasks)}] {msg}")
            if success:
                success_count += 1
            else:
                fail_count += 1
                if HAS_TQDM:
                    tqdm.write(msg)
    else:
        print(f"Running across {workers} parallel workers...")
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(_worker_task, task) for task in tasks]

            iterator = (
                tqdm(concurrent.futures.as_completed(futures), total=len(tasks), desc="Processing images", unit="img")
                if HAS_TQDM
                else concurrent.futures.as_completed(futures)
            )

            for idx, future in enumerate(iterator):
                try:
                    success, msg = future.result()
                    if not HAS_TQDM:
                        print(f"[{idx+1}/{len(tasks)}] {msg}")
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                        if HAS_TQDM:
                            tqdm.write(msg)
                except Exception as exc:
                    fail_count += 1
                    err_msg = f"Worker exception: {exc}"
                    if HAS_TQDM:
                        tqdm.write(err_msg)
                    else:
                        print(err_msg)

    print("\nBatch Processing Completed:")
    print(f"  ✓ Succeeded: {success_count}")
    if fail_count > 0:
        print(f"  ✗ Failed:    {fail_count}")
    print(f"  📂 Destination: {output_dir.resolve()}\n")

    return success_count, fail_count
