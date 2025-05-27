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
