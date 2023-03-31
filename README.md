# Performance of Three Panel Data Estimators

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nebisimsek/epp_final_project/main.svg)](https://results.pre-commit.ci/latest/github/nebisimsek/epp_final_project/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Structure

This project aims to compare the performance of three different panel data estimators
under different scenarios. These three estimators are pooled estimator, one-way fixed
effect estimator and two-way fixed effect estimator.

To see their performance under different scenarios, I create a very flexible function
that you can easily change endogeneity structure with *c_unit* and *c_time*; they
correspond to the correlation constant of time-invariant and unit-invariant factors. You
can also add a trended variable with *c_trend* and determine the intensity. Finally with
*c_var* one can control for the variation over time.

After running the project the simulated results will appear under **bld** folder. The
results are categorized concerning the values *c_unit*, *c_time*, *c_var* and *c_trend*
taken. A report will be automatically created as well.

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate epp_final_project
```

To build the project, type

```console
$ pytask
```

If some of the tasks fail when plotting the results please run it one more time.

The number of simulation, observation and time has decreased due to faster running time.
These values are adjustable under **task_analysis** folder.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
