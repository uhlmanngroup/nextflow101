"""
Train a decision tree classifier for live/dead worm classification
"""
import argparse
import json
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def train_classifier(features_path, labels_path, train_split):
    """
    Train a decision tree classifier on the worm features
    
    Args:
        features_path: path to features CSV (no labels!)
        labels_path: path to labels CSV
        train_split: proportion of data for training
    """
    
    # Load features and labels separately
    features_df = pd.read_csv(features_path)
    labels_df = pd.read_csv(labels_path)
    
    print(f'Loaded {len(features_df)} feature vectors')
    print(f'Loaded {len(labels_df)} labels')
    
    # Merge on well_id and object_id to ensure alignment
    df = pd.merge(features_df, labels_df[['well_id', 'object_id', 'label']], 
                  on=['well_id', 'object_id'], how='inner')
    
    if len(df) != len(features_df):
        print(f'WARNING: only {len(df)} matches found between features and labels!')
    
    # Prepare features (X) and labels (y)
    feature_columns = [col for col in features_df.columns 
                      if col not in ['well_id', 'object_id']]
    X = df[feature_columns].values # data
    y = df['label'].values # labels
    
    # Split data and stratify to maintain class balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        train_size=train_split,
        stratify=y
    )
    
    # Train decision tree
    classifier = DecisionTreeClassifier(
        max_depth=5,  # limit depth for interpretability
    )
    classifier.fit(X_train, y_train)
    
    # Predictions
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f'\nValidation accuracy: {accuracy:.3f}')
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': classifier.feature_importances_
    }).sort_values('importance', ascending=False)
    print('\nTop 5 important features:')
    print(feature_importance.head())
    
    # Save confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=['dead', 'live'])
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['dead', 'live'], 
                yticklabels=['dead', 'live'])
    plt.title(f'Confusion Matrix (accuracy: {accuracy:.3f})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=150)
    plt.close()
    
    # Save decision tree visualization
    plt.figure(figsize=(20, 10))
    plot_tree(classifier, 
              feature_names=feature_columns,
              class_names=['dead', 'live'],
              filled=True,
              rounded=True,
              fontsize=10)
    plt.title('Decision Tree Classifier')
    plt.tight_layout()
    plt.savefig('decision_tree.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Save classification report
    report = classification_report(y_test, y_pred, target_names=['dead', 'live'])
    with open('classification_report.txt', 'w') as f:
        f.write('Classification Report\n')
        f.write('='*50 + '\n')
        f.write(report)
        f.write('\n\nFeature Importance:\n')
        f.write(feature_importance.to_string())
    
    print('\nClassification Report:')
    print(report)
    
    # Save model info
    model_info = {
        'accuracy': float(accuracy),
        'n_train': len(X_train),
        'n_val': len(X_test),
        'n_features': len(feature_columns),
        'tree_depth': int(classifier.get_depth()),
        'n_leaves': int(classifier.get_n_leaves()),
        'feature_importance': feature_importance.head(10).to_dict('records')
    }
    with open('model_info.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print('\nModel saved successfully!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', required=True)
    parser.add_argument('--labels', required=True)
    parser.add_argument('--train_split', type=float, required=True)
    
    args = parser.parse_args()
    train_classifier(args.features, args.labels, args.train_split)

if __name__ == '__main__':
    main()