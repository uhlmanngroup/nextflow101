"""
Combine individual binary masks for the same well into a single instance segmentation mask
"""
import argparse
import numpy as np
from skimage import io

def combine_masks(well_id, binary_mask_files):
    """
    Combine binary masks from the same well into a single instance segmentation mask
    
    Args:
        well_id: identifier of the well (e.g., "A01")
        binary_mask_files: list of binary mask files
    """
    # Read first mask to get dimensions
    first_mask = io.imread(binary_mask_files[0])
    h, w = first_mask.shape
    
    # Initialize instance mask
    instance_mask = np.zeros((h, w), dtype=np.uint16)
    
    # Combine binary masks into a single instance segmentation mask with a different integer label for each instance
    for idx, binary_mask_file in enumerate(binary_mask_files, 1):
        binary_mask = io.imread(binary_mask_file) > 0
        instance_mask[binary_mask] = idx
    
    # Save the combined instance segmentation mask as .tif
    output_path = f"{well_id}_instances_mask.tif"
    io.imsave(output_path, instance_mask)
    print(f"Combined {len(binary_mask_files)} masks for {well_id}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--well_id', required=True)
    parser.add_argument('--binary_masks', nargs='+', required=True)
    
    args = parser.parse_args()
    combine_masks(args.well_id, args.binary_masks)

if __name__ == '__main__':
    main()