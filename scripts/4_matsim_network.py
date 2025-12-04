import subprocess
import os

JAVA = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot\bin\java.exe"
MATSim_JAR = r"..\matsim\matsim.jar"
OSM_FILE = r"..\data\osm\finland-latest.osm.pbf"
OUTPUT_NETWORK = r"..\data\matsim\network.xml"

os.makedirs(r"..\data\matsim", exist_ok=True)

CMD = [
    JAVA,
    "-cp", MATSim_JAR,
    "org.matsim.utils.CreateNetwork",
    OSM_FILE,
    OUTPUT_NETWORK
]

print("Running MATSim converter...")
print(" ".join(CMD))

result = subprocess.run(CMD, capture_output=True, text=True)

print(result.stdout)
print(result.stderr)
