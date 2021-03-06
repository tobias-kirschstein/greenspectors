# The Greenspectors
TUM.ai Makeathon October 2021

![grafik](https://user-images.githubusercontent.com/6200099/137619081-e80e9608-7714-4092-914d-19b6183dcabf.png)  
Link to our [demo](http://tobias-kirschstein.de:8501/)


# 0. Links to docs / presentations / ...
 - [Task planning](https://docs.google.com/document/d/1Ro8nIAeYcWVywB1NEJlZ1F7wzv7KIiPk-sV98JiK3Ro/edit?usp=sharing)
 - [Siemens Q&A](https://docs.google.com/document/d/1Vqd6bRytk_fKfnCmVjwEGyBJnr00Gjnls0Gd2aTCW_E/edit?usp=sharing)
 - [Business Part Ideas](https://docs.google.com/document/d/1RwkyPaZ-CcJfWCudokT2mA4mJjkWvEx7CNlf-2D51Qs/edit?usp=sharing)
 - [Makeathon Github repository](https://github.com/tum-ai/os-makeathon-2021)
 - [Presentation](https://docs.google.com/presentation/d/10jGVwk_PDrPKcCpRgqFM284chptmDy_yHuPH3HSk8E4/edit?usp=sharing)


# 1. Getting Started
## 1.1. Repository Installation

 1. Create a new `conda` environment:  
    ```shell
    conda create -n greenspectors
    ```
    If you don't yet have conda, you can install it here: https://docs.conda.io/en/latest/miniconda.html
 2. Activate the `conda` environment:
    ```shell
    conda activate greenspectors
    ```
 3. Install Python 3.8:
    ```shell
    conda install python=3.8
    ```
 4. Clone the repository:
    ```shell
    git clone git@github.com:tobias-kirschstein/greenspectors.git
    ```
 5. Install the `Greenspectors` repository in development mode (so you don't have to redo it whenever the repo changes):
    ```shell
    pip install -e .
    ```
    This command has to be run in the root directory of your cloned repository (where the folders `notebooks`, `src`, `test` are)
 6. use Jupyter Lab to run notebooks:
    ```shell
    jupyter lab
    ```

## 1.2. Contributing

 - [notebooks](notebooks): All Jupyter notebooks go there
 - [src/greenspectors](src/greenspectors): All regular python modules (that you want to be importable) go there
 - [test](test): Any unit tests go there
 - [setup.cfg](setup.cfg): Add any dependencies you introduce under `install_requires =` (using `package_name~=1.2.3`). These will be installed when `pip install` is called
 - [requirements.txt](requirements.txt): Add the *exact* dependency (using `package_name=1.2.3`)
