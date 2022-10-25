# Bison Lab

All analysis code related to the Bison Lab project at Earthshot Institute.

## Getting Started


### Setup

* In terminal/command line, navigate to your preferred software directory and clone this reposity to your local computer

```
# with SSH key
git clone git@github.com:earthshot-institute/bison-lab.git

# or with username/password
git clone https://github.com/earthshot-institute/bison-lab.git
```

An Anaconda Python distribution is required as this simplifies the installation. Either `Miniconda` or `Conda` are suitable: please follow the [conda installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Once Conda is installed, we can create a conda environment called `bison-lab` in which we can install all libraries/dependencies for this repository:

```bash
conda env create -f environment.yml
```

**Before running any code** activate this conda environment:

```bash
conda activate bison-lab
```

The environment can be deactivated with:

```bash
conda deactivate
```

#### Code Quality

To run code quality tooling on every commit, we need to install the [pre-commit](https://pre-commit.com) Git hook:

```bash
pre-commit install
```

Now on every commit, the hooks configured in the .pre-commit-config.yaml will be executed.


### Uninstall

To remove the `bison-lab` conda environment:

```bash
conda env remove -n bison-lab
```

### Notebooks

Run Jupyter from the notebooks directory.

You have the option of using [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html):

```bash
jupyter lab
```

or the "classic" Jupyter notebook:

```bash
jupyter notebook notebooks/
```
