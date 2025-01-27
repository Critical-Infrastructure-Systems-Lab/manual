import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


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


def assign_nearest_substation(
    source_df: pd.DataFrame,
    substations: gpd.GeoDataFrame,
    source_name_col: str,
    substation_geo_col: str = "geometry",
) -> pd.MultiIndex:
    # First convert the target_gdf to a GeoDataFrame
    target_gdf = source_df.copy()
    target_gdf = gpd.GeoDataFrame(
        target_gdf,
        geometry=gpd.points_from_xy(target_gdf["longitude"], target_gdf["latitude"]),
        crs=substations.crs,
    )

    distance, nearest_substations = ckdnearest(
        target_gdf, substations, "geometry", substation_geo_col
    )
    target_gdf["substation"] = nearest_substations.values
    nearest_bus_map = target_gdf.set_index(source_name_col)["substation"].to_dict()
    return distance, nearest_bus_map
