# Data folder structure
```
hki-pt-network/
  data/
    osm/ # Generated with sctipt 1
      helsinki_drive.graphml
      helsinki_walk.graphml
    gtfs/ # Manually imported to from hsl gtfs zip 
      stops.txt
      routes.txt
      trips.txt
      stop_times.txt
      shapes.txt
      calendar.txt
      calendar_dates.txt
    matsim/
      # IN PROGRESS
    demand/
      # TO-DO
    intermediate/ # Generated with script 3
      gtfs_stops.geojson
      gtfs_stops_snapped.geojson
```