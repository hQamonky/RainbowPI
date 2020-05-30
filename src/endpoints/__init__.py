import json

import markdown
import os
import atexit
import RPi.GPIO as GPIO

# Import the framework
from flask import Flask
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)

# Set GPIO pins
RED = 17
GREEN = 22
BLUE = 24

# Initiate GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)


def save_rgb(r, g, b):
    with open('./src/endpoints/rgb.json') as json_file:
        rgb = json.load(json_file)
    rgb['red'] = r
    rgb['green'] = g
    rgb['blue'] = b
    with open('./src/configuration.json', 'w') as outfile:
        json.dump(rgb, outfile)
    return rgb


def get_rgb():
    with open('./src/endpoints/rgb.json') as json_file:
        rgb = json.load(json_file)
    return rgb


def save_red(r):
    with open('./src/endpoints/rgb.json') as json_file:
        rgb = json.load(json_file)
    rgb['red'] = r
    with open('./src/configuration.json', 'w') as outfile:
        json.dump(rgb, outfile)
    return rgb


def save_green(g):
    with open('./src/endpoints/rgb.json') as json_file:
        rgb = json.load(json_file)
    rgb['green'] = g
    with open('./src/configuration.json', 'w') as outfile:
        json.dump(rgb, outfile)
    return rgb


def save_blue(b):
    with open('./src/endpoints/rgb.json') as json_file:
        rgb = json.load(json_file)
    rgb['blue'] = b
    with open('./src/configuration.json', 'w') as outfile:
        json.dump(rgb, outfile)
    return rgb


def set_rgb(r, g, b):
    GPIO.output(RED, int(r))
    GPIO.output(GREEN, int(g))
    GPIO.output(BLUE, int(b))
    save_rgb(r, g, b)


def set_red(r):
    GPIO.output(RED, int(r))
    save_red(r)


def set_green(g):
    GPIO.output(GREEN, int(g))
    save_green(g)


def set_blue(b):
    GPIO.output(BLUE, int(b))
    save_blue(b)


def turn_on():
    rgb = get_rgb()
    set_rgb(rgb['red'], rgb['green'], rgb['blue'])


def turn_off():
    GPIO.output(RED, 0)
    GPIO.output(GREEN, 0)
    GPIO.output(BLUE, 0)
    GPIO.cleanup()


atexit.register(lambda: turn_off())

turn_on()


# Endpoints ------------------------------------------------------------------------------------------------------------


# Route shows the user guide file.
@app.route('/')
def index():
    # Open file
    with open(os.path.dirname(app.root_path) + "/../docs/API User Guide.md", 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()
        # Convert to HTML
        return markdown.markdown(content)


class On(Resource):
    @staticmethod
    def get():
        turn_on()
        rgb = get_rgb()
        return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}


class Off(Resource):
    @staticmethod
    def get():
        GPIO.output(RED, 0)
        GPIO.output(GREEN, 0)
        GPIO.output(BLUE, 0)
        return "Turned off"


class RGB(Resource):
    @staticmethod
    def get():
        rgb = get_rgb()
        return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('red', required=True)
        parser.add_argument('green', required=True)
        parser.add_argument('blue', required=True)
        args = parser.parse_args()
        set_rgb(args.red, args.green, args.blue)
        return {"red": args.red, "green": args.green, "blue": args.blue}


class GetRed(Resource):
    @staticmethod
    def get():
        return get_rgb()['red']


class SetRed(Resource):
    @staticmethod
    def get(value):
        set_red(value)
        return get_rgb()


class GetGreen(Resource):
    @staticmethod
    def get():
        return get_rgb()['green']


class SetGreen(Resource):
    @staticmethod
    def get(value):
        set_green(value)
        return get_rgb()


class GetBlue(Resource):
    @staticmethod
    def get():
        return get_rgb()['blue']


class SetBlue(Resource):
    @staticmethod
    def get(value):
        set_blue(value)
        return get_rgb()


api.add_resource(On, '/on')
api.add_resource(Off, '/off')
api.add_resource(RGB, '/rgb')
api.add_resource(GetRed, '/red')
api.add_resource(SetRed, '/red/<value>')
api.add_resource(GetGreen, '/green')
api.add_resource(SetGreen, '/green/<value>')
api.add_resource(GetBlue, '/blue')
api.add_resource(SetBlue, '/blue/<value>')
