// Parameters
params.data_dir = "${projectDir}/../../data/"
params.intensity_threshold = 3.0 // Threshold for live/dead classification
params.train_split = 0.7  // Proportion of the data for the training set 

// Actual workflow
workflow {
    // First, let's load the images...
    images = Channel.fromPath("${params.data_dir}/images/*_multichannel_image.tif")
        .map { file ->
            tuple(file.baseName.split('_')[0], file)
        }
    
    // ...and the masks
    masks = Channel.fromPath("${params.data_dir}/masks/*_instances_mask.tif")
        .map { file ->
            tuple(file.baseName.split('_')[0], file)
        }
    
    // Pair the images with their corresponding masks
    paired_data = images.join(masks)
    
    // Extract features for each object in each image
    (feature_files, label_files) = EXTRACT_FEATURES_AND_LABELS(paired_data)

    // Combine features and labels from all images together into a data collection
    (all_features, all_labels) = COMBINE_FEATURES_AND_LABELS(
        feature_files.collect(),
        label_files.collect()
    )

    // Train a decision tree to classify live from dead worms based on their features 
    (confusion_matrix, decision_tree, classification_report, model_info) = TRAIN_CLASSIFIER(all_features, all_labels)
    
    // Generate some performance readouts 
    CREATE_SUMMARY(
        all_features,
        all_labels,
        model_info
    )
}

// Define the process that extracts the features for each object and its label
process EXTRACT_FEATURES_AND_LABELS {
    publishDir "${params.data_dir}/features", mode: 'copy', pattern: '*.csv'
    
    input:
    tuple val(well_id), path(image), path(mask)
    
    output:
    path("${well_id}_features.csv")
    path("${well_id}_labels.csv")
    
    script:
    """
    python ${projectDir}/extract_features_and_labels.py \\
        --well_id ${well_id} \\
        --image ${image} \\
        --mask ${mask} \\
        --threshold ${params.intensity_threshold}
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

// Cleanup on successful completion
workflow.onComplete {
    if (workflow.success) {
        println "Workflow completed successfully!"
        println "Cleaning up work directory..."
        ["bash", "-c", "rm -rf ${workflow.workDir}"].execute().waitFor()
        println "Cleanup done!"
    } else {
        println "Workflow failed - keeping work directory for debugging"
    }
}