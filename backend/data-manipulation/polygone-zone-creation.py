from backend import db_connection as db


def create_crime_zone(db_collection, boroughs_polygon):

    all_crime_zones = {}
    for place_name, polygon_coordinates in boroughs_polygon.items():
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": [polygon_coordinates]
        }

        # query the locations of crime within polygon
        query = {
            "geometry": {
                "$geoWithin": {
                    "$geometry": polygon_geojson
                }
            }
        }
        crimes_in_zone = list(db_collection.find(query))
        # Print or process the result
        if crimes_in_zone:
            all_crime_zones.update({place_name: crimes_in_zone})
        else:
            print("No crimes found within the polygon zone.")
    return all_crime_zones


if __name__ == "__main__":
    database = db.client.open_montreal
    collection = database.actes_criminels
    borough_list = {}
    create_crime_zone(collection,borough_list)
    db.client.close()
