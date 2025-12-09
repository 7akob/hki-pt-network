import random
from lxml import etree

OUTPUT = "../matsim_input/population.xml"

root = etree.Element("population")

for pid in range(2000):
    person = etree.SubElement(root, "person", id=str(pid))
    plan = etree.SubElement(person, "plan", selected="yes")

    etree.SubElement(
        plan, "activity",
        type="home",
        x="385000",
        y="6670000",
        end_time=str(random.randint(6*3600, 9*3600))
    )

    etree.SubElement(
        plan, "leg",
        mode="pt"
    )

    etree.SubElement(
        plan, "activity",
        type="work",
        x="384000",
        y="6673000"
    )

with open(OUTPUT, "wb") as f:
    f.write(etree.tostring(root, pretty_print=True))
