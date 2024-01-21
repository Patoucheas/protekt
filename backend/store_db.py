import json
from pymongo import MongoClient

# MongoDB connection string
atlas_connection_uri = "mongodb+srv://gen:gen123@cluster0.bqucodi.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(atlas_connection_uri)

# Database name
db = client.open_montreal

# GeoJSON file paths and their corresponding collection names
geojson_files = {
    "pdq.geojson": "pdq"

    # Add more files and collections as needed
}


# Function to load GeoJSON data and insert into MongoDB
def upload_geojson(file_path, collection_name, ):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Assuming each file is a FeatureCollection
        if data['type'] == 'FeatureCollection':
            features = data['features']
            db[collection_name].insert_many(features)
        else:
            db[collection_name].insert_one(data)
    print(f"Uploaded data from {file_path} to {collection_name}")


# Upload each GeoJSON file to its corresponding collection
for file_path, collection_name in geojson_files.items():
    upload_geojson(file_path, collection_name)

print("All data uploaded successfully")
