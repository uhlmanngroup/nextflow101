// Parameters
params.data_dir = "${projectDir}/../../data/"
params.intensity_threshold = 3.0 // Threshold for live/dead classification - examine the provided extract_features_and_labels.py script to understand how it works!
params.train_split = 0.7  // Proportion of the data for the training set 

// Actual workflow
workflow {
    // First, let's load the images...
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: the files are in "${params.data_dir}/images/" and all have a name that ends with "_multichannel_image.tif"
    images = ...
    
    // ...and the masks
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: the files are in "${params.data_dir}/masks/" and all have a name that ends with "_instances_mask.tif"
    masks = ...
    
    // Pair the images with their corresponding masks
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: Use .join() to pair images and masks by their common well_id
    paired_data = ...
    
    // Extract features for each object in each image
    (feature_files, label_files) = EXTRACT_FEATURES_AND_LABELS(paired_data)

    // Combine features and labels from all images together into a data collection
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: use .collect() to gather all feature/label files into a list, then call COMBINE_FEATURES_AND_LABELS and recover its outputs in a tuple
    ... = ...

    // Train a decision tree to classify live from dead worms based on their features 
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: call TRAIN_CLASSIFIER and recover its outputs in a tuple
    ... = ...
    
    // Generate some performance readouts 
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: call CREATE_SUMMARY using the outputs from the previous steps
    ...
}

// Define the process that extracts the features for each object and its label
process EXTRACT_FEATURES_AND_LABELS {
    publishDir "${params.data_dir}/features", mode: 'copy', pattern: '*.csv'
    
    input:
    tuple val(well_id), path(image), path(mask)
    
    output:
    // Define two separate CSV file outputs - one for features and one for labels
    // YOUR TURN! Replace the "..." below with your code!
    ...
    ...
    
    script:
    """
    # YOUR TURN! Replace the "..." below with your code!
    # Use the provided extract_features_and_labels.py script
    python ...
    """
}

// Define the process that combines features from all objects into a single data structure
process COMBINE_FEATURES_AND_LABELS {
    publishDir "${params.data_dir}", mode: 'copy'
    
    input:
    path(feature_files)
    path(label_files)
    
    output:
    path("all_features.csv")
    path("all_labels.csv")
    
    script:
    """
    python ${projectDir}/combine_features_and_labels.py \\
        --output_features all_features.csv \\
        --output_labels all_labels.csv
    """
}

// Define the process that trains a decision tree 
process TRAIN_CLASSIFIER {
    publishDir "${params.data_dir}/model", mode: 'copy'
    
    input:
    path(features)
    path(labels)
    
    output:
    path("confusion_matrix.png")
    path("decision_tree.png")
    path("classification_report.txt")
    path("model_info.json")
    
    script:
    """
    python ${projectDir}/train_classifier.py \\
        --features ${features} \\
        --labels ${labels} \\
        --train_split ${params.train_split}
    """
}

// Process to create summary visualization
process CREATE_SUMMARY {
    publishDir "${params.data_dir}", mode: 'copy'
    
    input:
    path(features)
    path(labels)
    path(model_info)
    
    output:
    path("classification_summary.png")
    
    script:
    """
    python ${projectDir}/create_classification_summary.py \\
        --features ${features} \\
        --labels ${labels} \\
        --model_info ${model_info} \\
        --threshold ${params.intensity_threshold}
    """
}