// Parameters
params.data_dir = "${projectDir}/../../data/"

// Actual workflow
workflow {
    // First, let's process the masks
    binary_mask_files = Channel.fromPath("${params.data_dir}/raw/BBBC010_v1_foreground_eachworm/*_ground_truth.png")

    // Create (well ID, filename) pairs for each mask file
    grouped_masks = binary_mask_files.map { file -> 
            tuple(file.baseName.split('_')[0], file)
    }.groupTuple()
    
    COMBINE_BINARY_MASKS(grouped_masks)

    // Second, let's process the different image channels  
    image_files = Channel.fromPath("${params.data_dir}/raw/BBBC010_v2_images/*.tif")

    // Identify the well IDs
    grouped_images = image_files.map { file ->
        def matcher = file.baseName =~ /([A-Z]\d{2})/ // Extract well ID (e.g., "A01")
        def well_id = matcher[0][1] 
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
    python ${projectDir}/combine_masks.py \\
        --well_id ${well_id} \\
        --binary_masks ${binary_mask_files.join(' ')}
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
    python ${projectDir}/merge_channels.py \\
        --well_id ${well_id} \\
        --channels ${channel_files.join(' ')}
    """
}

// Cleanup on successful workflow completion -- remove if you want to be able to debug!
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