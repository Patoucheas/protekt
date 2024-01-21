# Import the Flask class from the flask module
from flask import Flask
from additional_information_queries import get_additional_information as info
from backend import db_connection as db
import jsonify

# Create an instance of the Flask class
app = Flask(__name__)


# Define a route for the root URL
@app.route("/temp")
def home():
    return "Server is up bitch"


@app.route("/additional")
def send_addtionial_info():
    info

# Run the application if this script is executed


if __name__ == "__main__":
    app.run(debug=True)