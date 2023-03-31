# **__PPG Signals Data Extraction__**

## Table of Contents
- [**__PPG Signals Data Extraction__**](#ppg-signals-data-extraction)
  - [Table of Contents](#table-of-contents)
  - [__Installation__](#installation)
  - [__Usage__](#usage)
    - [.csv File and Folder Requirements Contents](#csv-file-and-folder-requirements-contents)
    - [Output File Structure](#output-file-structure)
  - [__Contributing__](#contributing)
    - [Reporting Issues](#reporting-issues)
    - [Contributing Code](#contributing-code)
  - [__Contact__](#contact)
  - [__License__](#license)
  - [__References__](#references)
    - [HRV Analysis](#hrv-analysis)


## __Installation__
1. Create a new directory
'mkdir [Directory]`

2. Clone github repository<br>
`git clone https://github.com/gtm1235/betweenmd_api_sql.git`

3. <u>**Switch to current Repository <font style="color: red;">refactor</font>**</u><br>
`git checkout refactor`

4. Create a python venv in the root directory<br>
`python -m venv venv`

5. Create csv Directory or directories

6. place PPG CSV files in directory

7. Activate the venv<br>
`source ./venv/bin/activate`

8. Install the requirements<br>
`python -m pip install -r requirements.txt`

9. Run the app.py file<br>
`python -m main`

__Postgres DB will automatically deploy and build tables the first time the app is run.__
__Be sure to have the .env file properly setup at first run__

## __Usage__

### .csv File and Folder Requirements Contents

### Output File Structure


## __Contributing__
Contributions will be restricted to those working with betweenMD on its various projects [License](#license).  Please contact Gennaro Maida at betweenMD [Contact](#contact) [contribution guidelines](#contributing-code).

### Reporting Issues
If you find any issues with the project, please open an issue on our [GitHub repository](https://github.com/your-repo-name/issues). Be sure to include as much detail as possible, including steps to reproduce the issue.

### Contributing Code
1. Fork the project.
2. Create a new branch.
3. Make your changes and commit them to your branch.
4. Push your changes to your fork.
5. Open a pull request on our [GitHub repository](https://github.com/your-repo-name/pulls) with a description of your changes.

We'll review your pull request as soon as possible. Thank you for contributing!

## __Contact__
Gennaro Maida
betweenMD, LLC
Gennaro@betweenmd.com

## __License__
MIT License with additional non-commercial use restriction - see the LICENSE file for details.

## __References__
### HRV Analysis

The HRV Analysis library is a Python package for analyzing heart rate variability (HRV) data. The library provides a wide range of tools for calculating HRV statistics, plotting HRV data, and performing time-domain, frequency-domain, and non-linear HRV analyses.

The HRV Analysis library is developed and maintained by the HRV Analysis development team [1]. If you use this library in your research, please cite the following paper:

[1] HRV Analysis Development Team. (2021). hrv-analysis: A Python library for heart rate variability analysis. Zenodo. https://doi.org/10.5281/zenodo.5521308




