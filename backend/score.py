from math import ceil

import pandas as pd
from pymongo import MongoClient

# MongoDB connection string
atlas_connection_uri = "mongodb+srv://gen:gen123@cluster0.bqucodi.mongodb.net/?retryWrites=true&w=majority"

def separate_crimes_by_city():
    # Connect to MongoDB Atlas
    client = MongoClient(atlas_connection_uri)

    # Database name
    db = client.open_montreal

    collection = db["actes_criminels"]

    query = {"city": {"$exists": True, "$ne": None}}
    # Projection to return only certain fields
    projection = {
        "properties.CATEGORIE": 1,
        "properties.DATE": 1,
        "properties.QUART": 1,
        "city": 1,
        "_id": 0
    }

    # Query the collection
    documents = collection.find(query, projection)
    crimes_separated = {}

    for doc in documents:
        city = doc["city"]
        if city not in crimes_separated:
            crimes_separated[city] = []

        crimes_separated[city].append({
            "categorie": doc["properties"]["CATEGORIE"],
            "date": doc["properties"]["DATE"],
            "quart": doc["properties"]["QUART"]
        })

    return crimes_separated



def calculate_score():
    #df = pd.read_csv("C:/Users/korjo/Documents/compsci/personal/protekt/population_arrondissements.csv")
    df = pd.read_csv("population_arrondissements.csv")
    locs = [x for x in df['Location']]
    population = {x: df[df['Location'] == x]['Population'].values[0] for x in locs}
    crimes_by_city = separate_crimes_by_city()
    weights = {
        "Infractions entrainant la mort": 3.5,
        "Introduction": 1.25,
        "Méfait": 1,
        "Vol dans / sur véhicule à moteur": 1.75,
        "Vol de véhicule à moteur": 1.5,
        "Vols qualifiés": 2,
    }
    result = {}
    per_capita = 100
    for city, crimes in crimes_by_city.items():
        number_of_crimes = len(crimes)
        score = 0
        # filtered_df = df[df['Location'] == city]['Population']
        if city in population.keys():
            pop = population[city]
            for crime in crimes:
                score += weights[crime['categorie']]
            result[city] = ceil((score / pop) * per_capita)

    fill_missing_scores(result, crimes_by_city, weights)

    return result
def fill_missing_scores(pre_proc, city_crimes, weight_list):
    missing = {
        'Villeray-Saint-Michel-Parc-Extension': 142222,
        'Mercier-Hochelaga-Maisonneuve': 131483,
        'Rosemont-La Petite-Patrie': 134038,
        'Côte-des-Neiges-Notre-Dame-de-Grâce': 165031,
        'Rivière-des-Prairies-Pointe-aux-Trembles': 106437,
        "L'Île-Bizard-Sainte-Geneviève": 18097,
    }
    per_capita = 100
    for city, crimes in city_crimes.items():
        number_of_crimes = len(crimes)
        score = 0
        # filtered_df = df[df['Location'] == city]['Population']
        if city in missing.keys():
            pop = missing[city]
            for crime in crimes:
                score += weight_list[crime['categorie']]
            pre_proc[city] = ceil((score / pop) * per_capita)

if __name__ == "__main__":
    test = calculate_score()
    print(test)
    for key in test.keys():
        print(key, test[key])
