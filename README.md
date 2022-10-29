# Bison Lab

All analysis code related to the Bison Lab project at Earthshot Institute.

## Getting Started

### Prerequisites
* An Anaconda Python distribution is required as this simplifies the installation. Either `Miniconda` or `Conda` are suitable: please follow the [conda installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Setup

* In terminal/command line, navigate to your preferred software directory and clone this reposity to your local computer

```
# with SSH key
git clone git@github.com:earthshot-institute/bison-lab.git

# or with username/password
git clone https://github.com/earthshot-institute/bison-lab.git
```

Create a Conda (see prerequisites above if you don't have Conda installed) environment called `bison-lab` in which we can install all libraries/dependencies for this repository:

1. CD into the bison-lab project directory you cloned from GitHub.
2. Run the Conda command to create an environment based on the environment.yml configuration file in the bison-lab project directory.
```bash
conda env create -f environment.yml
```
3. (Optional) If you want to use the `Jupyter Lab` interface, install the widget to enable leaflet maps
```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet
```

4. **Before running any code** activate this conda environment:

```bash
conda activate bison-lab
```

:tada: **You're ready to go!** :tada:


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
