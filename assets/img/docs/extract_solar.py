""" Creates solar.csv.

Note:

- Total radiation is the mean surface downward short-wave radiation flux.
- Direct radiation is the mean surface direct short-wave radiation flux.

We can calculate the diffuse fraction as follows:

- Diffuse radiation = Total radiation - Direct radiation
- Diffuse fraction = Diffuse radiation / Total radiation 

"""

import xarray as xr
import pandas as pd
import geopandas as gpd
import gsee
from nearest_point import assign_nearest_substation


def load_era5_timeseries(
    filename: str, varname: str, latitude: float, longitude: float
) -> pd.DataFrame:
    """Load the ERA5 timeseries data from a NetCDF file and return a DataFrame
    with the variable name as the column name."""
    dataset = xr.open_dataset(filename)
    dataset = dataset.sel(longitude=longitude, latitude=latitude, method="nearest")
    return dataset.to_dataframe()[varname]


def create_weather_data(
    descriptive_to_era5: dict[str, str],
    latitude: float,
    longitude: float,
    data_folder: str,
    timezone: str = "Asia/Bangkok",
) -> pd.DataFrame:
    """Create weather data for capacity calculation"""
    # 14 months with two extra months: Dec (indexed as 00) of the previous year
    # and Jan (indexed as 13) of the next year
    months = [f"{i:02d}" for i in range(0, 14)]

    output = pd.DataFrame()
    for key, value in descriptive_to_era5.items():
        series = pd.DataFrame()
        for month in months:
            filename = f"{data_folder}/{key}_{month}.nc"
            dataset = load_era5_timeseries(
                filename, value, latitude=latitude, longitude=longitude
            )
            # Append to the series
            if series.empty:
                series = dataset
            else:
                series = pd.concat([series, dataset], axis=0)

        if output.empty:
            output = series
        else:
            output = pd.concat([output, series], axis=1)

    # Convert index to datetime
    output.index = pd.to_datetime(output.index, utc=True)
    # Convert to Thailand time
    output.index = output.index.tz_convert(timezone)
    return output


def create_solar(solar_df, data_folder):
    # Map the variable names
    descriptive_to_era5 = {
        "global_horizontal": "msdwswrf",  # W/m^2
        "direct_shortwave": "msdrswrf",  # W/m^2
        "2m_temperature": "t2m",  # K
    }
    # Column names as requred by GSEE
    weather_columns = {
        "msdwswrf": "global_horizontal",
        "msdrswrf": "direct_shortwave",
        "t2m": "temperature",
    }

    # Create the solar capacity dataframe
    solar_capacity = pd.DataFrame()
    for _, row in solar_df.iterrows():
        #########################
        # Create the weather data
        #########################
        latitude = row["latitude"]
        longitude = row["longitude"]

        weather_data = create_weather_data(
            descriptive_to_era5,
            latitude=latitude,
            longitude=longitude,
            data_folder=data_folder,
        ).rename(columns=weather_columns)
        # The GSEE package expects the temperature in Celsius
        weather_data["temperature"] = weather_data["temperature"] - 273.15
        # Calculate the diffuse fraction
        weather_data["diffuse"] = (
            weather_data["global_horizontal"] - weather_data["direct_shortwave"]
        )
        weather_data["diffuse_fraction"] = weather_data["diffuse"] / (
            weather_data["global_horizontal"] + 0.0001
        )

        #########################
        # Calculate the solar capacity
        #########################
        name = row["name"]
        max_capacity = row["max_capacity"]

        # The gsee.pv.run_model function expects the following columns:
        # - temperature: Temperature in Celsius
        # - global_horizontal: Total radiation in W/m^2
        # - diffuse_fraction: Diffuse fraction
        solar_factor = gsee.pv.run_model(
            data=weather_data,
            coords=(latitude, longitude),
            tilt=35,
            azim=180,
            tracking=0,  # No tracking
            capacity=1,  # Use 1 W so we can scale it later
        )
        # Solar capacity is the max_capacity of the solar farm multiplied by the solar factor
        site_capacity = solar_factor * max_capacity
        # Round to 4 decimal places
        site_capacity = site_capacity.round(4)
        site_capacity.name = name

        # Append to the solar_capacity dataframe
        if site_capacity.empty:
            solar_capacity = site_capacity
        else:
            solar_capacity = pd.concat([solar_capacity, site_capacity], axis=1)
    # Save as solar.csv
    return solar_capacity


if __name__ == "__main__":
    # Load
    spp_renew = pd.read_csv("nondispatch_spp.csv")
    solar_df = spp_renew[spp_renew["spp_fuel"] == "solar"]
    data_folder = "./solar_data"
    solar_capacity = create_solar(solar_df, data_folder)

    # Assign the solar units to the nearest substation
    substations = gpd.read_file("../clean_buses.geojson")
    distance, nearest_bus_map = assign_nearest_substation(
        source_df=solar_df,
        substations=substations,
        source_name_col="name",
        substation_geo_col="geometry",
    )
    col_idx = pd.MultiIndex.from_tuples(
        [(col, nearest_bus_map[col]) for col in solar_capacity.columns]
    )
    solar_capacity.columns = col_idx

    solar_capacity.index = pd.to_datetime(solar_capacity.index)
    solar_capacity = solar_capacity.loc[solar_capacity.index.year == 2023]
    solar_capacity.to_csv("./clean_data/solar.csv", index=False)
    print("solar.csv saved.")
