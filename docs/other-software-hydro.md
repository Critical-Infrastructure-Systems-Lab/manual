---
layout: page
title: Other software - Hydro
description: >
  Resources and examples on how to use software developed by other teams (hydro).
hide_description: true
sitemap: false
permalink: /docs/other-software-hydro
---

## VIC (Variable Infiltration Capacity) Hydrologic Model

The **Variable Infiltration Capacity (VIC)** model is a semi-distributed, macroscale hydrologic model widely used for simulating the terrestrial water and energy balance over large domains, such as river basins or continental regions. Designed for applications in climate impact studies, water resources assessment, and hydrologic forecasting, VIC has become a foundational tool in computational hydrology.

There are two major versions of VIC currently in use. **VIC 4.x** is the legacy version, written in C with a relatively monolithic structure. It includes the core hydrologic processes such as surface runoff, baseflow, evapotranspiration, snow accumulation and melt, and energy balance at the land surface. Though still used in some studies, it is no longer under active development.

In contrast, **VIC 5.x** introduces a modular architecture that improves extensibility and maintainability. It retains the core hydrologic logic of VIC 4.x but adds multiple “drivers” that define how the model is run and how input/output is handled. These include the **Classic Driver** (backward compatible with 4.x), the **Image Driver** (using NetCDF I/O and parallelism with MPI), the **CESM Driver** (for coupling with the Community Earth System Model), and a **Python Driver**, which provides bindings to the C code for integration into Python-based workflows. While the Python interface is still experimental, it offers a promising direction for modern hydrologic modeling pipelines.

The VIC model requires gridded meteorological inputs, typically daily or sub-daily precipitation, temperature, and wind speed. Model parameters include soil and vegetation properties, topographic information, and land cover fractions, which must be prepared in a structured format. Outputs vary by driver but often include streamflow, soil moisture, snow water equivalent, and evapotranspiration, typically saved as NetCDF files.

To assist with preparing and processing these inputs and outputs, the [`tonic`](https://github.com/UW-Hydro/tonic) Python package provides a suite of utilities tailored for VIC. For routing streamflow through river networks, VIC can be paired with [`RVIC`](https://github.com/UW-Hydro/RVIC), a companion routing model. In our lab, we typically use [VIC-Res](https://github.com/Critical-Infrastructure-Systems-Lab/VICRes) for routing purposes.

The current version of the model and source code is hosted on GitHub: [https://github.com/UW-Hydro/VIC](https://github.com/UW-Hydro/VIC).

- **VIC 4.x Documentation**: [https://vic.readthedocs.io/en/vic.4.2.d/](https://vic.readthedocs.io/en/vic.4.2.d/)
- **VIC 5.x Documentation**: [https://vic.readthedocs.io/en/master/](https://vic.readthedocs.io/en/master/)

For post-processing VIC output or developing your own workflows, we recommend using Python packages such as `xarray`, `netCDF4`, and `matplotlib` to analyze and visualize the model’s gridded data products.

---

## netCFD 

NetCDF (Network Common Data Form) is a widely used file format for storing multi-dimensional scientific data such as temperature, precipitation, wind, and other environmental variables. It is designed for efficient access, sharing, and analysis of large datasets—especially those varying over space and time. It is very popular because it stores structured array data (e.g., time × latitude × longitude), it is self-describing (metadata for variables and dimensions), it supports compression and efficient partial reads, and it is platform-independent. Tools and Libraries:

* `xarray`, `netCDF4`, and `h5netcdf` for programmatic access and analysis.
* Command-line: [NCO](https://nco.sourceforge.net) and [CDO](https://www.unidata.ucar.edu/software/netcdf/workshops/2012/third_party/CDO.html) (Climate Data Operators) for quick processing (e.g., subsetting, averaging).
* Visualization: [Panoply](https://www.giss.nasa.gov/tools/panoply/) for browsing and plotting NetCDF files

---

## Weather generators

### Multi-site and distributed stochastic weather generators

* [IBMWeatherGen](https://github.com/IBM/IBMWeatherGen), gridded, multisite, multivariate, and daily stochastic weather generator based on resampling methodology (Python).
* [Stochastic Weather Generator v2.0](https://github.com/nassernajibi/WGEN-v2.0), weather-regime based stochastic weather generator (R).
* [RWGEN](https://github.com/rwgen1/rwgen?tab=readme-ov-file), stochastic spatiotemporal Rainfall and Weather GENerator built around the Neyman-Scott Rectangular Pulse (NSRP) rainfall model (Python).
* [AWE-GEN-2D](https://hyd.ifu.ethz.ch/research-data-models/awe-gen-2d.html), a stochastic weather generator that simulates gridded climate variables at high spatial and temporal resolution for present and future climates (Matlab).
* [wxgen](https://github.com/metno/wxgen?tab=readme-ov-file), a command-line tool for generating arbitrarily long weather time-series. The generator produces gridded output for multiple variables (e.g. temperature, precipitation) and aims to have realistic covariances in space, time, and across variables (Python).

### Single-site weather generators

* [weathergen](https://walkerjeffd.github.io/weathergen/), provides a set of functions for generating synthetic climate timeseries (R).

### Streamflow generators

This is a good [introduction](https://waterprogramming.wordpress.com/2017/08/29/open-source-streamflow-generator-part-i-synthetic-generation/) on the topic of stochastic streamflow generations.

* [Kirsch-Nowak_Streamflow_Generator](https://github.com/julianneq/Kirsch-Nowak_Streamflow_Generator). This repository contains code for generating correlated synthetic daily streamflow time series at multiple sites assuming stationary hydrology. Monthly flows are generated using Cholesky decomposition and then disaggregated to daily flows by proportionally scaling daily flows from a randomly selected historical month +/- 7 days (Matlab / Python). 








