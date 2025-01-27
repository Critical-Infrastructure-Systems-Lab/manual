---
layout: page
title: Preparing Solar and Wind Inputs for PowNet
description: >
  Guide on preparing solar and wind files for PowNet.
hide_description: true
sitemap: false
permalink: /docs/pownet-solar-wind-inputs
---
## Introduction

Variable renewable energy (solar and wind) are treated as generators that can provide instantaneous output subject to availability at each hour. Since solar and wind are dependent on the weather, we can estimate their available using a climate data. The question now is which climate dataset do we use and how do we convert climate variables to site-specific solar and wind capacities?

In this post, we use ERA5 as the climate dataset. ERA5 (ECMWF Reanalysis v5) is a climate reanalysis that provides hourly data on the Earth's climate. To download ERA5 from the Climate Data Store (CDF), we need to first [register an account](https://cds.climate.copernicus.eu/). Once you have registered, you would receive a token for downloading via the API. As for calculating solar and wind capacities, we use the gsee and windpowerlib packages, respectively.


### Tips for faster ERA5 data download

No one wishes to wait hours and hours to download data for their analysis. Likewise, downloading ERA5 data efficiently helps with timely analysis. Here's a breakdown of strategies to accelerate your downloads based on a discussion from the [ECMWF forum](https://forum.ecmwf.int/t/how-to-download-faster/1391).

**Monitor the CDS Queue**: Performance is highly dependent on the queue status which can be monitored [here](https://cds.climate.copernicus.eu/live). While network bandwidth can be a limiting factor, the CDS queue is often the primary bottleneck, especially during peak usage times.

**Minimize Requests**:  The CDS API prioritizes requests based on the number of "items". An item is a set of (variables x levels x dates). Note that this does not include the size of your region (a.k.a. grid cells). Each request incurs overhead as it moves through the queue. Therefore, reducing the number of requests is key. How do we do this? For daily data, submit one request per month, and for monthly data, one request per year. A request should cover your *whole* region instead of multiple smaller regions. You can then subset the downloaded data on your local machine as needed. 

Although this means that a request should have as many variables as possible, I personally prefer downloading variable-by-variable as it simplifies analysis and there could also be a prioritization penalty for total download volume in MB. On this note, the CDS allows downloads up to 10GB in size.

To conclude, each request is for either a full month or full day of data, for one variable, for the entire grid, and then I subset the downloaded netcdf file on the client side.

**Parallel Downloads**: Since the performance is dependent on the queue, why don't submit multiple requests at once to take advantage of the CDS API's ability to handle up to 20 concurrent (or more now?) requests per user? The provided script uses Python's concurrent package to achieve this task. In theory, this allows several requests to progress through the queue simultaneously, significantly reducing overall download time. Practically, I am not so sure...


### Required Python packages

- xarray: This package is built for working with multi-dimensional labeled arrays, making it ideal for handling netCDF files, the format ERA5 data comes in.

- pandas: A data manipulation library of choice.  We'll use pandas to work with time series data extracted from ERA.

- geopandas: Geopandas extends pandas to handle geospatial data.

- gsee: The gsee package provides tools for calculating solar energy yield from ERA5 data.

- windpowerlib: This library focuses on wind power calculations.

- cdsapi:  This package provides an interface to the Climate Data Store's API.


### Scripts

There are four scripts that can help download ERA5 data and calculate hourly solar/wind capacities. These scripts should be placed in the same folder location. Note that "nondispatch_spp.csv" in `extract_solar.py` and `extract_wind.py` is a file containing power stations. Please replace this CSV file with your own data of power stations. The required data include generator name, max capacity, latitude, and longitude.

- [get_era5.py](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/get_era5.py): downloads ERA5 data. Required inputs are the bounding box and whether you would like to get "wind" or "solar" datasets.
- [extract_solar.py](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/extract_solar.py): calculates hourly solar capacity
- [extract_wind.py](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/extract_wind.py): calculates hourly wind capacity
- [nearest_point.py](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/nearest_point.py): provides a function to find the closest point from another dataframe.
