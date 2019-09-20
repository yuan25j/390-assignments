# Public Release Data and Code

## Project Repository Structure
1. *data*: we provide a synthetic master dataset that includes all the information needed
   to closely replicate our original results.
2. *code*: we release our code in R and Python to replicate our paper results.
3. *results*: we provide our replication of the results from our synthetic dataset.

## Synthetic Dataset Creation

Beginning with our final analytic files for the study, we used the [synthpop](https://cran.r-project.org/web/packages/synthpop/index.html) R package to create a synthetic version of the key variables needed to replicate all analyses in the paper. We made every effort to limit the number of variables in the synthetic data to the minimum used in the analysis, both for simplicity and to reduce risk of inadvertent disclosure of PHI, so variables not used in any analyses (e.g., hospitalizations, visit details, etc.) were not included.

Briefly, we generate a dataset with the same number of observations (patient-years) as our original dataset. The package uses classification and regression trees to sequentially generate variables that captures the moments and covariances of the original dataset. More details can be found at https://cran.r-project.org/web/packages/synthpop/synthpop.pdf.

We include a [data dictionary](./data/data_dictionary.md) describing each of the individual variables. One note is that, while the original dataset includes multiple observations (years) from the same patient, the synthetic dataset observations do not take this clustering into account; creating adequate time dependencies for multiple years of synthetic data posed significant challenges, and in fact none of our analyses rely on using multiple observations per patient (though of course we do account for this in calculating standard errors in the original paper).


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
