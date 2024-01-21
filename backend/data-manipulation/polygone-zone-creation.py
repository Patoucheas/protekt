from backend import db_connection as db


def create_crime_zone(db_collection):
    # create the polygon geojson
    polygon_geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.690, 45.514],  # Bottom-left corner
                [-73.690, 45.524],  # Top-left corner
                [-73.682, 45.524],  # Top-right corner
                [-73.682, 45.514],  # Bottom-right corner
                [-73.690, 45.514]   # Closing the polygon
            ]
        ]
    }

    # query the locations of crime within polygon
    query = {
        "geometry": {
            "$geoWithin": {
                "$geometry": polygon_geojson
            }
        }
    }
    crimes_in_zone = list(collection.find(query))
    # Print or process the result
    if crimes_in_zone:
        print("Crimes within the polygon zone:")
        for crime in crimes_in_zone:
            print(crime)
    else:
        print("No crimes found within the polygon zone.")


if __name__ == "__main__":
    database = db.client.open_montreal
    collection = database.actes_criminels
    create_crime_zone(collection)
    db.client.close()
