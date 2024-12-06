import googlemaps
import csv
import json

def locations_to_coord(loc_file, csv_file):
    """
    Converts location name strings present in extracted CSV file to their
    corresponding coordinates using Google Maps API.

    @param[in]  loc_file - Name of the file to write the coordinates to
    @param[in]  csv_file - Name of the extracted CSV file

    @return None
    """
    assert isinstance(loc_file, str)
    assert isinstance(csv_file, str)
    assert len(loc_file) > 0
    assert len(csv_file) > 0

    with open(loc_file, "w") as file: # Clear the file
        pass

    gmaps = googlemaps.Client(key="AIzaSyC_opNkguxB9ain47wjBvV1sSrJ_vMhoDI")

    unique_locations = set()
    with open(csv_file, mode="r") as file:
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
        
        with open(loc_file, "a") as file:
            file.write(f"{location} : {coordinates[location]}\n")

# Call this function to convert locations to cordinates
locations_to_coord(loc_file="locations.txt", csv_file="mingextract.csv")



