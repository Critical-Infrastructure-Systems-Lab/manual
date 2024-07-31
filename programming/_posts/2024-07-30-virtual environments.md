---
layout: post
title: A Practical Guide to Python Virtual Environments
description: >
  A first introduction to Python virtual environments
sitemap: false
hide_last_modified: false
---

# A Practical Guide to Python Virtual Environments
>**Edited by: Phumthep Bunnak**

### The problem: dependency hell

Imaging you're juggling two Python projects simultaneously. Your first project, analyzing historical stocks data, relies on a specific version of the Pandas package (version 1.5.3, let's say). Your second project, a cutting-edge machine learning model, demands the latest features of Pandas 2.1.0.

Here's where things get tricky: A critical function in Pandas has changed between these two versions. In 1.5.3, a function expects a certain argument order; in 2.1.0, the order is completely different. Trying to run both projects in the same environment can lead to errors and crashes and headaches. This is a classic example of "dependency hell".


### The solution: virtual environments
A virtual environment in Python is a self-contained directory that houses a specific Python Installation (interpretor/version) and a set of packages independent of other Python environments. In other words, each virtual environment has its own
- Python interpreter. This makes it easy to have multiple Python versions on your machine simultaneously.
- Specific versions of Python packages. A Python package (e.g. Pandas) is not shared across environment.

Python virtual environments are isolated workspaces for your projects, preventing package and version conflicts. This isolation extends to software installed in other virtual environments and the default Python installation that might come with your operating system. Each environment is disposable and not tracked by version control systems like Git [^1]. You can customize each virtual environment to match a project’s specific requirements, ensuring ease of deployment and reproducibility across machines. Having a distinct virtual environment for each project helps maintain a clean and streamlined project workflow, free of dependency issues.

Several tools can create and manage virtual environments, but `conda` shines for our research group's coding projects because `conda` has a large community of users, making it easy to find support. Ultimately, the choice of virtual-environment manager depends on your project needs.


### Why choose Anaconda over Pip (and when to use both)
If Python comes with `pip`, a perfectly functioning package installer, why bother with `conda`? The short answer is that `conda` offers capabilities beyond `pip`'s scope. While `pip` solely manages Python packages, `conda` not only manages Python packages but also Python versions themselves, along with non-Python dependencies like C/C++ libraries often required by scientific computing or data analysis tools. Using `pip` outside a virtual environment can lead to conflicts with other system-wide Python applications, as `pip` installs packages globally. In contrast, `conda` ensures that your project's dependencies remain isolated and don't interfere with other installations. Additionally, `conda`'s intelligent solver automatically identifies and resolves conflicts among packages, saving time by avoiding the need to manually installing and removing multiple dependencies. 

It's important to note that `conda` and `pip` are not mutaully exclusive and can be used together effectively. In fact, a `conda` environment comes with `pip` pre-installed, enabling their simultaneous use in some workflow. The recommended practice is to first install all necessary packages using `conda`. Anaconda boasts curated channels with a wide selection of Python packages. However, if a specific package is not available through Anaconda channels, then you can easily switch to the bundled `pip` within your `conda` environment to install the package from the PyPI ecosystem.

### Creating Virtual Environments with Anaconda (3 Ways)

We will now explore three cases for creating a virtual environment using Anaconda.

1. Creating a custom environment from scratch:

```bash
conda create -n my_pandas_project python=3.9
conda activate my_pandas_project
conda install pandas=1.5.3
```

This creates an environment named `my_pandas_project` with Python 3.9 and then installs Pandas version 1.5.3.

2. Creating an environment based on a requirement file:

If your project already has a `requirements.txt` file listing its dependencies:

```bash
conda create -n my_pandas_project python=3.9
conda activate my_pandas_project
conda install --file requirements.txt
```

This ensures that you get the exact package versions specified in the file. This approach avoids installing a package one-by-one.

3. Bonus: Installing a forked GitHub repo as a package:

This approach is ideal when collaborating with others. 

Create a folder for your project (e.g., `stock_analysis`). Inside that folder, run:

```bash
conda env create -f environment.yml
conda activate stock_analysis
```

An `environment.yml` file is similar to `requirements.txt` but often contains more detailed dependency information.


### Best Practices
- Keep your projects organized and prevent conflicts by having one environment per project
- Use descriptive names for environments (e.g., stock_analysis_v1) to avoid confusion
- Keep an updated environment.yml or requirements.txt file when developing a project

### [Bonus] Using `pip` to install a local project to a `conda` environment

Instead of just installing packages from online sources, `pip` allows you to install Python projects directly from your local machine. This setup is especially useful when you have developed your own packages or working with code not yet published online. Here's how to do it within a `conda` environment.

1. Activate an environment (or create one if you haven't)
    ```
    conda activate <your_environment_name>
    ```

2. Navigate to your project folder. Use your terminal to move to the root directory of your local project containing the `setup.py` or `pyproject.toml` file.

3. Install with `pip` using the following command:
    ```
    pip install -e .
    ```

The `-e` flag (short for "editable") installs your project in "development mode." This means that any changes you make to your project's code will be immediately reflected in the `conda` environment without needing to reinstall. With these steps, you can develop and use your local Python package!



### Links
[^1]: For more details: https://docs.python.org/3/library/venv.html

