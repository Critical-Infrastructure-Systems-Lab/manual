---
layout: page
title: PowNet input collection
description: >
  Resources and examples on how to collect input data for PowNet.
hide_description: true
sitemap: false
permalink: /docs/PowNet-input-collection
author: 'Phumthep Bunnak'
---
## Workflow of PowNet Data Collection

Modeling a real-world power system begins with collecting data on both electricity supply and demand. In most Southeast Asian countries, machine-readable datasets of power systems are unavailable, and updated information is spread across various sources. Fortunately, this information is often found in official reports.

The data collection process with gathering annual energy statistics reports and utility business plans. A country may also publish its long-term development plan for the power sector. These documents are usually available from the governmental department responsible for energy management, often called the department of energy, the ministry energy, or the energy regulatory commission. It is also useful to keep an eye out for presentations by officials at international events, as the slides often contain information about existing and planned generation and interconnections.

### Examples of documents

| **Country** | **Document**                                                     | **Comment**                                                                                           |
| ---------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Thailand    | Power Development Plan 2021                                  | PDPs may contain a map of existing and planned infrastructure                                       |
| Thailand    | Energy Statistics of Thailand 2021                           | Statistics on energy supply, demand, and prices                                                       |
| Laos        | The Study on Power Network System Master Plan in Lao People's Democratic Republic | A long-term planning by Japan International Cooperation Agency                                      |
| Malaysia    | Performance and Statistical Information of Electricity Supply in Industry in Malaysia 2016 | Thorough energy statistics by the Energy Commission (Suruhanjaya Tenega)                            |
| Malaysia    | Sarawak Energy’s Sustainability Report                        | Contains statistics and maps of the transmission lines                                              |
| Malaysia    | Energy Statistics Handbook                                   | Energy statistics by the Energy Commission                                                            |
| Malaysia    | Electricity & Gas Supply Infrastructure Malaysia              | Infrastructure map                                                                                  |
| Malaysia    | Sabah Electricity Supply Industry Outlook 2019                | Statistics and map of Sabah                                                                          |
| Indonesia   | Electricity Supply Business Plan PT Perusahaan Listrik Negara  | PT PLN is the state-owned electric utility. The business plan contains thorough statistics and maps |
| Philippines | Transmission Development Plan 2022                           | Provides information on the existing transmission system and planned investments                    |

Once the data sources have been collected, it should be organized and structured into three CSV files: one for generation data, one for transmission data, and one for substation data. These data are later processed as inputs for modeling in PowNet. The next section of this page describes specific steps and key data fields to be collected for generation, transmission, and substation.

### Data on generation
#### Sources for generation data
Several international organizations and online communities have curated datasets of global power plants, both at the power plant and generator levels. These resources include
- [Global Database of Power Plants (up to 2021)](https://github.com/wri/global-power-plant-database)
- [Global Coal Plant Tracker](https://globalenergymonitor.org/projects/global-coal-plant-tracker/?gad_source=1&gclid=CjwKCAjwufq2BhAmEiwAnZqw8iR82nUkdQgFugta4_MC17IxS4xqy5bOFX9k9d5nKJH_4-k3oFMBzhoCIf0QAvD_BwE)
- [Hydropower along Mekong](https://www.mrcmekong.org/hydropower/)
- [OpenStreetMap](https://openinframap.org/#8.78/15.8523/100.8503)

#### Key data fields
We can begin to populate a spreadsheet with datasets from the previous step. Data fields of interest include
- **name**: name of the unit. For generators at the same site, use numbers as suffixes for naming
- **latitude**
- **longitude**
- **year**: commercial date of operation (COD)
- unit_type: simple cycle, combined cycle, etc.
- **fuel_type**
- **max_capacity**
- min_capacity
- heat_rate
- operation_cost
- fuel_cost
- fixed_cost
- startup_cost
- ramp_rate
- min_uptime
- min_downtime
- owner (optional)

Note that bolded fields are the required fields at this stage. The most important fields are name and max_capacity. If a data source contains addresses of power plants, then we can use an add-on in Google Sheets to recover the geo-coordinates.

Detailed technical parameters can be inferred from the [Viet Nam Technology Catalogue for power generation and storage](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/2021-VN_tech_catalogue.pdf), as units in the region are likely to share similar technical specifications. These techno-economic parameters are essential for modeling system operations.

#### Reconciling data with official statistics
Once the generation data has been collected, the dataset should be reconciled with official statistics due to several reasons. For example, the maximum capacity of a unit might differ between sources because some may use nameplate capacity while others use contracted capacity. In such cases, the official reports will act as the reference, therefore, any mismatch should be reconciled accordingly. This can be done by breaking down the installed capacity by fuel type for each year and comparing it with the numbers from the official reports. Reviewing the installed capacity makes it easier to spot the differences. 

Common causes of mismatch in numbers include 
- Retired units leading to missing capacity
- Incorrect COD leading to extra capacity
- Expanded/Derated capacity leading to mismatch in installed capacity

An example of a spreadsheet for reconciling the data can be seen [here](https://github.com/Critical-Infrastructure-Systems-Lab/manual/blob/master/assets/img/docs/MY_powerplants_2016.xlsx). Small mismatches between the collected data and the official reports are expected. Numbers might not even align perfectly among official reports from the same department and year.

### Data on high-voltage transmission lines and Substations
Sources for transmission data
Obtaining detailed information about the technical specifications and locations of high-voltage transmission lines is the most challenging step in data collection because countries do not widely share this data. Therefore, data collection requires piecing together from less detailed official maps or incomplete open-source databases. For instance, Thailand’s Power Development Plan 2015 provides a map of the transmission system, but the map is absent in the subsequent 2018 version.

#### Key data fields
Fields needed for modeling in PowNet include
- name
- source_latitude: (should be from shapefile)
- sink_longitude: (should be from shapefile)
- source_latitude: (should be from shapefile)
- sink_longitude: (should be from shapefile)
- source_kv: (should be from shapefile)
- sink_kv: (should be from shapefile)
- number of circuits (inferred from the map)
- max_capacity (optional)
- conductor_type (optional)
- reactance (optional): modeling uses the reactance parameter
- year

Generally, information on substations (name, location, and rating) is provided along with the transmission lines. Specifically, we are interested in collecting the following fields:
- name
- latitude
- longitude
- kv: Kilo-Volt
- rating (optional): in MVA
- year

#### Digitizing the transmission system
More than likely, the address or geo-coordinates of transmission lines and substations are not available from official sources. Therefore, when a map of the transmission system is available, GIS software can digitize the map into shapefiles, which can be used for visualization. This involves overlaying the map onto geo-coordinates and manually drawing lines that align with the transmission lines on the map. A tutorial on georeferencing a map in QGIS is provided [here](https://www.youtube.com/watch?v=p_ieBLVEMq8). Note that when drawing substations, they should be connected to the transmission lines.

### Data on electricity demand
The ideal scenario is to collect a timeseries of hourly electricity demand at each substation. However, this level of granularity is typically classified and not readily available.

When such detailed data is unavailable, it is recommended to collect demand data at the highest possible spatial and temporal detail. There are algorithms available to process coarser data into a finer resolution. Generally, demand data is published in power development plans or reports of annual energy statistics. The daily load profile for the whole country is generally available online.

In terms of the temporal dimension, the following information is useful to collect:
- Peak daily demand
- Peak weekly demand
- Information on the temporal variability of demand over a period T equal to 24 hours, 7 days, and 12 months
The listed data helps in devising the daily, weekly, and annual profiles of demand variability. Temporal decomposition algorithms can then create hourly timeseries from this information.


### Other notes on data collection
- Keep an eye out for data on domestic energy prices
- When collecting data for a new country, it is good practice to understand the business structure (single-buyer or liberalized market) and begin searching through information provided by major electric utilities of that country
