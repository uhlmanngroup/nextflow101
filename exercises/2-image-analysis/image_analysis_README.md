# Exercise 2: Image Analysis

In this exercise, you will create a workflow for the [BBBC010 dataset](https://bbbc.broadinstitute.org/BBBC010) that

1. for each worm in each image, extract shape, intensity, and texture features from the brighfield channel, and generate a class label from the intensity of the GFP channel ("live" or "dead", see the BBBC010 website for more details);

2. combine all the features and labels across images into an aggregated data structure;

3. train a decision tree classifier to distinguish "live" from "dead" worms based on the brightfield channel features;

4. generate a visual summary of the classification results.

> WARNING: you **must** have successfully run the data preparation workflow from exercise 1 (`data_preparation_workflow.nf`) to be able to work on this exercise! 
>
> If you did not manage to complete exercise 1, you can generate the required outputs as follows:
>
>       cd ../../solutions/01-data-preparation/
>       nextflow run data_preparation_workflow.nf

### Learning goals

1. Multi-output process handling
   - Manage processes that generate multiple output files

2. Data aggregation patterns
   - Collect outputs from parallel processes with `.collect()`

3. Complex workflows
   - Build analysis pipelines composed of multiple steps
   - Pass multiple files between processes
   - Manage global parameters throughout the workflow

### How to go about this exercise

* Open `image_analysis_workflow.nf` with your favourite code editor and complete the sections marked with `YOUR TURN! Replace the "..." below with your code!` - to do so, you will have to open an examine the provided Python scripts 

* Once you have completed the missing pieces of code, run your workflow:
	```
	nextflow run image_analysis_workflow.nf
   ```

* Debug when needed by
	* inspecting the nextflow log: NextFlow saves an execution log in a `.nextflow.log` file that can be opened in a text editor

	* checking the current directory for failed tasks: NextFlow creates a `work` subdirectory into which it saves a trace of everything it does! In the error traceback that appears in your Terminal, look for the working directory where the error happened, e.g.:
    ```
	Work dir:
	/Users/myname/my/path/to/nextflow101/exercises/2-image-analysis/work/bf/d7f0c2e2609...
    ```
    Using the actual path from the error message, you can then navigate to the corresponding working directory:
    ```
    cd work/bf/d7f0c2e2609...
    ```
    There, you can examine what happened by looking at the exact command that NextFlow executed (`.command.sh`) and the error output (`.command.err`), which can both be opened in a text editor 

	* re-running the workflow with a more verbose output:
    ```
	nextflow run main.nf -with-trace
	```

* When your workflow completes successfully, check the outputs of your workflow in the `../../data/` folder

* If you are stuck, check the solution in `../../solutions/02-image-analysis/`!

* BONUS: experiment with different parameter values for `intensity_threshold` and `train_split`, and observe how it affects the results!

### Further resources

* [Documentation on NextFlow patterns](https://nextflow-io.github.io/patterns/index.htm)
* [Documentation on scikit-image's region properties (shape and intensity features)](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html)
* [Documentation on scikit-image's texture features](https://scikit-image.org/docs/0.25.x/auto_examples/features_detection/plot_glcm.html)
* [Documentation on scikit-learn's decision trees](https://scikit-learn.org/stable/modules/tree.html)