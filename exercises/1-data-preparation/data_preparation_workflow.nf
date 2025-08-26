// Parameters
params.data_dir = "${projectDir}/../../data/"

// Actual workflow
workflow {
    // First, let's process the masks by creating a channel for the binary mask files
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: the files are in "${params.data_dir}/raw/BBBC010_v1_foreground_eachworm/" and all have a name that ends with "_ground_truth.png"
    binary_mask_files = ...

    // Create (well ID, filename) pairs for each mask file
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: use file.baseName to get each file's name and split() to parse it
    grouped_masks = binary_mask_files.map { file -> 
            tuple(..., file)
    }.groupTuple()
    
    COMBINE_BINARY_MASKS(grouped_masks)

    // Second, let's process the different image channels  
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: the files are in "${params.data_dir}/raw/raw/BBBC010_v2_images/" and all have a name that ends with ".tif"
    image_files = ...

    // Identify the well IDs
    // YOUR TURN! Replace the "..." below with your code!
    // Hint: use file.baseName to get each file's name and a regular expression pattern to extract the well ID (e.g., "A01") in it
    grouped_images = image_files.map { file ->
        def matcher = ... // 
        def well_id = ... 
        tuple(well_id, file)
    }.groupTuple()
    
    MERGE_CHANNELS(grouped_images)
}

// Define the process that combines binary masks for the same well into a single instance segmentation mask
process COMBINE_BINARY_MASKS {
    publishDir "${params.data_dir}/masks", mode: 'copy'
    
    input:
    tuple val(well_id), path(binary_mask_files)
    
    output:
    path("${well_id}_instances_mask.tif")
    
    script:
    """
    # YOUR TURN! Replace the "..." below with your code!
    # Use the provided combine_masks.py script
    # Hint: use the ${projectDir} variable to provide the path to the script
    python ...
    """
}

// Define the process that merges images of the same well into a single two-channel image
process MERGE_CHANNELS {
    publishDir "${params.data_dir}/images", mode: 'copy'
    
    input:
    tuple val(well_id), path(channel_files)
    
    output:
    path("${well_id}_multichannel_image.tif")
    
    script:
    """
    # YOUR TURN! Replace the "..." below with your code!
    # Use the provided merge_channel.py script
    # Hint: use the ${projectDir} variable to provide the path to the script
    python ...
    """
}