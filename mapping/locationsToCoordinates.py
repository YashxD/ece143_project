import googlemaps
import csv
import json

with open("locations.txt", "w") as file: # Clear the file
    pass

gmaps = googlemaps.Client(key="AIzaSyC_opNkguxB9ain47wjBvV1sSrJ_vMhoDI")

unique_locations = set()
with open("mingextract.csv", mode="r") as file:
    reader = csv.DictReader(file)  # Use DictReader for named columns
    for row in reader:
        unique_locations.add(row["location"])
unique_locations_list = list(unique_locations)

bounds = {"southwest": {"lat": 32.846263, "lng": -117.270637}, "northeast": {"lat": 32.897726, "lng": -117.184645}} 

# Get coordinates for each location
coordinates = {}
for location in unique_locations_list:
    result = gmaps.geocode(location + ", San Diego", components = bounds)
    if result:
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
        if (lat > bounds["southwest"]["lat"] and lat < bounds["northeast"]["lat"] and lng > bounds["southwest"]["lng"] and lng < bounds["northeast"]["lng"]):
            coordinates[location] = (lat, lng)
        else:
            print(f"Found outside of bounds: {location}")
            coordinates[location] = None
        
    else:
        coordinates[location] = None
        print(f"Could not locate: {location}")
    
    print(f"{location} : {coordinates[location]}")
    
    with open("locations.txt", "a") as file:
        file.write(f"{location} : {coordinates[location]}\n")





