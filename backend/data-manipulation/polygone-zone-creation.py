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


def determine_crime_zones_score(all_crime_zones):
    # new dict from initial dict
    zones_score = {}

    for place_name, crime_list in all_crime_zones.items():
        # put the scoring algorithm function here
        score = 50
        # new dict design
        zones_score[place_name] = {"score": score, "crimes": crime_list}
    return zones_score



if __name__ == "__main__":
    database = db.client.open_montreal
    collection = database.actes_criminels
    borough_list = {}
    create_crime_zone(collection,borough_list)
    db.client.close()
