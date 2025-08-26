# Exercise 1: Data Preparation

In this exercise, you will create a workflow for the [BBBC010 dataset](https://bbbc.broadinstitute.org/BBBC010) that

1. combines the binary foreground/background segmentation masks for individual worms into a single instance segmentation mask for each well, where each object has a unique ID;

2. Merge the GFP and brighfield channel images provided as separate files into a multichannel TIFF file for each well.

### Learning goals

1. NextFlow fundamentals
   - Understand the structure of a NextFlow workflow
   - Define processes with inputs, outputs, and scripts
   - Work with parameters and configuration files

2. Channel operations
   - Create channels from file paths using `Channel.fromPath()`
   - Transform and group data with the `.map()` and `.groupTuple()` operators

3. Data flow patterns
   - Understand how data flows between processes
   - Write results in specific directories

4. File pattern matching
   - Extract information from filenames using string operations and regular expressions
   - Write outputs with meaningful naming conventions

### How to go about this exercise

* Open `data_preparation_workflow.nf` with your favourite code editor and complete the sections marked with `YOUR TURN! Replace the "..." below with your code!` - to do so, you will have to open an examine the provided Python scripts 

* Once you have completed the missing pieces of code, run your workflow:
	```
	nextflow run data_preparation_workflow.nf
   ```

* Debug when needed by
	* inspecting the nextflow log: NextFlow saves an execution log in a `.nextflow.log` file that can be opened in a text editor

	* checking the current directory for failed tasks: NextFlow creates a `work` subdirectory into which it saves a trace of everything it does! In the error traceback that appears in your Terminal, look for the working directory where the error happened, e.g.:
    ```
	Work dir:
  /Users/myname/my/path/to/nextflow101/exercises/1-data-preparation/work/bf/d7f0c2e2609...
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

* If you are stuck, check the solution in `../../solutions/01-data-preparation/`!

### Further resources

* [Documentation on NextFlow scripts](https://www.nextflow.io/docs/latest/script.html)
* [Test and debug your regular expressions with RegEx101](https://regex101.com/)
