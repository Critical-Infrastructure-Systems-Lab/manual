---
layout: post
title: How to Download ERA5-Land Climate Data
description: >
  Two ways to download ERA5-Land climate dataset
sitemap: false
hide_last_modified: false
---

# How to Download ERA5 Climate Data
>**Edited by: Jerry Zhuoer Feng**

### What is it?

ERA5-Land provides global hourly high resolution information of climate variables produced by the Copernicus Climate Change Service (C3S) at the European Centre for Medium-Range Weather Forecasts (ECMWF).

ERA5-Land is a gridded dataset at 0.1° x 0.1° spatial resolution and an hourly temporal resolution. It contains most meterological variables that we use including wind, temperature, precipitation, and many more. The ERA5-Land dataset covers the period from 1950 to 5 days before the current date and is updated daily. A detailed description of the dataset can be found here: [Overview](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview). 

### Why do I need a script to download it?

Although there is a website to download the data, you will find out that you cannot multi-select Year or Month using the website.

### Method 1: Downloading data using Climate Data Store API
**Disclaimer: Currently there seems to be a rather small limit on how much data you can download at once. If you need to bulk download data e.g., 10+ years, it is recommended to take the detour lined out in Method 2.** 

First you will need a ECMWF account. you can register an account for free here: [Registration](https://cds.climate.copernicus.eu/). This will give you a personal API. Install the Climate Data Store API in your local environment just like any other Python library:

```
pip install cdsapi
```

To setup the API, follow the instructions here: [API Setup](https://cds.climate.copernicus.eu/how-to-api).

You can now request and download data using a python script like the one below. The official website [Website](https://cds.climate.copernicus.eu/datasets/derived-era5-land-daily-statistics?tab=download) contains a helpful tool that helps you to generate the Python code, but you need to change some of the parameters due to the multi-select limit mentioned above.

```python 
import cdsapi
dataset = "reanalysis-era5-land"
request = {
    "variable": [
        "2m_temperature",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "total_precipitation"
    ], # Check the variable name on the official website
    "year": [
        "2021", "2022", "2023"
    ], # list of years
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
    ], # list of months
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ], # list of days
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ], # list of timestamps
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [90, -180, -90, 180] # North, West, South, East
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
```

### Method 2: Downloading data using Google Earth Engine

The Google Earth Engine method is slightly more complicated, but it allows us to bypass the download limit in Method 1. You can find out more about the dataset here: [Catalog](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY). Unfortunately, Google's website only gives you the instruction in JavaScript, so let's take a look at how to download it in python.

#### Step 1: Create a Earth-Engine-Enabled Google Cloud Project

Google requires a Cloud Project to use the Google Earth Engine authentication flow. Create one here: [Create Google Cloud Project](https://console.cloud.google.com/projectcreate). Remember the name of your project, it will be needed later when calling the API.

You will then need to enable the Google Earth Engine API for the project you just created here: [Enabling API for Your Project](https://console.cloud.google.com/apis/library/earthengine.googleapis.com). Make sure you are signed in and double check the project name in the upper left hand corner.

#### Step 2: Authenticate inside Python

First install the Google Earth Engine API in your Python environment:

```
pip install earthengine-api
```

You will then need to import and authenticate the API. Run the following code: 

```python
import ee
ee.Authenticate()
ee.Initialize(project='era5-land-data')
```

You will be prompted to follow a URL in **your Python IDE** to generate a code and paste in a box in **your Python IDE**. After that you are done! One thing to note, the authentication expires after being idle for one week, so if you come back to your project after a while, you may need to do the authentication again.

#### Step 3: Download the data

**Special thanks to Dr. Shanti Shwarup Mahto for his contribution to this section!**

After authenticating the Google Earth Engine API, you can download the data using the code below. Remember to run the authentication bloc before this!

```python
import os
import time
from datetime import datetime, timedelta

# Define the Area of Interest (AOI)
geometry = [95, 30, 110, 0]  # Top-left(lon, lat) and Bottom-right(lon, lat) coordinates
geometry = ee.Geometry.Rectangle(geometry)

# Change with your location in the Google Drive
dtdr = '/'
os.chdir(dtdr)
data_download_directory1 = 'ERA5_Hourly_raw'  # Folder name in your Google Drive, if the folder does not exist, it will create a new folder.
start_date = datetime(2009, 7, 1)
end_date = datetime(2018, 12, 31)

current_date = start_date

while current_date <= end_date:
    next_date = current_date + timedelta(days=1)
    
    dataset = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY') \
                .filterDate(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')) \
                .filterBounds(geometry)
                
    count = dataset.size().getInfo()
    print(f"Number of images between {current_date.strftime('%Y-%m-%d')} and {next_date.strftime('%Y-%m-%d')}: {count}")
    
    # Select the variable
    def process_image(image):
        layer1 = image.select('temperature_2m').subtract(273.15)  # Correct method name
        return layer1.copyProperties(image, ['system:time_start'])
           
    dataset = dataset.map(process_image)
                 
    dataset = dataset.map(lambda image: image.clip(geometry))
    
    # Make a stack by combining all 24 hourly images into a single multi-band image
    hourly_stack = dataset.toBands()
    print(current_date)
    #================================= Daily Stack
    export_params1 = {
        'image': hourly_stack,
        'description': f"ERA5Land_{current_date.strftime('%Y%m%d')}",
        'scale': 11000,
        'fileFormat': 'GeoTIFF',
        'region': geometry,
        'crs': 'EPSG:4326',
        'folder': data_download_directory1,
        'maxPixels': 1e13,
        'formatOptions': {'cloudOptimized': True}
    }
    # Export the image as a cloud-optimized GeoTIFF to Google Drive
    task = ee.batch.Export.image.toDrive(**export_params1)
    task.start()
    print(f"Exporting daily file: {current_date.strftime('%Y-%m-%d')}")
    current_date = current_date + timedelta(days=1)
```

A caveat of this is that the data is downloaded in your Google Drive instead of locally, so you will need to retrieve it from your Google Drive. Another caveat is that this code only **creates** a series of requests, not downloading the files directly. **This means that the files are not downloaded (yet!) after the code has finished running.** Depend on the size of your request, your internet speed, and the Google Earth Engine server, you may need to wait a significant while (more than an hour) before all the files requested show up in your Google Drive. Finally, these codes download files in GeoTIFF format, which may or may not be what you need. To post-process this, refer to the tutorial on *How to Re-grid ERA5 Climate Data*.
