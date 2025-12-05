import geopandas as gpd
import osmnx as ox

G = ox.load_graphml("../data/osm/helsinki_all.graphml")

# Project only network temporarily
G_proj = ox.project_graph(G, to_crs="EPSG:3879")
nodes_proj, edges_proj = ox.graph_to_gdfs(G_proj)

gtfs_stops = gpd.read_file("../data/intermediate/gtfs_stops.geojson")

# Project to metric for the snapping operation
gtfs_proj = gtfs_stops.to_crs("EPSG:3879")

nearest = ox.nearest_nodes(
    G_proj, gtfs_proj.geometry.x, gtfs_proj.geometry.y
)

# Add nearest node ID back to original (WGS84) GeoDataFrame
gtfs_stops["nearest_node"] = nearest

gtfs_stops.to_file(
    "../data/intermediate/gtfs_stops_snapped.geojson",
    driver="GeoJSON"
)
