---
layout: page
title: Other software
description: >
  Resources and examples on how to use software developed by other teams.
hide_description: true
sitemap: false
permalink: /docs/other-software
---

# Weather generators

## Multi-site and distributed stochastic weather generators

* [IBMWeatherGen](https://github.com/IBM/IBMWeatherGen), gridded, multisite, multivariate, and daily stochastic weather generator based on resampling methodology (Python).
* [Stochastic Weather Generator v2.0](https://github.com/nassernajibi/WGEN-v2.0), weather-regime based stochastic weather generator (R).
* [RWGEN](https://github.com/rwgen1/rwgen?tab=readme-ov-file), stochastic spatiotemporal Rainfall and Weather GENerator built around the Neyman-Scott Rectangular Pulse (NSRP) rainfall model (Python).
* [AWE-GEN-2D](https://hyd.ifu.ethz.ch/research-data-models/awe-gen-2d.html), a stochastic weather generator that simulates gridded climate variables at high spatial and temporal resolution for present and future climates (Matlab).
* [wxgen](https://github.com/metno/wxgen?tab=readme-ov-file), a command-line tool for generating arbitrarily long weather time-series. The generator produces gridded output for multiple variables (e.g. temperature, precipitation) and aims to have realistic covariances in space, time, and across variables (Python).

## Single-site weather generators

* [weathergen](https://walkerjeffd.github.io/weathergen/), provides a set of functions for generating synthetic climate timeseries (R).

## Streamflow generators

This is a good [introduction](https://waterprogramming.wordpress.com/2017/08/29/open-source-streamflow-generator-part-i-synthetic-generation/) on the topic of stochastic streamflow generations.

* [Kirsch-Nowak_Streamflow_Generator](https://github.com/julianneq/Kirsch-Nowak_Streamflow_Generator). This repository contains code for generating correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Monthly flows are generated using Cholesky decomposition and then disaggregated to daily flows by proportionally scaling daily flows from a randomly selected historical month +/- 7 days (Matlab / Python).


# Sensitivity analysis

* [SAFE toolbox](https://safetoolbox.github.io), available in Python, R, and Matlab. In addition to the software documentation, users can refer to [Pianosi et al. (2015)](https://www.sciencedirect.com/science/article/pii/S1364815215001188?via%3Dihub).
* [SALib](https://github.com/SALib/SALib), available in Python. Similarly to SAFE, it implements commonly used sensitivity analysis methods.

A good starting point to start learning sensitivity analysis is the review by [Pianosi et al. (2016)](https://www.sciencedirect.com/science/article/pii/S1364815216300287).


# Multi-Objective Evolutionary Algorithms 

MOEAs are effective tools used to solve [black-box optimization](https://en.wikipedia.org/wiki/Derivative-free_optimization) problems. They are popular in the domain of environmental engineering because of the number of black-box optimization problems we solve (e.g., calibration of simulation models, simulation-based optimization). An excellent starting point to MOEAs is the introductory overview by [Maier et al. (2019)](https://www.sciencedirect.com/science/article/abs/pii/S1364815218305905), while more advanced readings are the reviews by [Reed et al. (2013)](https://www.sciencedirect.com/science/article/abs/pii/S0309170812000073) and [Maier et al. (2016)](https://www.sciencedirect.com/science/article/abs/pii/S1364815214002679). Libraries we typically use are:

* [Platypus](https://platypus.readthedocs.io/en/latest/), a framework for evolutionary computing in Python with a focus on multiobjective evolutionary algorithms (MOEAs). It differs from existing optimization libraries, including PyGMO, Inspyred, DEAP, and Scipy, by providing optimization algorithms and analysis tools for multiobjective optimization.
* [MOEA Framework](https://moeaframework.org), an open source Java library for developing and experimenting with multiobjective evolutionary algorithms (MOEAs) and other metaheuristics.
* [Borg](http://borgmoea.org), a state-of-the-art optimization algorithm developed by David Hadka and Patrick Reed.

**Note** that many of these tools are developed by our colleague Pat Reed, so more details can be found on the Reed Group [lab manual](https://reedgroup.github.io/intro.html).


# netCFD 

NetCDF (Network Common Data Form) is a widely used file format for storing multi-dimensional scientific data such as temperature, precipitation, wind, and other environmental variables. It is designed for efficient access, sharing, and analysis of large datasets—especially those varying over space and time. It is very popular because it stores structured array data (e.g., time × latitude × longitude), it is self-describing (metadata for variables and dimensions), it supports compression and efficient partial reads, and it is platform-independent. Tools and Libraries:

* `xarray`, `netCDF4`, and `h5netcdf` for programmatic access and analysis.
* Command-line: [NCO](https://nco.sourceforge.net) and [CDO](https://www.unidata.ucar.edu/software/netcdf/workshops/2012/third_party/CDO.html) (Climate Data Operators) for quick processing (e.g., subsetting, averaging).
* Visualization: [Panoply](https://www.giss.nasa.gov/tools/panoply/) for browsing and plotting NetCDF files



