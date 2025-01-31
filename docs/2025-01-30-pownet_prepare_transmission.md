---
layout: page
title: Preparing Transmission input for PowNet
description: >
  Guide on preparing "transmission.csv" as required by PowNet
hide_description: true
sitemap: false
permalink: /docs/pownet_prepare_transmission
---
By: Phumthep Bunnak Jan 30th, 2025

## Introduction

When modeling a power system, the transmission system determines the amount of electricity that can be transferred from point A to point B. In PowNet, the transmission system is modeled with a linearized power flow formulation. Currently, the package supports the Kirchhoff formulation and an angle-based formulation. For further details on the formulations of linearized power flow, please see an article by [Hörsch et al. (2022)](https://doi.org/10.1016/j.epsr.2017.12.034)


### What is `transmission.csv` in PowNet?

The file `transmission.csv` captures the topology of the transmission system. Specifically, we treat substations as nodes and transmission lines as edges. As PowNet is constantly updated, the required CSV format may change. However, the following fields are typically needed in `transmission.csv`.

- source: The name or ID of the starting substation of the transmission line.
- sink: The name or ID of the ending substation of the transmission line.
- source_kv: The voltage level (in kV) at the starting substation.
- sink_kv: The voltage level (in kV) at the ending substation.
- distance: The length of the transmission line (km).
- n_circuits: The number of parallel circuits making up the transmission line.
- source_lon: The longitude of the starting substation.
- source_lat: The latitude of the starting substation.
- sink_lon: The longitude of the ending substation.
- sink_lat: The latitude of the ending substation.
- user_line_cap: The user-defined line capacity (in MW). Leave blank or enter -1 if you do not wish to define your own value.
- user_susceptance: The user-defined line susceptance. Leave blank or enter -1 if you do not wish to define your own value.


### Where can we get data on the transmission lines?

Getting data for transmission lines is actually one of the most challeging tasks when modeling a power system. Here are a few tried-and-true data sources.

1. Utility Reports: Official reports from electric utilities sometimes contain maps or data about their transmission systems.  These can be a valuable starting point, though the level of detail varies.

2. OpenStreetMap (OSM): OSM is a free, crowd-sourced map of the world.  While it may contain some transmission line data, its completeness and accuracy can vary by region.

3. Open Infrastructure Map: This is a paid service that provides infrastructure data, including power lines. It may offer more comprehensive coverage than OSM.

4. Manual Digitization (with satellite imagery): In some cases, you might have to manually digitize transmission lines from satellite imagery (e.g., Google Maps). This is probably not something you want to manually do for a large system!


### Scripts

We have created a Python script to process transmission data from Open Infrastructure Map for use by `PowNet`. To use this script, a user must first purchase a `.gpkg` containing geospatial information of a transmission system. To use this script, ensure you have the following Python packages installed: `Pandas`, `Numpy`, `Sci-kit Learn`, `NetworkX`, `Geopandas`, `Shapely`, and `Scipy.`

- `process_geospatial.py`: This is the main script that the user runs.  It requires the user to specify the location of the .gpkg file. [Download Link](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/process_geospatial.py)
- `geospatial_utils.py`: Although the user does not need to run this file, it contains supporting functions for `process_geospatial.py`. Therefore, the user must keep both Python files in the same directory. [Download Link](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/geospatial_utils.py).
