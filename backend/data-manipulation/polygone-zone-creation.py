from backend import db_connection as db
import test_data_manipulation as data_coordinates
from shapely.geometry import mapping


def create_crime_zone(db_collection, boroughs_polygon):

    all_crime_zones = {}
    for place_name, polygon_coordinates in boroughs_polygon.items():
        polygon_geojson = mapping(polygon_coordinates)

        # query the locations of crime within polygon
        query = {
            "geometry": {
                "$geoWithin": {
                    "$geometry": polygon_geojson
                }
            }
        }
        crimes_in_zone = list(db_collection.find(query))
        # Add a new field "city" to each crime document and set it to the place_name
        for crime in crimes_in_zone:
            crime["city"] = place_name

        # Update the documents in the collection with the new "city" field
        update_query = {"_id": {"$in": [crime["_id"] for crime in crimes_in_zone]}}
        update_operation = {
            "$set": {"city": place_name}
        }
        db_collection.update_many(update_query, update_operation)
        # Print or process the result
        if crimes_in_zone:
            print(place_name + " in crime zone")
            all_crime_zones.update({place_name: crimes_in_zone})
        else:
            print(place_name + " No crimes found within the polygon zone.")
    for city in all_crime_zones:
        print("Number of crime in ",city, ": ", len(all_crime_zones[city]))

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
    borough_dict = data_coordinates.get_borough_coordinates()
    create_crime_zone(collection,borough_dict)
    db.client.close()
