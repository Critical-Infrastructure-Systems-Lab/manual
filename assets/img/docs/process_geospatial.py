"""This script processes GIS data for PowNet"""

import os
import pandas as pd
import geopandas as gpd

from geospatial_utils import (
    process_buses,
    process_lines,
    create_bus_df,
    cluster_buses,
    split_overpassing_lines,
    extend_line_to_bus,
    filter_isolated_buses,
    get_lines_to_isolated_buses,
    connect_subgraphs,
)


def save_geodataframes_to_geojson(
    gdfs: list[tuple[gpd.GeoDataFrame, str]], output_folder: str
) -> None:
    """Saves a list of GeoDataFrames to GeoJSON files in a specified folder.

    Args:
        gdfs (list[tuple[gpd.GeoDataFrame, str]]): A list of tuples, where each tuple
                                                  contains a GeoDataFrame and its
                                                  corresponding filename (without extension).
        output_folder (str): The path to the folder where the files will be saved.
    """
    for gdf, filename in gdfs:
        gdf.to_file(
            os.path.join(output_folder, f"{filename}.geojson"), driver="GeoJSON"
        )


def main():

    ########################################################
    # User defined parameters
    ########################################################

    voltage_threshold = 115  # Minimum voltage threshold for lines and buses
    bus_cluster_distance = 500  # Distance threshold for clustering buses
    overpass_distance = 300  # Distance threshold for overpassing lines
    isolated_bus_distance = 1000  # Distance threshold for isolated buses
    max_subgraph_iter = 50  # Number of iterations to connect disconnected subgraphs

    country = "THA"  # Country code

    ########################################################
    # Load and process data
    ########################################################
    file_name = os.path.join(country, f"{country}.gpkg")
    lines = gpd.read_file(file_name, layer="power_line")[
        ["name", "max_voltage", "circuits", "cables", "geometry"]
    ]
    buses = gpd.read_file(file_name, layer="power_substation_polygon")[
        ["name", "max_voltage", "geometry"]
    ]

    # ########################################################
    # # Special case with Laos
    # ########################################################
    # lines = gpd.read_file(f"{country}/laos_grid/LaoGridLines.shp")
    # cols_2_drop = [
    #     "Line",
    #     "Length",
    #     "source",
    #     "sink",
    #     "linesus",
    #     "linemva",
    #     "cct",
    #     "km",
    #     "mm2",
    #     "cond",
    # ]
    # lines = lines.drop(cols_2_drop, axis=1)
    # lines = lines.rename(columns={"kV": "max_voltage", "Id": "name"})
    # cols_2_add = ["circuits", "cables"]
    # # Add NaN values for circuits and cables
    # lines[cols_2_add] = None

    # buses = gpd.read_file(f"{country}/laos_grid/LaoSubstations.shp")
    # cols_2_drop = ["Id", "PeakD_MW", "GWh"]
    # buses = buses.drop(cols_2_drop, axis=1)
    # buses = buses.rename(columns={"substation": "name", "kV": "max_voltage"})
    # # if the max_voltage has the following values "230/115/22", then we take the highest value
    # buses["max_voltage"] = buses["max_voltage"].apply(
    #     lambda x: max(map(int, x.split("/")))
    # )

    # # Convert kV to V for the script
    # buses["max_voltage"] = buses["max_voltage"] * 1000
    # lines["max_voltage"] = lines["max_voltage"] * 1000

    ########################################################

    # Process data
    buses = process_buses(buses, voltage_threshold=voltage_threshold)
    lines = process_lines(lines, voltage_threshold=voltage_threshold)
    line_buses = pd.concat(
        [create_bus_df(row, crs=lines.crs) for _, row in lines.iterrows()],
        axis=0,
    )
    buses = pd.concat([buses, line_buses], axis=0, ignore_index=True)
    clustered_buses = cluster_buses(buses, cluster_distance=bus_cluster_distance)
    lines = split_overpassing_lines(
        lines, clustered_buses, filter_distance=overpass_distance
    )
    lines = extend_line_to_bus(lines, clustered_buses)

    # Get isolated_buses and lines to connect them to the network
    isolated_buses, buses_to_connect = filter_isolated_buses(
        lines, clustered_buses, isolated_bus_distance=isolated_bus_distance
    )

    fake_line_gdf = get_lines_to_isolated_buses(isolated_buses, buses_to_connect, lines)

    # Update lines and clustered_buses
    lines = pd.concat([lines, fake_line_gdf], axis=0, ignore_index=True)

    # Connect disconnected subgraphs
    subgraph_lines = []
    for c_idx in range(max_subgraph_iter):
        connected_subgraph_lines = connect_subgraphs(lines, clustered_buses, c_idx)
        if not connected_subgraph_lines:
            break
        subgraph_lines.extend(connected_subgraph_lines)
        connected_subgraph_lines = gpd.GeoDataFrame(
            connected_subgraph_lines,
            geometry="geometry",
            crs=lines.crs,
        )
        lines = pd.concat([lines, connected_subgraph_lines], axis=0, ignore_index=True)
        if c_idx == max_subgraph_iter:
            raise ValueError("Reached maximum number of iterations.")

    subgraph_lines = gpd.GeoDataFrame(
        subgraph_lines, geometry="geometry", crs=lines.crs
    )

    # Drop isolated buses that are not overpassing lines
    # but also not within the isolated_bus_distance
    unconnected_buses = clustered_buses[
        ~clustered_buses["id"].isin(
            lines["source_bus"].tolist() + lines["sink_bus"].tolist()
        )
    ]
    clustered_buses = clustered_buses[
        ~clustered_buses["id"].isin(unconnected_buses["id"].tolist())
    ]

    # PowNet needs distance column or the length of the line in km
    lines["distance"] = lines["geometry"].to_crs(epsg=3857).length / 1000

    ########################################################
    # Checks and save outputs
    ########################################################
    print("Checking processed geospatial data...")
    print(
        f"No. disconnected buses (not overpassing but not isolated enough): {len(unconnected_buses)}"
    )
    # Lines that share the same source/sink
    lines_with_same_source_sink = lines[lines["source_bus"] == lines["sink_bus"]]
    print(
        f"No. lines with the same source and sink: {len(lines_with_same_source_sink)}"
    )

    # Save outputs
    output_folder = os.path.join(country, "clean_geojson")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # original_lines = gpd.read_file(file_name, layer="power_line")[
    #     ["name", "max_voltage", "circuits", "cables", "geometry"]
    # ]
    # original_buses = gpd.read_file(file_name, layer="power_substation_polygon")[
    #     ["name", "max_voltage", "geometry"]
    # ]

    gdfs_to_save = [
        # (original_buses, "original_buses"),
        # (original_lines, "original_lines"),
        (clustered_buses, f"{country}_final_buses"),
        (lines, f"{country}_final_lines"),
        (isolated_buses, f"{country}_isolated_buses"),
        (unconnected_buses, f"{country}_unconnected_buses"),
        (subgraph_lines, f"{country}_subgraph_lines"),
    ]
    save_geodataframes_to_geojson(gdfs_to_save, output_folder)


if __name__ == "__main__":
    main()
