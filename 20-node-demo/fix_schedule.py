import xml.etree.ElementTree as ET
from itertools import cycle

schedule_path = "transitSchedule.xml"
output_path = "transitSchedule_fixed.xml"

tree = ET.parse(schedule_path)
root = tree.getroot()

bus_cycle = cycle(["veh_bus_1", "veh_bus_2"])
veh_map_single = {
    "line_metro": "veh_tram_1",
    "line_train": "veh_tram_1",
    "line_tram":  "veh_tram_1",
    # default: veh_bus_1
}

for line in root.findall("transitLine"):
    line_id = line.get("id")
    for route in line.findall("transitRoute"):
        deps_parent = route.find("departures")
        if deps_parent is None:
            continue

        for dep in deps_parent.findall("departure"):
            # if already has vehicleRefId, don't touch
            if "vehicleRefId" in dep.attrib:
                continue

            if line_id == "line_bus":
                dep.set("vehicleRefId", next(bus_cycle))
            else:
                dep.set("vehicleRefId", veh_map_single.get(line_id, "veh_bus_1"))

tree.write(output_path, encoding="utf-8", xml_declaration=True)
print("Wrote patched schedule to", output_path)
