# crash_analysis

Automating standard crash analysis for Vision Zero and other corridor safety projects

### Environment Setup

To create the python environment, run the next line in a conda prompt from the project directory:

`conda env create -f environment.yml`

To activate the new environment, run the following line:

`conda activate crash-analysis`

To update the environment as changes are needed, run the following line:

`conda env update -f environment.yml`

### Running Scripts

To run any of the scripts in this repo, activate the conda environment, change directory to the project folder, and then run the `python` command followed by the path to the file. For example:

```
conda activate crash-analysis
d:
cd dvrpc_shared/crash_analysis
python /scripts/{script_name}.py
```
