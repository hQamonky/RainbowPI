import markdown
import os
import pigpio

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)
pi = pigpio.pi()


# Route shows the user guide file.
@app.route('/')
def index():
    # Open file
    with open(os.path.dirname(app.root_path) + "/../docs/API User Guide.md", 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content)
