import osmnx as ox

# To see download logs
ox.settings.log_console = True
ox.settings.use_cache = True

place = ["Helsinki, Finland", "Espoo, Finland", "Vantaa, Finland", "Kauniainen, Finland"]

G_drive = ox.graph_from_place(place, network_type="drive")
G_walk  = ox.graph_from_place(place, network_type="walk")

ox.save_graphml(G_drive, "../data/osm/helsinki_drive.graphml")
ox.save_graphml(G_walk,  "../data/osm/helsinki_walk.graphml")
