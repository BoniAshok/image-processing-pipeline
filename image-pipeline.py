import os 
import argparse
from PIL import Image , ImageOps

def process(input_dir , output_dir , to_grayscale , resize_dims , flip_horizontal , flip_vertical):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"created output directory: {output_dir}")

    supported_files = ('.png' , '.jpg' , '.jpeg')

    try:
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_files)]
        if not image_files:
            print(f"no supported image files found in '{input_dir}'.")

            return
    except FileNotFoundError:
        print(f"error:input directory not found at '{input_dir}'")
        return
    print(f"found {len(image_files)} images to process. ")

    for index , filename in enumerate(image_files):
        try:
            input_path = os.path.join(input_dir , filename)
            output_path = os.path.join(output_dir , filename)

            with Image.open(input_path) as img:
                print(f"Processing ({index + 1}/{len(image_files)}): {filename}")
                processed_img = img.copy()

                if to_grayscale:
                    processed_img = ImageOps.grayscale(processed_img)

                if resize_dims:
                    processed_img = processed_img.resize(resize_dims)

                if flip_horizontal:
                    processed_img = processed_img.transpose(Image.FLIP_LEFT_RIGHT)

                if flip_vertical:
                    processed_img = processed_img.transpose(Image.FLIP_TOP_BOTTOM)

                if processed_img.mode == 'RGBA' and output_path.lower().endswith('.jpg'):
                    processed_img = processed_img.convert('RGB')

                processed_img.save(output_path)
        except Exception as e:
            print(f"cound not process {filename}. Reason {e}.")

    print("\nprocessing completed")
    print(f"all processed images have been saved to: {output_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A command-line tool to batch process images.")

    parser.add_argument("-i", "--input_dir", type=str, required=True,
                        help="Path to the input directory containing images.")
    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Path to the directory where processed images will be saved.")
    
    # Transformation arguments
    parser.add_argument("--grayscale", action="store_true",
                        help="Convert images to grayscale.")
    parser.add_argument("--resize", type=int, nargs=2, metavar=('WIDTH', 'HEIGHT'),
                        help="Resize images to a specific width and height (e.g., --resize 800 600).")
    parser.add_argument("--flip_horizontal", action="store_true",
                        help="Flip images horizontally.")
    parser.add_argument("--flip_vertical", action="store_true",
                        help="Flip images vertically.")

    args = parser.parse_args()

    # Call the main processing function with parsed arguments
    process(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        to_grayscale=args.grayscale,
        resize_dims=tuple(args.resize) if args.resize else None,
        flip_horizontal=args.flip_horizontal,
        flip_vertical=args.flip_vertical
    )