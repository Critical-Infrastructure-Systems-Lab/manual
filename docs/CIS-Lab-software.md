---
layout: page
title: CIS Lab software
description: >
  Resources and examples on how to use and develop our software.
hide_description: true
sitemap: false
permalink: /docs/CIS-Lab-software
---

This page provides an overview of software tools developed and maintained by the CIS Lab. Repositories are organized by application domain.

---

## River Basins

- **[VICRes](https://github.com/Critical-Infrastructure-Systems-Lab/VICRes):** Extends the VIC hydrologic model to represent reservoir storage and operations. The repo includes python wrappers for optimization and sensitivity analysis.

- **[InfeRes](https://github.com/Critical-Infrastructure-Systems-Lab/InfeRes):** A Python package for inferring reservoir water surface area, level and storage volume. Additional resources for InfeRes: [Gathering storage data (for validation purposes) from websites](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-06-16-scraping-a-website/)  

- **[reservoir](https://github.com/Critical-Infrastructure-Systems-Lab/reservoir)**  
  An R package for analyzing, designing, and operating water supply reservoirs.

---  

## Energy Systems

- **[PowNet](https://github.com/Critical-Infrastructure-Systems-Lab/PowNet):** A Python-based production cost model for simulating unit commitment and economic dispatch in large-scale power systems. Additional resources for PowNet:  

  - [Collecting input data (generation, transmission, and demand) from multiple sources](PowNet-input-collection.md)
  - [Esimating solar and wind capacities for PowNet with ERA5 data](./2025-01-27-pownet-solar-wind-inputs.md)
  - [Preparing Transmission input for PowNet](2025-01-30-pownet_prepare_transmission.md)
  - Coming soon: how to create CSV files.

---

## Urban Water

- **[DHALSIM](https://github.com/Critical-Infrastructure-Systems-Lab/DHALSIM):** A digital twin for water distribution systems, integrating hydraulic simulation and cyber-physical security analysis.

- **[epanetCPA](https://github.com/Critical-Infrastructure-Systems-Lab/epanetCPA):** A MATLAB toolbox for modeling the hydraulic response of water distribution systems to cyber-physical attacks.

---

## Streamflow reconstructions

- **[ldsr](https://github.com/Critical-Infrastructure-Systems-Lab/ldsr):** A package for streamflow reconstruction using linear dynamical systems with regularization.

- **[mbr](https://github.com/Critical-Infrastructure-Systems-Lab/mbr):** Implements the Mass-balance-adjusted regression algorithm for sub-annual streamflow reconstruction.

---

## Data Analytics

- **[MATLAB_Iterative_Input_Selection](https://github.com/Critical-Infrastructure-Systems-Lab/MATLAB_Iterative_Input_Selection):** MATLAB implementation of the [Iterative Input Selection (IIS)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/wrcr.20339) algorithm for feature selection in time series data.

- **[w-qeiss](https://github.com/Critical-Infrastructure-Systems-Lab/w-qeiss):** Implements the [Wrapper for Quasi Equally Informative Subset Selection (W-QEISS)](https://ieeexplore.ieee.org/abstract/document/7150365) algorithm for variable selection.

- **[AutoEncoders for Event Detection (AEED)](https://github.com/Critical-Infrastructure-Systems-Lab/aeed):** A Keras-based class for [anomaly detection](https://ascelibrary.org/doi/abs/10.1061/(ASCE)WR.1943-5452.0000983), with application to water sensor networks.

---


