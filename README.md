# Next Flow 101

### To use

1. Have [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) and [git](https://git-scm.com/downloads) installed

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

If you use or refer to this tutorial, please acknowledge it as follows:

Uhlmann, V. (2025) NextFlow 101 Tutorial. github.com/uhlmanngroup/nextflow101

### Further resources

* GloBIAS Seminar Series: NextFlow for BioImage Analysis by Christian Tischer, Tong Li, Miguel Ibarra and Tim-Oliver Buchholz, [available on YouTube](https://youtu.be/xjM_zy1RYQQ?si=8g3yRCdqWxi-0LkY).
* Minimal Nextflow OME-Zarr workflow from Tong Li, [available on GitHub)(https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow).

### Acknowledgements
Ignacio Arganda-Carreras (University of the Basque Country, Spain), Anna Klemm (Scilifelab & Uppsala University, Sweden), Perrine Paul-Gilloteaux (University of Nantes, France), and Christian Tischer (EMBL Heidelberg, Germany) are to be thanked for prompting the creation of this tutorial in the context of the [2025 EMBO Practical Course on Advanced methods in bioimage analysis](https://www.embl.org/about/info/course-and-conference-office/events/bia25-01/).


