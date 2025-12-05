import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
GTFS_DIR = os.path.join(BASE_DIR, "data", "gtfs")
INTERMEDIATE_DIR = os.path.join(BASE_DIR, "data", "intermediate")

os.makedirs(INTERMEDIATE_DIR, exist_ok=True)

# Load GTFS stops
stops = pd.read_csv(os.path.join(GTFS_DIR, "stops.txt"))

# Ensure required columns exist
if not {"stop_lat", "stop_lon"}.issubset(stops.columns):
    raise ValueError("GTFS stops.txt is missing stop_lat or stop_lon columns!")

# Create GeoDataFrame (WGS84)
geometry = [Point(lon, lat) for lon, lat in zip(stops.stop_lon, stops.stop_lat)]
gdf_stops = gpd.GeoDataFrame(stops, geometry=geometry, crs="EPSG:4326")

# Save GeoJSON
outpath = os.path.join(INTERMEDIATE_DIR, "gtfs_stops.geojson")
gdf_stops.to_file(outpath, driver="GeoJSON")

print("Saved:", outpath, "with", len(gdf_stops), "features")
