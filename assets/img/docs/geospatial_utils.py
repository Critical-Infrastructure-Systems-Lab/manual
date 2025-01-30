""" This module contains utility functions for processing geospatial data (transmission lines and substations).
"""

import geopandas as gpd
from networkx import Graph, connected_components
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point
from shapely.ops import split
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN

EPSG_CRS = 3857  # Web Mercator


def get_source_sink(linestring: LineString) -> tuple:
    """
    Extracts the source and sink coordinates of a LineString geometry.

    Args:
      line: A shapely LineString geometry

    Returns:
      A tuple containing the source and sink coordinates as shapely Points.
    """
    return linestring.boundary.geoms[0], linestring.boundary.geoms[1]


def ckdnearest(
    gdf_A: gpd.GeoDataFrame, gdf_B: gpd.GeoDataFrame, loc_col_A: str, loc_col_B: str
) -> tuple[pd.Series, pd.Series]:
    """Finds the nearest point in `gdf_B` for each point in `gdf_A` using a cKDTree.

    This function efficiently computes the nearest neighbor between two GeoDataFrames
    using a cKDTree for optimized spatial searching.

    Source: https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas

    Args:
        gdf_A (gpd.GeoDataFrame): The GeoDataFrame containing the points to find nearest neighbors for.
        gdf_B (gpd.GeoDataFrame): The GeoDataFrame containing the potential nearest neighbors.
        loc_col_A (str): The name of the geometry column in `gdf_A`.
        loc_col_B (str): The name of the geometry column in `gdf_B`.

    Returns:
        tuple[pd.Series, pd.Series]: A tuple containing:
            - A Series with the distances to the nearest neighbors.
            - A Series with the 'id' column of the nearest points from `gdf_B`.

    Example:
        >>> distances, nearest_points = ckdnearest(gdf_points, gdf_stations, 'geometry', 'geometry')
        >>> print(distances.head())
        >>> print(nearest_points.head())
    """

    array_A = np.array(list(gdf_A[loc_col_A].apply(lambda x: (x.x, x.y))))
    array_B = np.array(list(gdf_B[loc_col_B].apply(lambda x: (x.x, x.y))))
    btree = cKDTree(array_B)
    dist, idx = btree.query(array_A, k=1)
    gdf_B_nearest = gdf_B.id.iloc[idx].drop(columns=loc_col_B).reset_index(drop=True)
    dist = pd.Series(dist, name="dist")
    return dist, gdf_B_nearest


def assign_cluster(buses: gpd.GeoDataFrame, distance: float) -> np.ndarray:
    """
    Assigns clusters to substations using DBSCAN.

    Args:
      buses: A GeoDataFrame of substations.
      distance: The maximum distance (in the same units as the geometries)
                between two substations for them to be considered in the same cluster.

    Returns:
      A NumPy array containing the cluster labels assigned by DBSCAN.
    """

    # Project the points to a suitable coordinate system for distance calculations (e.g., UTM)
    buses_proj = buses.to_crs(epsg=EPSG_CRS)  # Example: UTM Zone 18N

    # Extract coordinates for DBSCAN
    coords = buses_proj["geometry"].apply(lambda geom: (geom.x, geom.y)).tolist()

    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=distance, min_samples=2)  # eps is the distance parameter
    clusters = dbscan.fit_predict(coords)
    return clusters


def extend_line(
    line: LineString,
    source_point: tuple[float, float],
    sink_point: tuple[float, float],
) -> LineString:
    """Extends a LineString to include the source and sink points.

    This function modifies a LineString geometry by adding the `source_point`
    at the beginning and the `sink_point` at the end, ensuring the line
    spans between these points.

    Args:
        line (LineString): A shapely LineString geometry.
        source_point (tuple[float, float]): A tuple representing the (x, y) coordinates of the source point.
        sink_point (tuple[float, float]): A tuple representing the (x, y) coordinates of the sink point.

    Returns:
        LineString: The extended LineString geometry.

    Example:
        >>> line = LineString([(1, 1), (2, 2)])
        >>> source = (0, 0)
        >>> sink = (3, 3)
        >>> extended_line = extend_line(line, source, sink)
        >>> print(extended_line)  # Output: LINESTRING (0 0, 1 1, 2 2, 3 3)
    """
    # Append if the source and sink points are not already in the line
    new_coords = list(line.coords)
    if line.coords[0] != source_point:
        new_coords.insert(0, source_point)
    if line.coords[-1] != sink_point:
        new_coords.append(sink_point)
    return LineString(new_coords)


def keep_distant_points(points, lines, distance):
    """
    Keep points that are further than a specified distance from any line.

    Args:
      points: A GeoDataFrame of points.
      lines: A GeoDataFrame of lines.
      distance: The minimum distance (in the same units as the geometries)
                a point must be from any line to be retained.

    Returns:
      A GeoDataFrame of points that are further than the specified distance
      from any line.
    """

    # Project to a suitable coordinate system for distance calculations
    points_proj = points.to_crs(epsg=EPSG_CRS)
    lines_proj = lines.to_crs(epsg=EPSG_CRS)

    # Create a buffer around the lines
    lines_buffer = lines_proj.buffer(distance)

    # Find points that do not intersect the buffer
    distant_points = points_proj[~points_proj.intersects(lines_buffer.unary_union)]

    # Return the distant points in the original coordinate system
    return distant_points.to_crs(points.crs)


def _split_line_at_point(
    line: LineString, point: Point
) -> tuple[LineString, LineString]:
    # Create a short line segment that intersects the original line for more
    # robust splitting because our linestring can be complex
    splitting_line1 = LineString(
        [
            (point.x - 1e-2, point.y),  # Point slightly to the left
            (point.x + 1e-2, point.y),  # Point slightly to the right
        ]
    )
    # If splitting_line overlaps with the line, then use the y-axis instead
    splitting_line2 = LineString(
        [
            (point.x, point.y - 1e-2),  # Point slightly below
            (point.x, point.y + 1e-2),  # Point slightly above
        ]
    )

    try:
        split_line = split(line, splitting_line1)
    except ValueError as e:
        if "Input geometry segment overlaps with the splitter" not in str(e):
            raise e
        split_line = split(line, splitting_line2)

    if len(split_line.geoms) == 1:
        return None
    return split_line.geoms[0], split_line.geoms[1]


def split_overpassing_lines(
    lines: gpd.GeoDataFrame, buses: gpd.GeoDataFrame, filter_distance: int
):
    """Splits power lines that overpass substations within a specified distance.

    This function iterates through power lines and splits them at the points where they
    overpass substations. It considers a `filter_distance` to account for cases where
    substations may not be exactly on the lines. The splitting is performed sequentially
    along each line, ensuring that the resulting segments maintain the original line's
    attributes.

    Args:
        lines (gpd.GeoDataFrame): A GeoDataFrame of power lines, with a 'geometry' column
                                  containing LineString geometries.
        buses (gpd.GeoDataFrame): A GeoDataFrame of substations, with a 'geometry' column
                                 containing Point geometries.
        filter_distance (int): The maximum distance (in meters) between a line and a
                               substation for the line to be considered "overpassing".

    Returns:
        gpd.GeoDataFrame: A new GeoDataFrame containing the split power lines. Each
                          split segment retains the original line's attributes (like
                          'name', 'max_voltage', etc.) and has a modified 'name'
                          to indicate the split sequence (e.g., "line123-split-0").

    Notes:
        - The function assumes that the input GeoDataFrames have a 'geometry' column.
        - The function reprojects the geometries to UTM (EPSG:32618) for accurate
          distance calculations and then converts them back to the original CRS.
    """
    split_lines = []

    # Convert crs to UTM for distance calculations
    line_crs = lines.crs
    lines_copy = lines.copy().to_crs(epsg=EPSG_CRS)
    buses_copy = buses.copy().to_crs(epsg=EPSG_CRS)

    # Iterate over the lines
    for _, line in lines_copy.iterrows():
        # Extract line spec to copy to the split lines
        name = line.name
        max_voltage = line.max_voltage
        circuits = line.circuits
        cables = line.cables
        line_id = line.id

        # Get the closest substations within the filter distance
        closest_buses = buses_copy.loc[
            buses_copy.geometry.distance(line.geometry) <= filter_distance
        ].copy()

        # If no substations are within the filter distance, keep the original line
        if closest_buses.empty:
            split_lines.append(
                {
                    "name": name,
                    "max_voltage": max_voltage,
                    "circuits": circuits,
                    "cables": cables,
                    "id": line_id,
                    "geometry": line.geometry,
                }
            )
            continue

        # Reorder the substations based on the distance from the start of the line
        closest_buses["distance"] = closest_buses.geometry.apply(
            lambda x: line.geometry.project(x)
        )
        closest_buses = closest_buses.sort_values("distance")

        # For each substation in the list, keep splitting the linestring
        current_segment = line.geometry
        number_split = 0
        for _, bus_row in closest_buses.iterrows():
            # Split the line at the projected point
            point_to_split = current_segment.interpolate(
                current_segment.project(bus_row.geometry)
            )

            # Skip if the point is at the start or end of the line
            if point_to_split.equals_exact(
                current_segment.boundary.geoms[0], tolerance=1e-6
            ) or point_to_split.equals_exact(
                current_segment.boundary.geoms[1], tolerance=1e-6
            ):
                continue
            split_line = _split_line_at_point(current_segment, point_to_split)

            # Otherwise, the line is splitted into two line segments
            line_a, current_segment = split_line

            split_lines.append(
                {
                    "name": f"{line_id}-split-{number_split}",
                    "max_voltage": max_voltage,
                    "circuits": circuits,
                    "cables": cables,
                    "id": line_id,
                    "geometry": line_a,
                }
            )
            number_split += 1
        # Append the last segment of the line
        split_lines.append(
            {
                "name": f"{line_id}-split-{number_split}",
                "max_voltage": max_voltage,
                "circuits": circuits,
                "cables": cables,
                "id": line_id,
                "geometry": current_segment,
            }
        )
    output = gpd.GeoDataFrame(split_lines, crs=lines_copy.crs).to_crs(line_crs)
    # Recover all the original columns -- including source and sink
    output["source"] = output.geometry.apply(lambda x: get_source_sink(x)[0])
    output["sink"] = output.geometry.apply(lambda x: get_source_sink(x)[1])
    return output


def create_bus_df(row: pd.Series, crs: str) -> gpd.GeoDataFrame:
    """Creates a GeoDataFrame for a bus (source or sink) from a line row.

    Args:
        row: A row from a GeoDataFrame of transmission lines.
        crs: The coordinate reference system for the GeoDataFrame.

    Returns:
        A GeoDataFrame with the bus location, max voltage, and geometry.
    """
    points = get_source_sink(row["geometry"])
    return gpd.GeoDataFrame(
        {
            "name": [f"bus{row['id']}{point_type}" for point_type in ["a", "b"]],
            "geometry": points,
            "max_voltage": [row["max_voltage"]] * 2,
        },
        geometry="geometry",
        crs=crs,
    )


def process_lines(lines: gpd.GeoDataFrame, voltage_threshold: int) -> gpd.GeoDataFrame:
    """Processes transmission line data by
    1. Converting max voltage to kV
    2. Filtering lines below the voltage threshold
    3. Assigning unique IDs to lines
    4. Extracting source and sink points

    Args:
        lines: A GeoDataFrame of transmission lines.
        voltage_threshold: The minimum voltage threshold for lines in kV.

    Returns:
        A GeoDataFrame with processed line data.
    """
    lines["max_voltage"] /= 1000
    lines = lines[~lines["max_voltage"].isnull()]
    lines.loc[:, "max_voltage"] = lines["max_voltage"].replace(220, voltage_threshold)
    lines = (
        lines[lines["max_voltage"] >= voltage_threshold].copy().reset_index(drop=True)
    )
    lines["id"] = [f"line{i}" for i in range(1, len(lines) + 1)]
    lines[["source", "sink"]] = lines["geometry"].apply(
        lambda geom: pd.Series(get_source_sink(geom))
    )
    return lines


def process_buses(buses: gpd.GeoDataFrame, voltage_threshold: int) -> gpd.GeoDataFrame:
    """Processes power substation data by
    1. Converting max voltage to kV
    2. Filtering buses below the voltage threshold
    3. Converting polygons to centroids

    Args:
        buses: A GeoDataFrame of power substations.
        voltage_threshold: The minimum voltage threshold for substations in kV.

    Returns:
        A GeoDataFrame with processed bus data.
    """
    # Convert polygons to centroids
    buses["geometry"] = buses["geometry"].apply(lambda x: x.centroid)
    buses["max_voltage"] /= 1000
    buses = buses[buses["max_voltage"] >= voltage_threshold]
    return buses


def cluster_buses(buses: gpd.GeoDataFrame, cluster_distance: int) -> gpd.GeoDataFrame:
    """Clusters buses within a specified distance of each other.

    Args:
        buses: A GeoDataFrame of power substations.
        cluster_distance: The maximum distance between two buses for them to be in the same cluster.

    Returns:
        A GeoDataFrame with clustered bus locations.
    """
    buses_copy = buses.copy()
    buses_copy["cluster"] = assign_cluster(buses_copy, distance=cluster_distance)

    # Get cluster centroids
    cluster_centroids = (
        buses_copy.loc[buses_copy["cluster"] != -1]
        .dissolve(by="cluster")
        .to_crs(epsg=EPSG_CRS)
        .centroid
    )
    cluster_centroids = cluster_centroids.to_crs(buses.crs).rename("cluster_location")

    # Assign cluster locations to buses if cluster is not -1
    buses_copy["cluster_location"] = buses_copy["cluster"].map(cluster_centroids)

    # For buses not in a cluster, assign the bus location as the cluster location
    buses_copy["cluster_location"] = buses_copy["cluster_location"].fillna(
        buses_copy["geometry"]
    )

    # Replace the geometry column with the cluster location
    buses_copy = buses_copy.drop("geometry", axis=1).rename(
        columns={"cluster_location": "geometry"}
    )

    # Aggregate buses in the same cluster while keeping the maximum voltage
    clustered_buses = buses_copy.groupby("geometry", as_index=False).agg(
        max_voltage=("max_voltage", "max"), count=("max_voltage", "count")
    )
    clustered_buses = gpd.GeoDataFrame(
        clustered_buses, geometry="geometry", crs=buses.crs
    )
    print(
        "No. buses that are clustered:",
        len(clustered_buses[clustered_buses["count"] > 1]),
    )

    clustered_buses["id"] = [f"bus{i}" for i in range(1, len(clustered_buses) + 1)]
    return clustered_buses


def extend_line_to_bus(
    lines: gpd.GeoDataFrame,
    clustered_buses: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Extend line endpoints to the nearest clustered buses.

    Args:
        lines: A GeoDataFrame of transmission lines.
        clustered_buses: A GeoDataFrame of clustered bus locations.

    Returns:
        A GeoDataFrame of lines with end points connected to their nearest buses.
    """
    _, source_nearest = ckdnearest(
        lines, clustered_buses, loc_col_A="source", loc_col_B="geometry"
    )
    _, sink_nearest = ckdnearest(
        lines, clustered_buses, loc_col_A="sink", loc_col_B="geometry"
    )

    lines_copy = lines.copy()
    lines_copy["source_bus"] = source_nearest
    lines_copy["sink_bus"] = sink_nearest

    lines_copy["source_bus_loc"] = lines_copy["source_bus"].map(
        clustered_buses.set_index("id")["geometry"]
    )
    lines_copy["sink_bus_loc"] = lines_copy["sink_bus"].map(
        clustered_buses.set_index("id")["geometry"]
    )
    lines_copy["connected_geometry"] = lines_copy.apply(
        lambda x: extend_line(x["geometry"], x["source_bus_loc"], x["sink_bus_loc"]),
        axis=1,
    )
    # Replace the geometry column with the connected geometry
    lines_copy = lines_copy.drop("geometry", axis=1).rename(
        columns={"connected_geometry": "geometry"}
    )
    # Replace the source and sink columns with source_bus_loc and sink_bus_loc
    lines_copy = lines_copy.drop(["source", "sink"], axis=1)
    lines_copy = lines_copy.rename(
        columns={"source_bus_loc": "source", "sink_bus_loc": "sink"}
    )
    # Set the CRS of the GeoDataFrame
    lines_copy.crs = lines.crs
    # We don't want lines that connect a bus to itself
    lines_copy = lines_copy[lines_copy["source_bus"] != lines_copy["sink_bus"]]
    return lines_copy


def filter_isolated_buses(
    lines: gpd.GeoDataFrame,
    clustered_buses: gpd.GeoDataFrame,
    isolated_bus_distance: int,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Filter isolated buses and identify buses to connect to the network based on a distance threshold.
    This assumes that buses further than the distance is intended to be isolated.

    Args:
        lines: A GeoDataFrame of transmission lines.
        clustered_buses: A GeoDataFrame of clustered bus locations.
        isolated_bus_distance: The distance threshold for isolated buses.

    Returns:
        A tuple of GeoDataFrames containing isolated buses and buses to connect to the network.
    """
    connected_buses = set(lines["source_bus"].tolist() + lines["sink_bus"].tolist())

    isolated_buses = clustered_buses[
        ~clustered_buses["id"].isin(connected_buses)
    ].reset_index(drop=True)

    isolated_buses = keep_distant_points(
        isolated_buses, lines, distance=isolated_bus_distance
    )

    buses_to_connect = clustered_buses[
        clustered_buses["id"].isin(connected_buses)
    ].reset_index(drop=True)

    return isolated_buses, buses_to_connect


def get_lines_to_isolated_buses(
    isolated_buses: gpd.GeoDataFrame,
    buses_to_connect: gpd.GeoDataFrame,
    lines: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """Creates fake lines to connect isolated buses to the network.

    Args:
        isolated_buses: A GeoDataFrame of isolated bus locations.
        buses_to_connect: A GeoDataFrame of bus locations to connect to the network.
        lines: A GeoDataFrame of transmission lines.

    Returns:
        A GeoDataFrame of fake lines connecting isolated buses to the network.
    """
    _, isolated_nearest = ckdnearest(
        isolated_buses,
        buses_to_connect,
        loc_col_A="geometry",
        loc_col_B="geometry",
    )
    isolated_nearest = isolated_nearest.values
    start_points = isolated_buses["geometry"].values
    end_points = (
        buses_to_connect.set_index("id").loc[isolated_nearest, "geometry"].values
    )
    fake_linestrings = [
        LineString([start, end]) for start, end in zip(start_points, end_points)
    ]
    fake_voltages = (
        buses_to_connect.set_index("id").loc[isolated_nearest, "max_voltage"].values
    )

    fake_line_gdf = gpd.GeoDataFrame(
        {
            "id": [f"fake{i}" for i in range(1, len(isolated_buses) + 1)],
            "max_voltage": fake_voltages,
            "source_bus": isolated_buses["id"].values,
            "sink_bus": isolated_nearest,
            "geometry": fake_linestrings,
        },
        geometry="geometry",
        crs=lines.crs,
    )
    return fake_line_gdf


def connect_subgraphs(
    lines: gpd.GeoDataFrame, clustered_buses: gpd.GeoDataFrame, current_iter_num: int
) -> list[dict]:
    """Identifies and connects disconnected subgraphs in the network.

    Args:
        lines: A GeoDataFrame of transmission lines.
        clustered_buses: A GeoDataFrame of clustered bus locations.
        current_iter_num: The current iteration number. Multiple iterations may be needed to connect all subgraphs.

    Returns:
        A list of dictionaries containing information about the connecting lines.
    """

    # 1. Identify disconnected subgraphs
    graph = lines[["source_bus", "sink_bus"]].values.tolist()

    G = Graph(graph)
    subgraphs = list(connected_components(G))

    if len(subgraphs) > 1:
        print(
            f"Round {current_iter_num}: Found {len(subgraphs)} disconnected subgraphs."
        )

        # 2. For each subgraph, find its nearest neighboring subgraph
        connecting_lines = []
        for idx, subgraph in enumerate(subgraphs):
            # First seperate buses in the subgraph from the rest
            subgraph_buses = clustered_buses[
                clustered_buses["id"].isin(subgraph)
            ].reset_index(drop=True)

            other_buses = clustered_buses[
                ~clustered_buses["id"].isin(subgraph)
            ].reset_index(drop=True)

            dist, nearest_buses = ckdnearest(
                subgraph_buses,
                other_buses,
                loc_col_A="geometry",
                loc_col_B="geometry",
            )

            # Find the nearest bus in the subgraph
            subgraph_bus_idx = dist.idxmin()
            subgraph_bus = subgraph_buses.loc[subgraph_bus_idx, "id"]
            nearest_bus = nearest_buses.loc[subgraph_bus_idx]

            # Connect the subgraph to its neighbor
            start_point = subgraph_buses.loc[subgraph_bus_idx, "geometry"]
            end_point = other_buses.set_index("id").loc[nearest_bus, "geometry"]

            connecting_line = LineString([start_point, end_point])

            if connecting_line not in connecting_lines:
                connecting_lines.append(
                    {
                        "id": f"subgraph{idx}-{current_iter_num}",
                        "max_voltage": max(
                            subgraph_buses.loc[subgraph_bus_idx, "max_voltage"],
                            other_buses.set_index("id").loc[nearest_bus, "max_voltage"],
                        ),
                        "source_bus": subgraph_bus,
                        "sink_bus": nearest_bus,
                        "source": start_point,
                        "sink": end_point,
                        "geometry": connecting_line,
                    }
                )
    else:
        print(f"Round {current_iter_num}: No disconnected subgraphs found.")
        connecting_lines = []
    return connecting_lines
