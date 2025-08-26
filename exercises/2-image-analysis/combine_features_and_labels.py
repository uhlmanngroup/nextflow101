"""
Combine features and labels files from multiple images
"""
import argparse
import os
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_features', required=True)
    parser.add_argument('--output_labels', required=True)
    
    args = parser.parse_args()
    
    # Find and combine feature files
    feature_dfs = []
    label_dfs = []
    
    # NextFlow conveniently passes all files to the working directory
    # We just need to identify which ones are features files vs labels files
    for file in sorted(os.listdir('.')):
        if file.endswith('_features.csv'):
            df = pd.read_csv(file)
            feature_dfs.append(df)
        elif file.endswith('_labels.csv'):
            df = pd.read_csv(file)
            label_dfs.append(df)
    
    # Combine features
    all_features = pd.concat(feature_dfs, ignore_index=True)
    all_features.to_csv(args.output_features, index=False)
    print(f'Combined features from {len(feature_dfs)} images ({len(all_features)} objects in total)')
    
    # Combine labels
    all_labels = pd.concat(label_dfs, ignore_index=True)
    all_labels.to_csv(args.output_labels, index=False)
    print(f'\nClass distribution:')
    print(all_labels.label.value_counts())
    
    # Sanity check
    if len(all_features) != len(all_labels):
        print(f'WARNING: number of objects with features ({len(all_features)}) != number of objects with labels ({len(all_labels)})')
    else:
        print(f'\nSuccessfully combined {len(all_features)} objects!')

if __name__ == '__main__':
    main()