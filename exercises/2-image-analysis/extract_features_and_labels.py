"""
Extract features and labels from worms in BBBC010
"""
import argparse
import numpy as np
import pandas as pd
from skimage import io, measure
from skimage.feature import graycomatrix, graycoprops

def extract_features_and_labels(well_id, image_path, mask_path, threshold):
    """
    Extract features for each object in the image.
    
    Args:
        well_id: well identifier
        image_path: path to multichannel image (first channel is GFP, second channel is brightfield)
        mask_path: path to instance segmentation mask
        threshold: intensity threshold for live/dead classification
    """
    # Read image and mask
    img = io.imread(image_path)
    mask = io.imread(mask_path)
    
    print(f'Processing {well_id} ({img.shape}) and corresponding mask ({mask.shape})')
    
    # Extract channels
    gfp_channel = img[0, :, :]
    bf_channel = img[1, :, :]
    
    # Get region properties
    regions = measure.regionprops(mask, intensity_image=bf_channel)
    
    # Extract features and labels
    features_list = []
    labels_list = []
    
    for region in regions:
        object_id = region.label
        
        # Get mask for this object
        object_mask = mask == object_id
        
        # Calculate sum of intensities in GFP channel for live/dead classification
        background_intensity = np.median(gfp_channel)
        object_intensity = np.median(gfp_channel[object_mask])
        label = 'dead' if object_intensity > (1.0+threshold) * background_intensity else 'live'
        
        # Calculate texture features
        masked_values = bf_channel[object_mask]
        min_val, max_val = masked_values.min(), masked_values.max()
        if max_val > min_val:
            normalized = ((bf_channel - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        else:
            normalized = np.zeros_like(bf_channel, dtype=np.uint8)
        normalized[~object_mask] = 0

        glcm = graycomatrix(normalized, 
                            distances=[1], 
                            angles=[0, np.pi/4, np.pi/2, 3*np.pi/4],
                            levels=256,
                            symmetric=True,
                            normed=True)
                
        # Average texture features across angles
        contrast = graycoprops(glcm, 'contrast')[0].mean()
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0].mean()
        homogeneity = graycoprops(glcm, 'homogeneity')[0].mean()
        energy = graycoprops(glcm, 'energy')[0].mean()
        correlation = graycoprops(glcm, 'correlation')[0].mean()
        asm = graycoprops(glcm, 'ASM')[0].mean()

        # Store label 
        labels_list.append({
            'well_id': well_id,
            'object_id': object_id,
            'label': label,
            'gfp_intensity': object_intensity  # Keep this for quality control and debugging
        })
        
        # Store regionprops features  
        features = {
            'well_id': well_id,
            'object_id': object_id,
            # Shape features
            'area': region.area,
            'perimeter': region.perimeter,
            'eccentricity': region.eccentricity,
            'solidity': region.solidity,
            'extent': region.extent,
            'major_axis_length': region.major_axis_length,
            'minor_axis_length': region.minor_axis_length,
            # Intensity features from brightfield
            'mean_intensity': region.mean_intensity,
            'max_intensity': region.max_intensity,
            'min_intensity': region.min_intensity,
            'intensity_std': np.std(bf_channel[object_mask]),
            # Texture features
            'texture_contrast': contrast,
            'texture_dissimilarity': dissimilarity,
            'texture_homogeneity': homogeneity,
            'texture_energy': energy,
            'texture_correlation': correlation,
            'texture_asm': asm
        }
        features_list.append(features)
    
    # Save features and labels to separate files
    features_df = pd.DataFrame(features_list)
    labels_df = pd.DataFrame(labels_list)
    
    features_df.to_csv(f'{well_id}_features.csv', index=False)
    labels_df.to_csv(f'{well_id}_labels.csv', index=False)
    
    print(f'Saved features and labels for {len(features_df)} objects')
    print(f'Class distribution: {labels_df.label.value_counts().to_dict()}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--well_id', required=True)
    parser.add_argument('--image', required=True)
    parser.add_argument('--mask', required=True)
    parser.add_argument('--threshold', type=float, required=True)
    
    args = parser.parse_args()
    extract_features_and_labels(args.well_id, args.image, args.mask, args.threshold)

if __name__ == '__main__':
    main()