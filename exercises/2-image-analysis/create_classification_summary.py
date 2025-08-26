"""
Create a summary visualization for classification results
"""
import argparse
import json
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def create_summary(features_path, labels_path, model_info_path, threshold):
    """
    Create a comprehensive summary of the classification results
    
    Args:
        features_path: path to features CSV file
        labels_path: path to labels CSV file
        model_info_path: path to model info JSON file
        threshold: intensity threshold used for classification
    """
    # Load data
    features_df = pd.read_csv(features_path)
    labels_df = pd.read_csv(labels_path)
    
    # Merge features and labels for analysis
    df = pd.merge(features_df, labels_df, on=['well_id', 'object_id'])
    
    with open(model_info_path, 'r') as f:
        info = json.load(f)
    
    # Create summary figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Class distribution
    ax = axes[0, 0]
    class_counts = df.label.value_counts()
    colors = {'dead': '#d62728', 'live': '#2ca02c'}
    bars = ax.bar(class_counts.index, class_counts.values, 
                   color=[colors[x] for x in class_counts.index])
    ax.set_title('Class Distribution in Dataset', fontsize=14, fontweight='bold')
    ax.set_xlabel('Class')
    ax.set_ylabel('Count')
    ax.set_ylim(0, max(class_counts.values) * 1.15)
    
    # Add count labels on bars
    for bar, count in zip(bars, class_counts.values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{count}\n({100*count/len(df):.1f}%)',
                ha='center', va='bottom')
    
    # 2. Feature importance
    ax = axes[0, 1]
    importance_data = pd.DataFrame(info['feature_importance'])
    top_features = importance_data.head(8)
    
    # Create horizontal bar chart
    bars = ax.barh(range(len(top_features)), top_features['importance'], 
                    color='steelblue')
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features['feature'])
    ax.set_xlabel('Importance')
    ax.set_title('Top Feature Importance', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    # Add value labels
    for bar, val in zip(bars, top_features['importance']):
        ax.text(val + 0.002, bar.get_y() + bar.get_height()/2, 
                f'{val:.3f}', va='center')
    
    # 3. Intensity distribution by class
    ax = axes[1, 0]
    
    # Create overlapping histograms
    dead_data = df[df.label == 'dead']['gfp_intensity']
    live_data = df[df.label == 'live']['gfp_intensity']
    
    # Determine bin edges for both distributions
    all_data = df['gfp_intensity']
    bins = np.linspace(all_data.min(), all_data.max(), 30)
    
    ax.hist(dead_data, bins=bins, alpha=0.6, label='dead', color='#d62728')
    ax.hist(live_data, bins=bins, alpha=0.6, label='live', color='#2ca02c')
    
    ax.set_xlabel('GFP Channel Intensity (summmed)')
    ax.set_ylabel('Count')
    ax.set_title('Intensity Distribution by Class', fontsize=14, fontweight='bold')
    ax.legend()
    
    # 4. Model performance metrics
    ax = axes[1, 1]
    ax.axis('off')
    
    # Create formatted text with metrics
    metrics_text = f'''Model Performance Summary
    {'='*35}

    Accuracy:           {info['accuracy']:.3f}

    Dataset Split:
      Training:         {info['n_train']} samples
      Validation:       {info['n_val']} samples
      
    Model Complexity:
      Tree Depth:       {info['tree_depth']}
      Leaf Nodes:       {info['n_leaves']}
      Features Used:    {info['n_features']}

    Classification Settings:
      Threshold (T):    {threshold}
      Train Split:      {info['n_train']/(info['n_train']+info['n_val']):.1%}
    '''
        
    ax.text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.2))
    
    # Overall title
    plt.suptitle('Classification Summary', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Save figure
    plt.savefig('classification_summary.png', dpi=150, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', required=True)
    parser.add_argument('--labels', required=True)
    parser.add_argument('--model_info', required=True)
    parser.add_argument('--threshold', type=float, required=True)
    
    args = parser.parse_args()
    create_summary(args.features, args.labels, args.model_info, args.threshold)

if __name__ == '__main__':
    main()