from backend import db_connection as db

if __name__ == "__main__":

    database = db.client.open_montreal

    collection = database.actes_criminels

    # test a basic query
    condition = {"properties.CATEGORIE": "Méfait"}
    count_result = collection.count_documents(condition)
    print(f"Number of documents matching the condition: {count_result}")

    db.client.close()
