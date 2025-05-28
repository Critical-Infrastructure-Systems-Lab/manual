---
layout: page
title: General programming
description: >
  Resources on programming.
hide_description: true
sitemap: false
permalink: /docs/general-programming
---

# Markdown

Markdown is a lightweight markup language for creating formatted text using a plain-text editor. It is widely used for blogging, including our own Lab manual! You can use Markdown for many other things, such as creating slides and other types of presentation material ([example](https://rmarkdown.rstudio.com/index.html)).

## To do list

- Go through [this guide](https://www.markdownguide.org) that will introduce you to Markdown. If you want to practice your Markdown skills, consider writing a post or webpage for this manual!

---

# Introduction to Python and R

In your daily work you will certainly make use of a general-purpose language, such as Matlab, Python, Julia, or R (with the caveat that R is more functional to statistical analysis and data visualization). In our lab, the two commonly used languages are Python and R. Being familiar with one (or both) of them is therefore important. 

## To do list

- Install Python on your computer. The easiest way to do so is to install [Anaconda](https://www.anaconda.com), an open-source distribution of the Python and R programming languages for data science that aims to simplify package management and deployment. Anaconda, together with its interface Anaconda Navigator, allow you to easily manage programming languages and packages.

- Read the [Anaconda documentation](https://docs.anaconda.com).

- Familiarize with Python. There are hundreds of guides available online; our suggestion is to use this Python [tutorial](https://docs.python.org/3/tutorial/index.html).

- Note that R can also be installed as a stand-alone software (i.e., independent of Anaconda). If you are planning to install it in such a way, simply visit the [R Project for Statistical Computing website](https://www.r-project.org). We recommend installing also [RStudio](https://posit.co/download/rstudio-desktop/), an integrated development environment for R.

- Familarize with [RStudio](https://docs.posit.co/ide/user/) and [R](https://www.r-project.org/other-docs.html).
  
---
 
# Python coding standard
When working on a long-term collaboration project with others, adopting a consistent coding standard is key. This practice not only improves the readability and maintainability of the codebase, saving you from future headaches, but also develops industry-valued skills.

## To do list

- Familiarize yourself with the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html). While the choice of a specific style guide is subjective, Google Python Style Guide offers a comprehensive set of common rules along with clear explanations and examples.
- Streamline your coding workflow by configuring [your favourite IDE](https://code.visualstudio.com/docs/python/formatting) to automatically format your code with tools, such as [Black](https://www.freecodecamp.org/news/auto-format-your-python-code-with-black/).

---

# GitHub

[GitHub](https://github.com) is a developer platform that allows developers to create, store, manage and share their code. It uses [Git](https://www.git-scm.com) software, providing the distributed version control of Git plus access control, bug tracking, software feature requests, task management, continuous integration, and wikis for every project. It is commonly used to host **open-source software** development.

Our team relies heavily on GitHub, and all our software projects are hosted on the [CIS Lab GitHub page](https://github.com/Critical-Infrastructure-Systems-Lab)--including the group manual. The expectation is that, over time, you will become a GitHub proficient user.

## To do list

- Open an account on [GitHub](https://github.com).

- Ask [Stefano](emailto:galelli@cornell.edu) to give you access to the [CIS Lab GitHub page](https://github.com/Critical-Infrastructure-Systems-Lab).

- Take the [online training](https://skills.github.com) provided on GitHub website. We recommend proceeding as follows:
  - Start with **Introduction to GitHub**
  - Take all modules on **First day on GitHub**
  - Take all modules on **First week on GitHub** (*Code with Codespaces* and *Code with Copilot* are optional)

---

# How to organize a (GitHub) repository

A well-organized GitHub repository improves code readability, promotes collaboration, and supports reproducibility. Below are general guidelines for structuring a research-oriented repository.

## Recommended Directory Structure

```
your-project/
├── README.md # Project overview and usage
├── LICENSE # Open-source license (e.g., MIT, GPL)
├── .gitignore # Files/folders to exclude from version control
├── environment.yml # Conda environment (or use requirements.txt for pip)
├── src/ # Source code
│ └── main.py
├── notebooks/ # Jupyter or R Markdown notebooks
│ └── analysis.ipynb
├── data/
│ ├── raw/ # Raw input data (never modified)
│ └── processed/ # Cleaned data used in analysis
├── docs/ # Additional documentation (e.g., for GitHub Pages)
│ └── index.md
├── tests/ # Unit and integration tests
│ └── test_main.py
└── results/ # Figures, tables, model outputs, logs
```


## Key Files and Their Roles

- `README.md`: Overview, installation instructions, usage examples.
- `LICENSE`: Declares how the code can be reused or modified.
- `.gitignore`: Prevents tracking of temporary or large files (e.g., `*.Rhistory`, `*.pyc`, `data/`).
- `requirements.txt` / `environment.yml`: Captures project dependencies. Use `renv` for R.

## Best Practices

- Use meaningful file and function names.
- Comment non-trivial code and include docstrings or roxygen documentation.
- Do **not** commit large datasets. Instead, store them externally or regenerate them from raw sources.
- Include at least minimal automated tests (`tests/`) and instructions on running them (see below).
- Use GitHub Issues and Pull Requests to track progress and code changes.

## To do list

- read this write-up on organizing research code: [How to structure a Python data science project](https://drivendata.github.io/cookiecutter-data-science/)

---

# Introduction to unit testing

Ensuring software reliability is an integral part of high-quality research, and unit tests help ensure the software is behaving as expected. Unit testing focuses on verifying that the building blocks -- small modular units of functions, classes, and methods -- work correctly. Many open-source projects report their test coverage, or the percentage of codebase tested. While high coverage does not guarantee the software is bug-free, it lends confidence to users that the code has been thoroughly tested. Ultimately, unit testing helps us squash bugs early in development, provide confidence when making code changes, and implicitly document the way individual code units are expected to work. 

In Python, popular unit testing frameworks include `unittest` and `pytest`. These frameworks automate the process of running tests and reporting results.

## To do list
- Read a tutorial on unit testing in Python [here](https://www.datacamp.com/tutorial/unit-testing-python).
- Familiarize with implementing unit testing by looking at [PowNet 2.0](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet/tree/master/src/test_pownet)

---

# Linux for research

[GNU/Linux](https://www.gnu.org/gnu/linux-and-gnu.html) is the powerhouse (operating system) behind most of our research group's computing clusters. Mastering the command line is required for running computational experiments. If you want a first dive into Linux, then check our blog post [here](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-07-10-tutorial-linux-1/). A deeper dive into this topic requires taking a short course on Bash Scripting.

## To do list

- Read our [tutorial](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-07-10-tutorial-linux-1/)

- Take a [Bash Scripting Tutorial](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/).

---

# Cluster basics

The [Cornell University Center for Advanced Computing (CAC)](https://www.cac.cornell.edu) provides several computing resources. As part of the EWRS concentration, we have access to [Hopper](https://www.cac.cornell.edu/techdocs/clusters/Hopper/), a 22 compute nodes (c0001-c0022) with dual 20-core Intel Xeon Gold 5218R CPUs @ 2.1 GHz and 192 GB of RAM. This is likely the first cluster you will use.

## To do list (Getting started with Hopper)

- To use Hopper, submit the [request form](https://www.cac.cornell.edu/services/external/RequestCACid.aspx?ProjectID=vs498_0001) to CAC. Also email Professor [Vivek Srikrishnan](emailto:vs498@cornell.edu) to ask for his approval of the request.

- While waiting for the approval, read and understand this [guide](https://github.com/Cornell-EWRS/hopper) to get started with Hopper.

---

# Large-scale computing

... **to be completed**

## To do list

- ...

- ... **To be completed**

---

# Google Earth Engine

Another resource you may use is Google Earth Engine ... **to be completed**

## To do list

- ...

- ... **To be completed**

---

# Software documentation

Software documentation provides information about a software program for everyone involved in its creation, deployment and use. **To be completed**

## To do list

- Open an account on [Read the Docs](https://about.readthedocs.com).

- ... **To be completed**

