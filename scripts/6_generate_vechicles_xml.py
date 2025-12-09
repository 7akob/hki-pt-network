from lxml import etree

OUTPUT = "../matsim_input/vehicles.xml"

root = etree.Element("vehicles")
vt = etree.SubElement(root, "vehicleTypes")

bus = etree.SubElement(vt, "vehicleType", id="bus")
engine = etree.SubElement(bus, "engineInformation")
etree.SubElement(engine, "fuelType").text = "diesel"

vtp = etree.SubElement(bus, "capacity")
etree.SubElement(vtp, "seats").text = "40"
etree.SubElement(vtp, "standingRoom").text = "60"

with open(OUTPUT, "wb") as f:
    f.write(etree.tostring(root, pretty_print=True))
