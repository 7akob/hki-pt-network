import osmnx as ox

ox.settings.log_console = True
ox.settings.use_cache = True

places = [
    "Helsinki, Finland",
    "Espoo, Finland",
    "Vantaa, Finland",
    "Kauniainen, Finland"
]

# Full OSM graph for MATSim (driveable + walkable)
G = ox.graph_from_place(places, network_type="all")

ox.save_graphml(G, "../data/osm/helsinki_all.graphml")
