"""
Merge several channels saved as individual files into a single multichannel image
"""
import argparse
import numpy as np
from skimage import io
import re

def merge_channels(well_id, channel_files):
    """
    Merge N grayscale images into a single N-channel image.
    
    Args:
        well_id: identifier of the well (e.g., "A01")
        channel_files: list of grayscale image files
    """
    # Sort files by channel identifier (w1, w2, w3, etc.)
    def get_channel_number(filepath):
        match = re.search(r'w(\d+)', filepath)
        return int(match.group(1)) if match else 0
    
    sorted_files = sorted(channel_files, key=get_channel_number)

    # Read all channel images
    channels = []
    for file_path in sorted_files:
        img = io.imread(file_path)
        print(f"Reading {file_path} ({img.shape}, {img.dtype})")
        channels.append(img)

    # Stack channels into an H x W x N image
    multichannel = np.stack(channels, axis=0)
    print(f"Stacked shape: {multichannel.shape}")
    
    # Save the resulting multichannel image as .tif
    output_path = f"{well_id}_multichannel_image.tif"
    io.imsave(output_path, multichannel)
    print(f"Merged channels for {well_id} into {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--well_id', required=True)
    parser.add_argument('--channels', nargs='+', required=True)
    
    args = parser.parse_args()
    merge_channels(args.well_id, args.channels)

if __name__ == '__main__':
    main()