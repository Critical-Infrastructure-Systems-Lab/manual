import os
import concurrent.futures

import geopandas as gpd
import pandas as pd
import cdsapi
from datetime import datetime as dt


def get_bbox(
    df: pd.DataFrame, buffer_size: float = 0.5
) -> tuple[float, float, float, float]:
    """Get the bounding box for a set of coordinates

    Args:
        df (pd.DataFrame): DataFrame with columns 'latitude' and 'longitude'
        buffer_size (float, optional): Buffer size (degrees) around the bounding box. Defaults to 0.5 degrees

    Returns:
        tuple[float, float, float, float]: Bounding box coordinates, ordering as max_y, min_x, min_y, max_x
    """
    geo_df = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    )
    bbox = geo_df.union_all().buffer(buffer_size).bounds
    min_x, min_y, max_x, max_y = bbox  # This is the order by geopandas
    # Reorder the bounding box coordinates as required by the CDS API
    bbox = [max_y, min_x, min_y, max_x]
    return bbox


def get_variables(target_renewable: str) -> dict[str, str]:
    """Return ERA5 variables for the target renewable energy source

    Args:
        target_renewable (str): Target renewable energy source which can be 'wind' or 'solar'

    Returns:
        dict[str, str]: Dictionary of ERA5 variables for the target renewable energy source
    """

    if target_renewable == "wind":
        return {
            "100m_u_component_of_wind": "100uwind",
            "100m_v_component_of_wind": "100vwind",
            "10m_u_component_of_wind": "10uwind",
            "10m_v_component_of_wind": "10vwind",
            "forecast_surface_roughness": "roughness_length",
            "surface_pressure": "pressure",
            "2m_temperature": "2m_temperature",
        }
    elif target_renewable == "solar":
        return {
            "mean_surface_direct_short_wave_radiation_flux": "direct_shortwave",
            "mean_surface_downward_short_wave_radiation_flux": "global_horizontal",
            "2m_temperature": "2m_temperature",
        }
    else:
        raise ValueError(
            f"Target_renewable should be 'wind' or 'solar'. Unsupported type: {target_renewable}"
        )


def download_data(
    era5_variable: str,
    month: str,
    year: str,
    bbox: tuple[float, float, float, float],
    output_folder: str,
) -> None:
    """Write ERA5 data for a single variable and month as a netCDF file.

    Args:
        variable (str): ERA5 variable to download
        month (str): Month to download, e.g. '01'
        year (str): Year to download, e.g. '2019'
        bbox (tuple[float, float, float, float]): Bounding box coordinates, ordering as max_y, min_x, min_y, max_x
        output_folder (str): Path to save the downloaded file

    """
    if type(month) == int:
        raise ValueError("Month should be a string, e.g. '01'")

    if os.path.exists(output_folder):
        print(f"File already exists: {output_folder}. Skipping download.")
        return

    current_time = dt.now()
    print(
        f"\Start downloading {era5_variable} for {month} at ",
        current_time.strftime("%H:%M:%S"),
    )

    request = {
        "product_type": ["reanalysis"],
        "variable": [era5_variable],
        "year": [year],
        "month": [month],
        "day": [str(i).zfill(2) for i in range(1, 32)],
        "time": [f"{i:02}:00" for i in range(24)],
        "data_format": "netcdf",
        "area": bbox,  # North, West, South, East
    }

    client = cdsapi.Client()
    dataset = "reanalysis-era5-single-levels"
    client.retrieve(dataset, request, output_folder)

    total_mins = round((dt.now() - current_time).seconds / 60, 2)
    print(f"Completed downloading {era5_variable} for {month} in {total_mins} mins")


def get_era5(
    era5_variables: dict[str, str],
    year: str,
    bbox: list[float],
    download_folder: str,
    parallel: bool = True,
) -> None:
    """Download ERA5 data for the specified variables, year, and bounding box

    Args:
        era5_variables (dict[str, str]): Dictionary of ERA5 variables for the target renewable energy source
        year (str): Year to download, e.g. '2019'
        bbox (list[float]): Bounding box coordinates, ordering as max_y, min_x, min_y, max_x
        download_folder (str): Path to save the downloaded files
        parallel (bool, optional): Download data in parallel. Defaults to True

    """
    # Identify months to download -- including month -1 and month +1
    months = [str(i).zfill(2) for i in range(1, 13)]

    # Input arguments for month -1 and month +1
    month_00_args = [
        (
            variable,
            "12",  # December of the previous year
            str(int(year) - 1),
            bbox,
            f"{download_folder}/{era5_variables[variable]}_00.nc",
        )
        for variable in era5_variables
    ]
    month_13_args = [
        (
            variable,
            "01",  # January of the next year
            str(int(year) + 1),
            bbox,
            f"{download_folder}/{era5_variables[variable]}_13.nc",
        )
        for variable in era5_variables
    ]
    boundary_months = month_00_args + month_13_args

    # Download data in parallel
    if parallel:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Package the arguments for the parallel download
            args = [
                (
                    variable,
                    month,
                    year,
                    bbox,
                    f"{download_folder}/{era5_variables[variable]}_{month}.nc",
                )
                for variable in era5_variables
                for month in months
            ]
            args.extend(boundary_months)
            executor.map(download_data, *zip(*args))

    # Download data sequentially
    else:
        for variable in era5_variables:
            for month in months:
                download_data(
                    variable,
                    month,
                    year,
                    bbox,
                    f"{download_folder}/{era5_variables[variable]}_{month}.nc",
                )
        # Month -1 and month +1 for each variable
        for args in boundary_months:
            download_data(*args)

    print("All downloads completed.")


if __name__ == "__main__":
    # Load the data
    renewable_type = "solar"  # Either 'wind' or 'solar'
    year = "2023"

    location_df = pd.read_csv("nondispatch_spp.csv")

    bbox = get_bbox(location_df[location_df["spp_fuel"] == renewable_type])

    download_folder = f"./{renewable_type}_data"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Parameters to download from ERA5 for the renewable type
    era5_variables = get_variables(renewable_type)

    get_era5(era5_variables, year, bbox, download_folder)
