---
layout: post
title: How to Re-grid ERA5-Land Climate Data
description: >
  Two ways to Re-grid ERA5-Land climate dataset
sitemap: false
hide_last_modified: false
---

# How to Re-grid ERA5-Land Climate Data
>**Edited by: Jerry Zhuoer Feng**

### Why Re-gridding?

ERA5-Land provides global hourly high resolution information of climate variables produced by the Copernicus Climate Change Service (C3S) at the European Centre for Medium-Range Weather Forecasts (ECMWF). It contains most meterological variables that we use including wind, temperature, precipitation, and many more. The ERA5-Land dataset covers the period from 1950 to 5 days before the current date and is updated daily. A detailed description of the dataset can be found here: [Overview](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview). 

However, ERA5-Land is a gridded dataset at 0.1° x 0.1° spatial resolution, which may not be what we need. Depends on the research question and the model, we often need to re-grid the data to a different spatial resolution. 

### Method 1: Re-grid GeoTIFF data using Python

**Special thanks to Dr. Shanti Shwarup Mahto for his contribution to this section!**

**This method is intended to be used after downloading ERA5 Data using Method 2 outlined in [ERA5 Data Download](https://critical-infrastructure-systems-lab.github.io/manual/programming/2024-10-21-ERA5-Data-Download/)** 

This code allows you to re-grid the GeoTIFF data you downloaded and output them in netCDF format, which is what we use most of the time. Here the process is done locally, so remember to download all the data you need from your Google Drive and put them in the correct folder before you start running the code below. Here we show the process of re-gridding the ERA5 Land data to 0.05° grid.

```python 
import rasterio
import numpy as np
from netCDF4 import Dataset
import os
from rasterio.warp import calculate_default_transform, reproject, Resampling
from tqdm import tqdm  # For progress bar

# Defind the interval you want in degrees
interval = 0.05

# Define input and output folders
input_folder = 'ERA5_Hourly_raw'
output_folder = 'ERA5_Hourly_' + str(interval)

# Ensure the output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the desired latitude and longitude range
lat_min, lat_max = 0.125, 29.975
lon_min, lon_max = 95.025, 109.975

# Create target longitude and latitude arrays
lon = np.arange(lon_min, lon_max + interval, interval)
lat = np.arange(lat_max, lat_min - interval, -interval)  # Reverse latitude to correct upside-down issue

# Process each .tif file in the input folder
tif_files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

for tif_file in tqdm(tif_files, desc="Converting files"):
    print(f"Processing {tif_file}...")
    input_path = os.path.join(input_folder, tif_file)
    output_path = os.path.join(output_folder, tif_file[:-4] + '.nc')
    year = tif_file[9:-8]

    # Open the .tif file using rasterio
    with rasterio.open(input_path) as src:
        # Define the transform for the desired resolution and bounds
        dst_transform, width, height = calculate_default_transform(
            src.crs, src.crs, len(lon), len(lat),
            left=lon_min, bottom=lat_min, right=lon_max, top=lat_max
        )

        # Create an empty array for the reprojected data
        param = np.empty((src.count, height, width), dtype=np.float32)

        # Reproject each band using bilinear interpolation
        for i in tqdm(range(src.count), desc="Reprojecting bands", leave=False):
            reproject(
                source=src.read(i + 1),
                destination=param[i],
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=src.crs,
                resampling=Resampling.bilinear
            )

    # Define time array
    time = np.arange(param.shape[0])

    # Create the NetCDF file
    with Dataset(output_path, 'w', format='NETCDF4') as nc:
        # Create dimensions
        nc.createDimension('longitude', len(lon))
        nc.createDimension('latitude', len(lat))
        nc.createDimension('time', len(time))

        # Create variables
        longitude = nc.createVariable('longitude', 'f4', ('longitude',))
        latitude = nc.createVariable('latitude', 'f4', ('latitude',))
        times = nc.createVariable('time', 'i4', ('time',))
        param_var = nc.createVariable('2m_temperature', 'f4', ('time', 'latitude', 'longitude'), zlib=True, complevel=4)

        # Assign data to variables
        longitude[:] = lon
        latitude[:] = lat
        times[:] = time
        param_var[:, :, :] = param

        # Add attributes
        longitude.units = 'degrees_east'
        latitude.units = 'degrees_north'
        times.units = f'days since {year}-01-01'
        param_var.units = 'degree Celsius'

    print(f'NetCDF file created for {tif_file}')
```

### Method 2: Re-grid the data using Climate Data Operators in Linux

Climate Data Operators is a collection of command line Operators to manipulate and analyze Climate data developed by Max Planck Institute for Meteorology. CDO is an incredibly powerful tool to process climate data, which carries out complex operations in a single line or two. For more information, check out [Overview]("https://code.mpimet.mpg.de/projects/cdo"). If you are interested in a comprehensive guide to CDO, check out the tutorial here: [User Guide]("https://code.mpimet.mpg.de/projects/cdo/embedded/index.html"). Unfortunately, CDO only works in a Linux environment, so you need to setup a Linux environment to use this, and figure out a way to transfer file between Linux and Windows.

Installing CDO in Linux is easy:

```
sudo apt-get install cdo
```

In Windows, you will have to build it from source. A instruction is given here [CDO for Windows](https://code.mpimet.mpg.de/projects/cdo/wiki/Win32). I have not tested this, so feel free to give it a try and update the Lab Manual if it works!

In CDO, we use the *remapbil* function to re-grid the data, which performs a bilinear interpolation. This can be done in a single line:

```
cdo remapbil,targetgrid ifile ofile
```

The *targetgrid* part is slightly nuanced. Essentially, you will need a file (often .txt) that contains the number of rows, columns, cell size, and the coordinates of the lower left corner. Kindly approach me or Dr. Shanti for the grid desciption file. you can read more about it here [Re-gridding with CDO](https://www.climate-cryosphere.org/wiki/index.php/Regridding_with_CDO)
