# Next Flow 101

### To use

1. Have [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), [git](https://git-scm.com/downloads), and [Docker](https://www.docker.com/) installed 

2. Create conda environment from yaml file:
    ```
    mamba env create -f nextflow101_env.yml
    ```

3. Activate environment:
    ```
    conda activate nextflow101
    ```

4. Download the [BBBC010 dataset](https://bbbc.broadinstitute.org/BBBC010), more specifically:

* The original images provided as [BBBC010_v2_images.zip (70 MB)](https://data.broadinstitute.org/bbbc/BBBC010/BBBC010_v2_images.zip)
* The binary segmentation masks for each object provided as [BBBC010_v1_foreground_eachworm.zip (2.7 MB)](https://data.broadinstitute.org/bbbc/BBBC010/BBBC010_v1_foreground_eachworm.zip)

5. Place the two .zip in the `data/raw` subfolder, and unzip them - that will create two directories (`BBBC010_v2_images`, 200 files, and `BBBC010_v1_foreground_eachworm`, 1407 files) 

6. Complete and run the workflows in the different subfolders:
    ```
    nextflow run workflow_name.nf
    ```


### Troubleshooting

### To cite

### Further resources
