# Public Release Synthetic Data and Code

## Project Repository Structure

This repository contains data and code needed to reproduce the main results for our [paper]() Dissecting Racial Bias in an Algorithm Used to Manage the Health of Populations. 

1. *data*: A synthetic master dataset that closely mirrors the dataset used to produce our original results (which cannot be shared to protect patient privacy).
2. *code*: Code in R and Python that can be used to replicate the figures and tables from the main manuscript.
3. *results*: Our own replication of these results using the synthetic dataset.

## Synthetic Dataset Creation

Beginning with our final analytic files for the study, we used the [synthpop](https://cran.r-project.org/web/packages/synthpop/index.html) R package to create a synthetic version of the key variables needed to replicate all analyses in the paper. 

The synthetic dataset contains the same number of observations (patient-years) as our original dataset. The package uses classification and regression trees to sequentially generate variables that captures the moments and covariances of the original dataset. More details can be found at https://cran.r-project.org/web/packages/synthpop/synthpop.pdf.

We include a [data dictionary](./data/data_dictionary.md) describing each of the individual variables. 


## Preparation

- Set working directory to `dissecting-bias`
    - `cd dissecting-bias`
- `R` environment setup:
    - Install our utility package:
        1. `R CMD INSTALL plot0_0.1.tar.gz`
- `python` environment setup:
    - Create our conda environment:
        1. `conda env create -f bias.yml`

## Execution
- To replicate figures:
    - `Rscript code/figure1/figure1.R`
        - 'figure1.R' imports results from `figure1b.R`, but there's no need to
          run them separately to produce figure1.
        - If you would like to run `figure1b.R` separately and genearted `figure1b.csv`, run `Rscript code/figure1/figure1b.R`.
    - `Rscript code/figure2.R`
    - `Rscript code/figure3.R`
- To train model and save predictions on the holdout:
    - `python code/model/main.py`
        - Please remember to switch environment (`source activate bias`) when running `python` code.
- To replicate tables:
    - `python code/table1.py`
    - `python code/table2.py`
        - `table3.R` imports results from `table2.py`, please make sure to run
          `table2.py` prior to running `table3.R`
    - `Rscript code/table3.R`

Let us know if there are any issues/questions! Zoey Li (@lizeyu), Katie Lin (@kl2532), Ziad Obermeyer (@ziadoo)
