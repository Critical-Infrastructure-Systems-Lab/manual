import unittest
import geopandas as gpd
from shapely.geometry import LineString, Point
from shapely.ops import snap

# Functions to test
from geospatial_utils import split_overpassing_lines


def check_distance_percentage(
    segment: LineString, point1: Point, point2: Point, threshold_percent: float = 0.01
) -> bool:
    """Checks if the distance between the endpoints of a line segment and two points
    is less than a specified percentage of the segment's length.

    Args:
        segment (LineString): The line segment.
        point1 (Point): The first point.
        point2 (Point): The second point.
        threshold_percent (float, optional): The distance threshold as a percentage
                                            of the segment's length. Defaults to 0.05.

    Returns:
        bool: True if the distances are within the threshold, False otherwise.
    """
    threshold_distance = segment.length * (threshold_percent / 100)
    return (
        (segment.boundary.geoms[0].distance(point1) < threshold_distance)
        and (segment.boundary.geoms[1].distance(point2) < threshold_distance)
    ) or (
        (segment.boundary.geoms[1].distance(point1) < threshold_distance)
        and (segment.boundary.geoms[0].distance(point2) < threshold_distance)
    )


class TestSplitOverpassingLines(unittest.TestCase):

    def test_split_overpassing_lines_1(self):
        crs = 32618
        # Create a line segment
        line1 = LineString([(0, 0), (100, 0)])
        line2 = LineString([(-200, 0), (-205, 0)])
        lines_gdf = gpd.GeoDataFrame(
            {
                "id": ["line1", "line2"],
                "max_voltage": [230, 230],
                "circuits": [2, 3],
                "cables": [6, 7],
                "source": [Point(0, 0), Point(-200, 0)],
                "sink": [Point(100, 0), Point(-205, 0)],
                "geometry": [line1, line2],
            },
            geometry="geometry",
            crs=crs,
        )

        # Create points
        point1 = Point(-100, 100)  # Outside filter_distance
        point2 = Point(50, 0)  # Exactly on the line
        point3 = Point(75, 10)  # Within filter_distance
        point4 = Point(100, 0)  # Exactly at one end of the line

        buses_gdf = gpd.GeoDataFrame(
            {
                "name": ["bus1", "bus2", "bus3", "bus4"],
                "max_voltage": [230, 230, 230, 230],
                "geometry": [point1, point2, point3, point4],
            },
            geometry="geometry",
            crs=crs,
        )

        # Call the function
        filter_distance = 50
        result_gdf = split_overpassing_lines(lines_gdf, buses_gdf, filter_distance)

        # Assertions
        self.assertEqual(len(result_gdf), 4)  # Expect 3 segments after splitting

        # Check if the line is split at the correct locations
        expected_segments = [
            LineString([(0, 0), (50, 0)]),
            LineString([(50, 0), (75, 0)]),  # Split at the projected point of point3
            LineString([(75, 0), (100, 0)]),
            LineString([(-200, 0), (-205, 0)]),
        ]

        # Sort the result and expected segments based on the x-coordinate of the first point
        # This is to handle the unpredictable order of segments from the function
        result_segments = sorted(
            result_gdf.geometry.tolist(), key=lambda line: line.coords[0][0]
        )
        expected_segments = sorted(
            expected_segments, key=lambda line: line.coords[0][0]
        )

        for result_segment, expected_segment in zip(result_segments, expected_segments):
            self.assertTrue(result_segment.almost_equals(expected_segment, decimal=3))

    def test_split_overpassing_lines_2(self):
        line = gpd.read_file("line462.geojson")
        buses = gpd.read_file("line462_bus.geojson")
        point_to_split = Point(1039671.645, 17863146.893)

        filter_distance = 300
        result_gdf = split_overpassing_lines(line, buses, filter_distance)

        # Assertions
        self.assertEqual(
            len(result_gdf), 2
        )  # Check if the line is split into two segments

        # Extract the start and end points of the original line
        line_start = Point(line.geometry[0].coords[0])
        line_end = Point(line.geometry[0].coords[-1])

        # Snap the point_to_split to the line to ensure accurate comparison
        snapped_point = snap(point_to_split, line.geometry[0], tolerance=1e-3)

        # Check if the segments have the correct start and end points
        segment1 = result_gdf.geometry[0]
        segment2 = result_gdf.geometry[1]

        self.assertTrue(check_distance_percentage(segment1, line_start, snapped_point))
        self.assertTrue(check_distance_percentage(segment2, snapped_point, line_end))


if __name__ == "__main__":
    unittest.main()
