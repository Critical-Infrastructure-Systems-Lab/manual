---
layout: page
title: Other software - Systems
description: >
  Resources and examples on how to use software developed by other teams (systems).
hide_description: true
sitemap: false
permalink: /docs/other-software-systems
---

## Sensitivity analysis

* [SAFE toolbox](https://safetoolbox.github.io), available in Python, R, and Matlab. In addition to the software documentation, users can refer to [Pianosi et al. (2015)](https://www.sciencedirect.com/science/article/pii/S1364815215001188?via%3Dihub).
* [SALib](https://github.com/SALib/SALib), available in Python. Similarly to SAFE, it implements commonly used sensitivity analysis methods.

A good starting point to start learning sensitivity analysis is the review by [Pianosi et al. (2016)](https://www.sciencedirect.com/science/article/pii/S1364815216300287).


## Multi-Objective Evolutionary Algorithms 

MOEAs are effective tools used to solve [black-box optimization](https://en.wikipedia.org/wiki/Derivative-free_optimization) problems. They are popular in the domain of environmental engineering because of the number of black-box optimization problems we solve (e.g., calibration of simulation models, simulation-based optimization). An excellent starting point to MOEAs is the introductory overview by [Maier et al. (2019)](https://www.sciencedirect.com/science/article/abs/pii/S1364815218305905), while more advanced readings are the reviews by [Reed et al. (2013)](https://www.sciencedirect.com/science/article/abs/pii/S0309170812000073) and [Maier et al. (2016)](https://www.sciencedirect.com/science/article/abs/pii/S1364815214002679). Libraries we typically use are:

* [Platypus](https://platypus.readthedocs.io/en/latest/), a framework for evolutionary computing in Python with a focus on multiobjective evolutionary algorithms (MOEAs). It differs from existing optimization libraries, including PyGMO, Inspyred, DEAP, and Scipy, by providing optimization algorithms and analysis tools for multiobjective optimization.
* [MOEA Framework](https://moeaframework.org), an open source Java library for developing and experimenting with multiobjective evolutionary algorithms (MOEAs) and other metaheuristics.
* [Borg](http://borgmoea.org), a state-of-the-art optimization algorithm developed by David Hadka and Patrick Reed.

**Note** that many of these tools are developed by our colleague Pat Reed, so more details can be found on the Reed Group [lab manual](https://reedgroup.github.io/intro.html). 
