# Import the Flask class from the flask module
from flask import Flask, jsonify
from flask_cors import CORS

from additional_information_queries import get_additional_information
from backend import db_connection as db
from backend import score
from backend.score import calculate_score

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

database = db.client.open_montreal
collection = database.actes_criminels


# Define a route for the root URL
def remove_none_values(dictionary):
    return {key: value for key, value in dictionary.items() if key is not None}


@app.route("/additional")
def send_addtionial_info():
    info_dict = get_additional_information(collection)
    # Check if info_dict is None before jsonify
    if info_dict is not None:
        info_dict_processed = remove_none_values(info_dict)
        response = jsonify(info_dict_processed)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    else:
        # Handle the case where info_dict is None, e.g., return an appropriate response
        return jsonify({"error": "No additional information available"})


@app.route("/score")
def send_score():
    score_dict = calculate_score()
    if score_dict is not None:
        response = jsonify(score_dict)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    else:
        # Handle the case where info_dict is None, e.g., return an appropriate response
        return jsonify({"error": "No additional information available"})


if __name__ == "__main__":
    app.run(debug=True)