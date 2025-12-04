import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

GTFS_DIR = "../data/gtfs/"

stops = pd.read_csv(GTFS_DIR + "stops.txt")
routes = pd.read_csv(GTFS_DIR + "routes.txt")
trips = pd.read_csv(GTFS_DIR + "trips.txt")
stop_times = pd.read_csv(GTFS_DIR + "stop_times.txt")
shapes = pd.read_csv(GTFS_DIR + "shapes.txt")
calendar = pd.read_csv(GTFS_DIR + "calendar.txt")
calendar_dates = pd.read_csv(GTFS_DIR + "calendar_dates.txt")

# --- convert stops to GeoDataFrame ---
gdf_stops = gpd.GeoDataFrame(
    stops,
    geometry=[Point(xy) for xy in zip(stops.stop_lon, stops.stop_lat)],
    crs="EPSG:4326"
)

# ensure intermediate folder exists
os.makedirs("../data/intermediate", exist_ok=True)

# save GTFS stops as geojson (used by script 3)
gdf_stops.to_file("../data/intermediate/gtfs_stops.geojson", driver="GeoJSON")

print("Saved to ../data/intermediate/gtfs_stops.geojson")