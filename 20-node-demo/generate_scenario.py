import math
import csv
import random

# -------------------------------
# NODE DEFINITIONS
# -------------------------------
nodes = [
    ("aalto", 24.826, 60.184),
    ("tapiola", 24.806, 60.176),
    ("leppavaara", 24.813, 60.219),
    ("huopalahti", 24.884, 60.220),
    ("myyrmaki", 24.843, 60.288),
    ("pasila", 24.933, 60.199),
    ("kamppi", 24.932, 60.169),
    ("ruoholahti", 24.915, 60.163),
    ("rautatientori", 24.941, 60.171),
    ("hakaniemi", 24.951, 60.179),
    ("kalasatama", 24.977, 60.188),
    ("herttoniemi", 25.031, 60.190),
    ("itakeskus", 25.081, 60.213),
    ("kontula", 25.075, 60.226),
    ("mellunmaki", 25.108, 60.244),
    ("malmi", 25.012, 60.251),
    ("oulunkyla", 24.990, 60.234),
    ("lauttasaari", 24.874, 60.159),
    ("munkkiniemi", 24.880, 60.200),
    ("espoonkeskus", 24.657, 60.205)
]

# Convert to roughly meter coordinates
def project(x, y):
    return (x * 100000, y * 100000)

node_dict = {n[0]: project(n[1], n[2]) for n in nodes}


# -------------------------------
# TRANSIT LINES (synthetic)
# -------------------------------
lines = {
    "metro": {
        "stations": ["aalto","tapiola","kamppi","rautatientori","hakaniemi","kalasatama","herttoniemi","itakeskus"],
        "freq": 4,
        "capacity": 800,
        "mode": "metro"
    },
    "train": {
        "stations": ["espoonkeskus","leppavaara","huopalahti","pasila","rautatientori"],
        "freq": 10,
        "capacity": 600,
        "mode": "train"
    },
    "tram": {
        "stations": ["kamppi","rautatientori","hakaniemi","kalasatama"],
        "freq": 8,
        "capacity": 200,
        "mode": "tram"
    },
    "bus": {
        "stations": ["mellunmaki","kontula","itakeskus"],
        "freq": 15,
        "capacity": 80,
        "mode": "bus"
    }
}


# -------------------------------
# DEMAND GENERATION
# -------------------------------
with open("demand_15min.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["from","to","time_slot_min","demand"])

    time_slots = [i * 15 for i in range(96)]

    major_pairs = [
        ("aalto","itakeskus", 8),
        ("kamppi","itakeskus", 12),
        ("espoonkeskus","kamppi", 15),
        ("tapiola","rautatientori", 10),
        ("pasila","kamppi", 18),
        ("kontula","kamppi", 14),
        ("mellunmaki","itakeskus", 9),
        ("leppavaara","rautatientori", 16)
    ]

    for (frm, to, base) in major_pairs:
        for t in time_slots:
            hour = t // 60
            peak = (7 <= hour <= 9) or (16 <= hour <= 18)
            demand = base * (2.5 if peak else 1.0)
            demand *= random.uniform(0.8, 1.2)
            writer.writerow([frm, to, t, max(1, int(demand))])


# -------------------------------
# NETWORK.XML  (FIXED VERSION)
# -------------------------------
with open("network.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">\n')
    f.write('<network>\n')
    f.write('  <nodes>\n')

    for nid, (x, y) in node_dict.items():
        f.write(f'    <node id="{nid}" x="{x}" y="{y}" />\n')

    f.write('  </nodes>\n')
    f.write('  <links>\n')

    link_id = 0
    for line in lines.values():
        st = line["stations"]
        for i in range(len(st)-1):
            a, b = st[i], st[i+1]
            x1,y1 = node_dict[a]
            x2,y2 = node_dict[b]
            dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)

            f.write(
                f'    <link id="l{link_id}" from="{a}" to="{b}" '
                f'length="{dist}" freespeed="20" capacity="2000" '
                f'permlanes="1" modes="pt" />\n'
            )
            link_id += 1

    f.write('  </links>\n')
    f.write('</network>\n')

# -------------------------------
# TRANSIT SCHEDULE (FIXED VERSION)
# -------------------------------

# 1) Build node→first_link mapping so stopFacilities get a correct linkRefId
node_to_link = {}

# Collect links per line in order
all_links = []  # (id, from, to)

link_id = 0
for line in lines.values():
    st = line["stations"]
    for i in range(len(st) - 1):
        a, b = st[i], st[i+1]
        link_name = f"l{link_id}"
        all_links.append((link_name, a, b))

        # Assign link to node if not already assigned (MATSim requires any valid attached link)
        if a not in node_to_link:
            node_to_link[a] = link_name
        node_to_link[b] = link_name

        link_id += 1


# 2) Build transitSchedule.xml
with open("transitSchedule.xml", "w") as f:
    f.write('<transitSchedule>\n')

    # ---- STOP FACILITIES ----
    f.write('  <transitStops>\n')
    for nid, (x, y) in node_dict.items():
        if nid not in node_to_link:
            continue  # skip nodes with no PT lines
        f.write(
            f'    <stopFacility id="stop_{nid}" x="{x}" y="{y}" '
            f'linkRefId="{node_to_link[nid]}" name="{nid}" />\n'
        )
    f.write('  </transitStops>\n')

    # ---- TRANSIT LINES & ROUTES ----
    for line_name, data in lines.items():
        stations = data["stations"]
        mode = data["mode"]
        freq = data["freq"]

        f.write(f'  <transitLine id="line_{line_name}">\n')
        f.write(f'    <transitRoute id="route_{line_name}">\n')
        f.write(f'      <transportMode>{mode}</transportMode>\n')

        # ---- Route profile (stop sequence) ----
        f.write('      <routeProfile>\n')
        for s in stations:
            f.write(
                f'        <stop refId="stop_{s}" departureOffset="00:00:00"/>\n'
            )
        f.write('      </routeProfile>\n')

        # ---- Link sequence (from network) ----
        f.write('      <route>\n')
        # Extract links that match this line's station pairs
        for i in range(len(stations) - 1):
            a = stations[i]
            b = stations[i+1]
            # find matching link
            for link_name, lf, lt in all_links:
                if lf == a and lt == b:
                    f.write(f'        <link refId="{link_name}"/>\n')
                    break
        f.write('      </route>\n')

        # ---- Departures (05:00–23:00) ----
        f.write('      <departures>\n')
        for minutes in range(300, 1381, freq):
            hh = minutes // 60
            mm = minutes % 60
            dep_time = f"{hh:02d}:{mm:02d}:00"
            dep_id = f"d_{line_name}_{minutes}"
            f.write(
                f'        <departure id="{dep_id}" departureTime="{dep_time}"/>\n'
            )
        f.write('      </departures>\n')

        f.write('    </transitRoute>\n')
        f.write('  </transitLine>\n')

    f.write('</transitSchedule>')


# -------------------------------
# TRANSIT VEHICLES
# -------------------------------
with open("transitVehicles.xml", "w") as f:
    f.write('<transitVehicles>\n')
    vid = 0
    for name, data in lines.items():
        for _ in range(10):
            f.write(f'  <vehicle id="{name}_{vid}" type="{name}_v"/>\n')
            vid += 1
    f.write('</transitVehicles>')


# -------------------------------
# POPULATION (1000 agents)  -- FIXED
# -------------------------------
with open("population.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
    f.write('<population>\n')

    pid = 0
    with open("demand_15min.csv") as dfile:
        reader = list(csv.DictReader(dfile))
        for row in reader[:1000]:
            frm = row["from"]
            to = row["to"]
            t = int(row["time_slot_min"])
            hh = t // 60
            mm = t % 60
            fx, fy = node_dict[frm]
            tx, ty = node_dict[to]

            f.write(f'  <person id="p{pid}">\n')
            f.write('    <plan>\n')
            f.write(f'      <activity type="home" x="{fx}" y="{fy}" end_time="{hh:02d}:{mm:02d}:00" />\n')
            f.write('      <leg mode="pt" />\n')
            f.write(f'      <activity type="work" x="{tx}" y="{ty}" />\n')
            f.write('    </plan>\n')
            f.write('  </person>\n')
            pid += 1

    f.write('</population>\n')
