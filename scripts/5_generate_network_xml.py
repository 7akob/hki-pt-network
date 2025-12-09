import pandas as pd
import geopandas as gpd
from lxml import etree

STOPS_FILE = "../data/intermediate/gtfs_stops_snapped.geojson"
OUTPUT = "../matsim_input/transitSchedule.xml"

stops = gpd.read_file(STOPS_FILE)

def write_schedule(stops, out_file):
    root = etree.Element("transitSchedule")

    # Transit Stops
    ts = etree.SubElement(root, "transitStops")
    for _, stop in stops.iterrows():
        etree.SubElement(
            ts, "transitStopFacility",
            id=str(stop.stop_id),
            x=str(stop.geometry.x),
            y=str(stop.geometry.y),
            linkRefId=str(stop.nearest_node)
        )

    # One simple transit line
    line = etree.SubElement(root, "transitLine", id="Line1")
    route = etree.SubElement(line, "transitRoute", id="Route1")

    mode = etree.SubElement(route, "transportMode")
    mode.text = "bus"

    # Route profile
    profile = etree.SubElement(route, "routeProfile")
    for _, stop in stops.head(20).iterrows():
        etree.SubElement(profile, "stop", refId=str(stop.stop_id))

    # Departures every 10 minutes
    departures = etree.SubElement(route, "departures")
    for i in range(0, 3600 * 3, 600):
        dep = etree.SubElement(departures, "departure", id=str(i))
        dep.set("departureTime", str(i))

    with open(out_file, "wb") as f:
        f.write(etree.tostring(root, pretty_print=True))

write_schedule(stops, OUTPUT)
print("Created transitSchedule.xml")
