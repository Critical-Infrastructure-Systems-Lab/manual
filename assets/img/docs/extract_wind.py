""" Create wind.csv.

Note:
- Assume GE100/2500 wind turbine (General Electric)
- Assume hub height is 100m.
- Assume no temperature changes at 2m and 10m.
- The data include wind speed at two different heights in m/s, air temperature
in two different heights in K, surface roughness length in m
and air pressure in Pa.

"""

import geopandas as gpd
import pandas as pd
import windpowerlib
from extract_solar import create_weather_data
from nearest_point import assign_nearest_substation

spp_renew = pd.read_csv("nondispatch_spp.csv")
wind_df = spp_renew[spp_renew["spp_fuel"] == "wind"]
data_folder = "./wind_data"


def create_wind(wind_df: pd.DataFrame, data_folder: str) -> pd.DataFrame:
    # The units are aligned with the windpowerlib
    descriptive_to_era5 = {
        "100uwind": "u100",  # m/s
        "100vwind": "v100",  # m/s
        "10uwind": "u10",  # m/s
        "10vwind": "v10",  # m/s
        "roughness_length": "fsr",  # m
        "pressure": "sp",  # Pa
        "2m_temperature": "t2m",  # K
    }
    weather_columns = {
        "u100": "100uwind",
        "v100": "100vwind",
        "u10": "10uwind",
        "v10": "10vwind",
        "fsr": "roughness_length",
        "sp": "pressure",
        "t2m": "temperature",
    }
    # Columns need height as the second-level index
    heights = {
        "10m_speed": 10,
        "100m_speed": 100,
        "temperature": 2,
        "roughness_length": 0,
        "pressure": 0,
    }
    # Define turbine
    ge_turbine = {
        "turbine_type": "GE100/2500",
        "hub_height": 100,  # meters
    }
    ge_turbine = windpowerlib.WindTurbine(**ge_turbine)

    wind_capacity = pd.DataFrame()
    for _, row in wind_df.iterrows():
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

        # Calculate wind speed from u and v components
        weather_data["10m_speed"] = (
            weather_data["10uwind"] ** 2 + weather_data["10vwind"] ** 2
        ) ** 0.5
        weather_data["100m_speed"] = (
            weather_data["100uwind"] ** 2 + weather_data["100vwind"] ** 2
        ) ** 0.5
        # Drop the u and v components
        weather_data = weather_data.drop(
            columns=["10uwind", "10vwind", "100uwind", "100vwind"]
        )

        # windpowerlib requires height as the second-level index
        weather_data.columns = pd.MultiIndex.from_tuples(
            [(col, heights[col]) for col in weather_data.columns],
            names=["variable_name", "height"],
        )

        # Rename columns to those required by the windpowerlib
        weather_data = weather_data.rename(
            columns={
                "10m_speed": "wind_speed",
                "100m_speed": "wind_speed",
                "2m_temperature": "temperature",
                "roughness_length": "roughness_length",
                "pressure": "pressure",
            }
        )

        #########################
        # Calculate wind capacity using default parameters of ModelChain
        #########################
        name = row["name"]
        max_capacity = row["max_capacity"]

        model_chain = windpowerlib.ModelChain(ge_turbine).run_model(weather_data)
        # Power output in W, so convert to MW. The rated capacity is 2.5 MW
        power_output = model_chain.power_output / 1e6
        # Normalize the power output to get a factor that can be multiplied by the
        # site's capacity to get the actual power output
        power_factor = power_output / 2.5
        site_capacity = power_factor * max_capacity
        # Round to 4 decimal places
        site_capacity = site_capacity.round(4)
        site_capacity.name = name

        if wind_capacity.empty:
            wind_capacity = site_capacity
        else:
            wind_capacity = pd.concat([wind_capacity, site_capacity], axis=1)
    return wind_capacity


if __name__ == "__main__":
    spp_renew = pd.read_csv("nondispatch_spp.csv")
    wind_df = spp_renew[spp_renew["spp_fuel"] == "wind"]
    data_folder = "./wind_data"
    wind_capacity = create_wind(wind_df, data_folder)

    # Assign units to the nearest substation
    substations = gpd.read_file("../clean_buses.geojson")
    distance, nearest_bus_map = assign_nearest_substation(
        source_df=wind_df,
        substations=substations,
        source_name_col="name",
        substation_geo_col="geometry",
    )
    col_idx = pd.MultiIndex.from_tuples(
        [(col, nearest_bus_map[col]) for col in wind_capacity.columns]
    )
    wind_capacity.columns = col_idx
    wind_capacity.index = pd.to_datetime(wind_capacity.index)
    wind_capacity = wind_capacity.loc[wind_capacity.index.year == 2023]
    wind_capacity.to_csv("./clean_data/wind.csv", index=False)
    print("Wind capacity data saved.")
