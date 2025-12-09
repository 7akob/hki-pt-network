import osmnx as ox
from lxml import etree

INPUT = "../data/osm/helsinki_drive.graphml"
OUTPUT = "../matsim_input/network.xml"

G = ox.load_graphml(INPUT)

def write_matsim_network(G, out_file):
    network = etree.Element("network")
    nodes_el = etree.SubElement(network, "nodes")
    links_el = etree.SubElement(network, "links")

    # Nodes
    for node_id, data in G.nodes(data=True):
        etree.SubElement(
            nodes_el, "node",
            id=str(node_id),
            x=str(data["x"]),
            y=str(data["y"])
        )

    # Links
    link_id = 0
    for u, v, data in G.edges(data=True):
        etree.SubElement(
            links_el, "link",
            id=str(link_id),
            from_=str(u),
            to=str(v),
            length=str(data.get("length", 30)),
            freespeed=str(data.get("speed_kph", 40) / 3.6),
            capacity="1000",
            permlanes="1"
        )
        link_id += 1

    with open(out_file, "wb") as f:
        f.write(etree.tostring(network, pretty_print=True))

write_matsim_network(G, OUTPUT)
print("Created network.xml")
