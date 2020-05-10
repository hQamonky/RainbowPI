import json

import markdown
import os
import pigpio
import atexit

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

pi = pigpio.pi()


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
    pi.set_PWM_dutycycle(RED, int(r))
    pi.set_PWM_dutycycle(GREEN, int(g))
    pi.set_PWM_dutycycle(BLUE, int(b))
    save_rgb(r, g, b)


def set_red(r):
    pi.set_PWM_dutycycle(RED, int(r))
    save_red(r)


def set_green(g):
    pi.set_PWM_dutycycle(GREEN, int(g))
    save_green(g)


def set_blue(b):
    pi.set_PWM_dutycycle(BLUE, int(b))
    save_blue(b)


def turn_on():
    rgb = get_rgb()
    set_rgb(rgb['red'], rgb['green'], rgb['blue'])


def turn_off():
    pi.set_PWM_dutycycle(RED, 0)
    pi.set_PWM_dutycycle(GREEN, 0)
    pi.set_PWM_dutycycle(BLUE, 0)
    pi.stop()


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


class RGB(Resource):
    @staticmethod
    def get():
        return

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


api.add_resource(RGB, '/rgb')
api.add_resource(GetRed, '/red')
api.add_resource(SetRed, '/red/<value>')
api.add_resource(GetRed, '/green')
api.add_resource(SetRed, '/green/<value>')
api.add_resource(GetRed, '/blue')
api.add_resource(SetRed, '/blue/<value>')
