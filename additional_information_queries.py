from backend import db_connection as db
import test_data_manipulation as data_coordinates


def get_additional_information(db_collection):
    # get the number of crime
    pipeline = [
        {
            "$group": {
                "_id": "$city",
                "crime_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "city": "$_id",
                "crime_count": 1
            }
        }
    ]
    numberOfCrimePerRegion = list(db_collection.aggregate(pipeline))

    # get most common type of crime
    pipeline = [
        {
            "$match": {
                "properties.CATEGORIE": {"$exists": True, "$ne": None}
            }
        },
        {
            "$group": {
                "_id": {"city": "$city", "crime_type": "$properties.CATEGORIE"},
                "crime_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"crime_count": -1}
        },
        {
            "$group": {
                "_id": "$_id.city",
                "most_common_crime": {"$first": "$_id.crime_type"},
                "crime_count": {"$first": "$crime_count"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "city": "$_id",
                "most_common_crime": 1,
                "crime_count": 1
            }
        }
    ]

    mostCommonCrimePerRegion = list(db_collection.aggregate(pipeline))
    additional_information = { x['city']: {'crime_count': x['crime_count']} for x in numberOfCrimePerRegion }

    for elem in mostCommonCrimePerRegion:
        additional_information[elem['city']]['most_common_crime'] = elem['most_common_crime']

    #print(numberOfCrimePerRegion)
    print(additional_information)
    print(len(additional_information))
    #print(mostCommonCrimePerRegion)
    return additional_information


if __name__ == "__main__":
    database = db.client.open_montreal
    collection = database.actes_criminels
    get_additional_information(collection)
