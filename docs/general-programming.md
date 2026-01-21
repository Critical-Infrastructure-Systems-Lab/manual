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
- Check out a good example, [PowNet](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet)!

---

# GitHub Actions (Optional but Powerful)

**GitHub Actions** is a built-in automation tool that lets you run tasks every time code is pushed, a pull request is opened, or on a custom schedule. For example, you can use Actions to:

- Automatically run tests when someone pushes a change
- Check that your code follows formatting rules
- Deploy a website or update documentation
- Re-run simulations on a schedule (e.g., daily or weekly)

A GitHub Action is configured in a YAML file (e.g., `.github/workflows/test.yml`) and can be set up to run code in Python, R, or Bash.

## Example Use Case

A simple `test.yml` workflow might:
1. Set up an R or Python environment
2. Install your package or scripts
3. Run unit tests from the `tests/` folder

## To do list

Start here:  

- [GitHub Actions Documentation](https://docs.github.com/en/actions)  
- Example: [R workflows from r-lib](https://github.com/r-lib/actions/tree/v2/examples)

---

# Introduction to unit testing

Ensuring software reliability is an integral part of high-quality research, and unit tests help ensure the software is behaving as expected. Unit testing focuses on verifying that the building blocks -- small modular units of functions, classes, and methods -- work correctly. Many open-source projects report their test coverage, or the percentage of codebase tested. While high coverage does not guarantee the software is bug-free, it lends confidence to users that the code has been thoroughly tested. Ultimately, unit testing helps us squash bugs early in development, provide confidence when making code changes, and implicitly document the way individual code units are expected to work. 

In Python, popular unit testing frameworks include `unittest` and `pytest`. These frameworks automate the process of running tests and reporting results.

## To do list
- Read a tutorial on unit testing in Python [here](https://www.datacamp.com/tutorial/unit-testing-python).
- Familiarize with implementing unit testing by looking at [PowNet 2.0](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet/tree/master/src/test_pownet)

---

# Writing Software Documentation

Well-documented code accelerates collaboration, reduces onboarding time, and enhances reproducibility. In our lab, we pair in-code documentation with external documentation hosted on [ReadTheDocs](https://readthedocs.io), using GitHub as the source of truth.

## Types of Documentation

1. **Docstrings / Roxygen Comments**  
   These live inside the code and explain what each function or class does, what it expects as input, and what it returns.
   - Python: Use triple-quoted docstrings in either NumPy or Google format.
   - R: Use `#'` comments above each function (with `{roxygen2}`) to generate help files.

2. **README.md**  
   Every repository should have a clear and minimal README that includes:
   - A short project description
   - How to install dependencies
   - How to run key scripts or reproduce key figures

3. **Narrative Documentation**  
   For larger projects, we maintain full documentation websites that include:
   - Overview of the model or tool
   - Installation and setup instructions
   - Usage examples and tutorials
   - Auto-generated API reference from in-code docstrings

## GitHub & ReadTheDocs: How It Works

We use **ReadTheDocs** to host our documentation and **GitHub** to store the code and doc sources. ReadTheDocs connects to GitHub and builds the documentation automatically every time a change is pushed to the `main` branch (or another branch if configured). Each project includes a `docs/` folder (for Sphinx) and a configuration file (`conf.py`). The docs are written in reStructuredText (`.rst`) or Markdown, and can include embedded code blocks, figures, equations, and links to the API.

To enable this:
- The repo must be public (or have a ReadTheDocs subscription if private).
- You must activate the repo on [ReadTheDocs.org](https://readthedocs.org/), link it to the GitHub repo, and configure a build environment (e.g., `requirements.txt` or `readthedocs.yml`).
- Optional: Use versioned docs (e.g., stable vs. dev branches).

## Lab Example: PowNet

The [`PowNet`](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet) repository uses this setup effectively. Its documentation is automatically built and hosted at [https://pownet.readthedocs.io](https://pownet.readthedocs.io). 

It includes:
- A clear system overview
- Installation instructions
- Tutorials on how to run dispatch models
- An API reference auto-generated from Python docstrings

## Best Practices

- Write docstrings as you code (not afterward).
- Include usage examples, figures, or outputs where appropriate.
- Keep narrative docs concise but complete.
- Make sure your README links to the full docs.

---

# Linux for research

[GNU/Linux](https://www.gnu.org/gnu/linux-and-gnu.html) is the powerhouse (operating system) behind most of our research group's computing clusters. Mastering the command line is required for running computational experiments. If you want a first dive into Linux, then check our blog post [here](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-07-10-tutorial-linux-1/). A deeper dive into this topic requires taking a short course on Bash Scripting.

## To do list

- Read our [tutorial](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-07-10-tutorial-linux-1/)

- Take a [Bash Scripting Tutorial](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/).

---

#  Cluster basics (CPU and GPU resources)

Please discuss with Stefano about your computing needs before proceeding with any of the resources described below.

## Free resources at Cornell

- As part of the EWRS concentration, we have free access to [Hopper](https://www.cac.cornell.edu/techdocs/clusters/Hopper/), a 22 compute nodes (c0001-c0022) with dual 20-core Intel Xeon Gold 5218R CPUs @ 2.1 GHz and 192 GB of RAM. This is likely the first cluster you will use. To use Hopper, submit the [request form](https://www.cac.cornell.edu/services/external/RequestCACid.aspx?ProjectID=vs498_0001) to CAC. Also email Professor [Vivek Srikrishnan](emailto:vs498@cornell.edu) to ask for his approval of the request. While waiting for the approval, read and understand this [guide](https://github.com/Cornell-EWRS/hopper) to get started with Hopper.

- The [Cornell University Center for Advanced Computing (CAC)](https://www.cac.cornell.edu) maintains Red Cloud, Cornell's on-premise cloud. Cornell students, faculty, and staff are eligible for a free [Red Cloud Exploratory Project Account](https://www.cac.cornell.edu/services/GPUs.aspx), which includes: 165 core hours, 50GB of storage, and 1 hour of consulting assistance. Note that Red Cloud provides both CPU and GPU resources. 

- The [Cornell Center for Social Sciences](https://socialsciences.cornell.edu/computing-and-data/cloud-computing-solutions) provides computing resources in a cloud environment with a wide range of available software. Cloud options include shared and dedicated computing servers. Based on member college approval, these resources are available to current Cornell faculty researchers, students and staff for research use only. 

## Empire AI

- With [Empire AI](https://www.empireai.edu), New York State is first in the nation to establish a consortium of public and private research institutions (including Cornell) advancing AI research for the public good at this scale. Within Cornell, this is part of the [Cornell AI Initiative](https://ai.cornell.edu). Access to Empire AI is provided through grant applications.

## ACCESS

- [ACCESS](https://access-ci.org) is a program established and funded by the U.S. National Science Foundation to help researchers and educators, with or without supporting grants, to utilize the nation’s advanced computing systems and services. ACCESS is available to students, researchers, and faculty members. In our lab, we use ACCESS  for large-scale simulations or heavy AI training.

- [Project Types](https://allocations.access-ci.org/project-types): ACCESS uses a tiered system for projects based on the scale of your needs:
   o **Explore ACCESS**: Ideal for code development, benchmarking, or small-scale research. It provides 400,000 credits and is usually approved within one business day.
   o **Discover ACCESS**: Designed for modest research needs as you move past the benchmarking phase. Provides 1,500,000 credits.
   o **Accelerate & Maximize**: Intended for large-scale research or multi-grant programs requiring significant computational power. 

- To get started:
   o Create an account: Register for an [ACCESS account](https://allocations.access-ci.org/get-your-first-project) using your institutional email. Do not use personal domains like Gmail.
   o Request your first project: Prepare a brief project title and abstract (1-page) and submit it via the [Get Started portal](https://allocations.access-ci.org/get-your-first-project). If you are a graduate student, you will need to upload a signed letter from Stefano affirming your role.
   o Browse available resources: Before requesting time, review the [Resource Catalog](https://allocations.access-ci.org/resources) to find the right hardware.

- Managing your allocations: Once a project is approved, you are awarded ACCESS Credits. These must be "exchanged" for specific resource hours before you can log in.
   o Exchange Credits: Navigate to your project management page and select "Exchange." Use the [Exchange Calculator](https://allocations.access-ci.org/exchange_calculator) to determine how many credits correspond to CPU/GPU hours on your chosen cluster.
   o Login and Setup: After the exchange is approved (usually 1–5 days), your Resource Username will appear on the project dashboard. 
   o Add Collaborators: If you are leading a project, you can add other lab members to the allocation via the project dashboard using their ACCESS IDs.

---

# Large-scale computing

Some of the computational experiments in our lab, such as simulation-optimization or uncertainty analysis, can take hours or days to complete if run sequentially. **Large-scale computing** refers to strategies that divide this work across multiple cores, CPUs, or even machines, enabling experiments to finish faster and scale to more realistic problem sizes.

One of the most widely used technologies for this is **MPI (Message Passing Interface)**. MPI enables programs to run **in parallel** by distributing tasks to separate processes that communicate with each other. In our lab, we typically do not write raw MPI code. Instead, we use **high-level libraries** like `mpi4py` (Python) or configure **batch jobs via SLURM** on a cluster like Hopper. 

## When you might need this
- Running thousands of ensemble simulations or inflow scenarios
- Training multiple policies in parallel
- Performing grid search over large parameter spaces

## Tools and Languages
- `mpi4py`: Python interface to MPI (used in some of our reservoir tools)
- `joblib` or `multiprocessing`: For simpler parallelism on shared memory
- `SLURM`: Job scheduler used on Hopper to submit parallel tasks
- `sbatch`: Command-line tool to launch jobs across nodes

## Example from our lab

In the [`PowNet`](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet) repository, we use cluster computing to run large-scale power system dispatch simulations. These jobs are often parallelized across multiple scenarios using **SLURM job arrays**, which are configured with Bash scripts and submitted to Cornell’s Hopper cluster. While the actual SLURM scripts may not be included in the public repo, they are used internally and follow Hopper conventions. Refer to the [Hopper guide](https://github.com/Cornell-EWRS/hopper#slurm) for templates and examples.

## To do list (Getting started with parallel computing)

- Read the SLURM section in the [Hopper guide](https://github.com/Cornell-EWRS/hopper#slurm)
- If using Python, read the [mpi4py tutorial](https://mpi4py.readthedocs.io/en/stable/tutorial.html)

---



