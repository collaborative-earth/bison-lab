# Bison Lab

All analysis code related to the Bison Lab project at Earthshot Institute.

## Getting Started

### Notebooks

Create and activate the conda environment.

```bash
conda env create -f env-notebooks.yml
conda activate bison-lab-notebooks
```

Run Jupyter from the notebooks directory.

```bash
jupyter notebook notebooks/
```

### Code Quality

To run code quality tooling on every commit install [pre-commit](https://pre-commit.com). First,
pip install the extra requirements and then install the pre-commit Git hook.

```bash
pip install -r requirements-extra.txt
pre-commit install
```

Now on every commit, the hooks configured in the .pre-commit-config.yaml will be executed.
