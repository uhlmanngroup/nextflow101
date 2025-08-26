# NextFlow 101

### To use

1. Have [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) and [git](https://git-scm.com/downloads) installed

2. Clone this repository on your local machine, open a Terminal window, and move to the repository's folder:
    ```
    cd /my/file/path/to/nextflow101/
    ```

3. Create conda environment from yaml file:
    ```
    mamba env create -f nextflow101_env.yml
    ```

4. Activate environment:
    ```
    source activate nextflow101
    ```

5. Download the [BBBC010 dataset](https://bbbc.broadinstitute.org/BBBC010), more specifically:

* The original images provided as [BBBC010_v2_images.zip (70 MB)](https://data.broadinstitute.org/bbbc/BBBC010/BBBC010_v2_images.zip)
* The binary segmentation masks for each object provided as [BBBC010_v1_foreground_eachworm.zip (2.7 MB)](https://data.broadinstitute.org/bbbc/BBBC010/BBBC010_v1_foreground_eachworm.zip)

6. Place the two .zip in the `data/raw` subfolder, and unzip them - that will create two directories (`BBBC010_v2_images`, 200 files, and `BBBC010_v1_foreground_eachworm`, 1407 files) 

7. Move to the `exercises` subfolder:
    ```
    cd exercises/
    ```

8. Move to the specific exercise subfolder of your choice:
    ```
    cd N-my-favourite-exercise/
    ```

9. Read the corresponding `README.md` and complete the exercise

10. If you get stuck, solutions are provided in the `solutions` subfolder.

### Troubleshooting

If the `nextflow101_env.yml` fails to install for whichever reason, try to create it manually with the following:
    ```
    mamba create -n nextflow101-manual python=3.10
    source activate nextflow101-manual     
    
    mamba install nextflow -c bioconda -c conda-forge
    mamba install numpy
    mamba install scikit-image
    mamba install scikit-learn
    mamba install pandas
    mamba install matplotlib
    mamba install seaborn
    ```

Then close your terminal window, open a new one, and continue at point 3 of the "to use" instructions above.

### To cite

If you use or refer to this tutorial, please acknowledge it as follows:

Uhlmann, V. (2025) NextFlow 101 Tutorial. github.com/uhlmanngroup/nextflow101

### Further resources

* GloBIAS Seminar Series: NextFlow for BioImage Analysis by Christian Tischer, Tong Li, Miguel Ibarra and Tim-Oliver Buchholz, [available on YouTube](https://youtu.be/xjM_zy1RYQQ?si=8g3yRCdqWxi-0LkY).
* Minimal Nextflow OME-Zarr workflow from Tong Li, [available on GitHub)(https://github.com/BioImageTools/ome-zarr-image-analysis-nextflow).

### Acknowledgements
Ignacio Arganda-Carreras (University of the Basque Country, Spain), Anna Klemm (Scilifelab & Uppsala University, Sweden), Perrine Paul-Gilloteaux (University of Nantes, France), and Christian Tischer (EMBL Heidelberg, Germany) are to be thanked for prompting the creation of this tutorial in the context of the [2025 EMBO Practical Course on Advanced methods in bioimage analysis](https://www.embl.org/about/info/course-and-conference-office/events/bia25-01/).
