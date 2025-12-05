import subprocess
import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
MATSim_JAR = BASE_DIR / "matsim" / "matsim.jar"
OSM_FILE = BASE_DIR / "data" / "osm" / "finland-latest.osm.pbf"
OUTPUT_NETWORK = BASE_DIR / "data" / "matsim" / "network.xml"

JAVA = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.17.10-hotspot\bin\java.exe"

os.makedirs(os.path.dirname(OUTPUT_NETWORK), exist_ok=True)

# --- Build correct Java command ---
CMD = [
    JAVA,
    "-cp", str(MATSim_JAR),
    "org.matsim.application.prepare.network.PrepareOSMNetwork",
    "--osm", str(OSM_FILE),
    "--output", str(OUTPUT_NETWORK),
    "--keepPaths",
    "--inferLanes",
    "--inferSpeeds"
]

print("Running MATSim network converter...")
print(" ".join(CMD))

result = subprocess.run(CMD, capture_output=True, text=True)

print("\n--- STDOUT ---")
print(result.stdout)
print("\n--- STDERR ---")
print(result.stderr)
