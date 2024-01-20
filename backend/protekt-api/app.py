# Import the Flask class from the flask module
from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)


# Define a route for the root URL
@app.route("/temp")
def home():
    return "Server is up bitch"


# Run the application if this script is executed
if __name__ == "__main__":
    app.run(debug=True)