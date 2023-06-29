import os
import argparse
from PIL import Image

def nearest_neighbor_upscale(original_path, downscaled_path, restored_path):
    original_files = sorted(os.listdir(original_path))
    downscaled_files = sorted(os.listdir(downscaled_path))
    assert len(original_files) >= len(downscaled_files)

    original_len = len(original_files)
    downscaled_len = len(downscaled_files)
    original_index = 0
    downscaled_index = 0
    while downscaled_index < downscaled_len:
        original_file_name = original_files[original_index]
        downscaled_file_name = downscaled_files[downscaled_index]

        original_base_name, original_extension = os.path.splitext(original_file_name)
        downscaled_base_name, downscaled_extension = os.path.splitext(downscaled_file_name)

        match = original_base_name.startswith(downscaled_base_name) or downscaled_base_name.startswith(original_base_name)
        if not match:
            original_index += 1
            if original_index >= original_len:
                raise ValueError(f"Could not find match for downscaled file: {downscaled_file_name}")
            continue

        original_file_path = os.path.join(original_path, original_file_name)
        downscaled_file_path = os.path.join(downscaled_path, downscaled_file_name)
        restored_file_path = os.path.join(restored_path, downscaled_file_name)

        original_image = Image.open(original_file_path)
        downscaled_image = Image.open(downscaled_file_path)
        upscaled_image = downscaled_image.resize(original_image.size, resample=Image.NEAREST)

        upscaled_image.save(restored_file_path)
        print(f"Restored image saved: {restored_file_path}")

        downscaled_index += 1

def main():
    parser = argparse.ArgumentParser(description="Image restoration using nearest neighbor upscaling")
    parser.add_argument("--original", required=True, help="Path to the original image folder")
    parser.add_argument("--downscaled", required=True, help="Path to the downscaled image folder")
    parser.add_argument("--restored", required=True, help="Path to the restored image folder")
    args = parser.parse_args()

    if not os.path.isdir(args.original):
        raise ValueError("Invalid original folder path.")
    if not os.path.isdir(args.downscaled):
        raise ValueError("Invalid downscaled folder path.")

    if not os.path.exists(args.restored):
        os.makedirs(args.restored)
    elif not os.path.isdir(args.restored):
        raise ValueError("Invalid restored folder path.")

    nearest_neighbor_upscale(args.original, args.downscaled, args.restored)

if __name__ == "__main__":
    main()
