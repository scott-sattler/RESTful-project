import sys
from flask import Flask, make_response, request
from flask_restful import reqparse
import pandas as pd
import json
import os


# UPLOAD_FOLDER = './static/uploads'
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'static\\uploads')
upload_folder = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# TODO: consider using color api (github below)
@app.route('/')
def get():
    """
    takes RGB values URL arguments
    :return: color name
    """
    parser = reqparse.RequestParser()
    parser.add_argument('r', required=True)
    parser.add_argument('g', required=True)
    parser.add_argument('b', required=True)
    args = parser.parse_args()  # parse arguments to dictionary

    color_name = get_color_name(int(args['r']),
                                int(args['g']),
                                int(args['b']))

    response = make_response(color_name, 200)
    response.mimetype = 'text/html'
    return response


@app.route('/store-file', methods=['POST'])
def store_file():
    parser = reqparse.RequestParser()
    parser.add_argument('ImageID', required=True)
    args = parser.parse_args()
    image_name = args['ImageID']
    file = request.files['file']

    file.save(os.path.join(app.config[upload_folder], image_name))

    return make_response('', 200)


def get_color_name(red: int, green: int, blue: int):
    col_names = ['color', 'hex', 'red', 'green', 'blue']
    df = pd.read_csv(os.path.join(app.root_path, 'static\\colors.csv'), header=None, usecols=[1, 2, 3, 4, 5], names=col_names)
    # vectorized_df = df.to_numpy ?

    # consider perceptual differences in RGB color deltas (eg blue sensitivity)
    smallest_delta = (255 * 3) + 1  # search trick
    color_name = None
    for row in df.itertuples(index=False):
        red_delta = int(row.red) - red
        green_delta = int(row.green) - green
        blue_delta = int(row.blue) - blue
        total_delta = abs(red_delta) + abs(green_delta) + abs(blue_delta)
        if total_delta < smallest_delta:
            smallest_delta = total_delta
            color_name = row.color

    return color_name


def rgb_to_hex(red: int, green: int, blue: int):
    return f'#{hex(red)[2:]:02}' \
           f'{hex(green)[2:]:02}' \
           f'{hex(blue)[2:]:02}'


def hex_to_rgb(hex_color: str):
    return (int(hex_color[1:3], 16),
            int(hex_color[3:5], 16),
            int(hex_color[5:], 16))


if __name__ == "__main__":
    path = 'C:\\Users\\Computer\\github\\microservices\\server_list.json'
    with open(path, 'r') as f:
        server_list = json.load(f)
    host = server_list['image']['host']
    port = server_list['image']['port']
    app.run(host=host, port=port, debug=True)
