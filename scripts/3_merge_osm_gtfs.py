import geopandas as gpd
import osmnx as ox

# Load graph
G = ox.load_graphml("../data/osm/helsinki_drive.graphml")

# Project to metric CRS (Helsinki)
G_proj = ox.project_graph(G, to_crs="EPSG:3879")

# Create nodes/edges GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G_proj)

# Load GTFS stops
gtfs_stops = gpd.read_file("../data/intermediate/gtfs_stops.geojson")

# Project GTFS stops into same CRS
gtfs_stops = gtfs_stops.to_crs("EPSG:3879")

# Find nearest OSM node for each GTFS stop
stop_to_node = ox.nearest_nodes(
    G_proj,
    gtfs_stops.geometry.x,
    gtfs_stops.geometry.y
)

gtfs_stops["nearest_node"] = stop_to_node

# Save output
gtfs_stops.to_file("../data/intermediate/gtfs_stops_snapped.geojson", driver="GeoJSON")

print("Snapped GTFS stops saved.")
