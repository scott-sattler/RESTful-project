from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
import requests
import base64
import json


app = Flask(__name__)
api = Api(app)


class Routing(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('AppID', required=True)
        parser.add_argument('ColorLookup', required=False)
        args = parser.parse_args()
        app_name = args['AppID']
        r, g, b = args['ColorLookup'].split(',')  # destructuring

        image_host = server_list[app_name]['host']
        image_port = server_list[app_name]['port']
        server = f'http://{image_host}:{image_port}'  # WARNING: hard coded

        url_with_args = f'{server}/?r={r}&g={g}&b={b}'
        request_color = requests.get(url_with_args)
        response_color = request_color.text

        return make_response(response_color, 200)


# TODO: refactor: to return image from database
class Image(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ImageID', required=True)
        parser.add_argument('location', required=False)
        args = parser.parse_args()
        image_name = args['ImageID']
        location = args['location']  # TODO WARNING: using local directory path

        path = location + '\\' + image_name

        file = open(path, "rb")
        data = file.read()
        file = base64.b64encode(data).decode()

        response = make_response(f'<img src=" data:image/jpg; base64, {file} ">')
        response.mimetype = 'text/html'
        return response


class StoreFile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ImageID', required=True)
        parser.add_argument('AppID', required=True)
        args = parser.parse_args()
        image_name = args['ImageID']
        app_name = args['AppID']
        file = request.files['file']
        filename = image_name

        # existing redirect?

        image_host = server_list[app_name]['host']
        image_port = server_list[app_name]['port']
        server = f'http://{image_host}:{image_port}/store-file?ImageID={filename}'  # WARNING: hard coded
        requests.post(server, files={'file': file})

        # route to image server for store
        return make_response('', 200)


# entry points
api.add_resource(Routing, '/')
api.add_resource(Image, '/image')
api.add_resource(StoreFile, '/store-file')

if __name__ == "__main__":
    # app.run(debug=True)                               # run Flask app
    path = 'C:\\Users\\Computer\\github\\microservices\\server_list.json'
    with open(path, 'r') as f:
        server_list = json.load(f)
    host = server_list['gateway']['host']
    port = server_list['gateway']['port']
    app.run(host=host, port=port, debug=True)
