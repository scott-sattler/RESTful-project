import sys
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, make_response, send_from_directory
from flask_restful import reqparse
from PIL import Image
import requests
import json

UPLOAD_FOLDER = './static/uploads'
TEMP_FOLDER = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'static\\temp')
IMG_SRC = "http://localhost/img/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # unused

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # unused
app.config['TEMP_FOLDER'] = TEMP_FOLDER  # why tho
temp_dir = 'TEMP_FOLDER'
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)  # unused


# TODO: Consolidate
def construct_address(host, port, route, args):
    """
        {host}:{port}{route}?{'&'.join(args)}

        :param str host: '172.0.0.1'
        :param str port: '5000'
        :param str route: '/store/file/here'
        :param list[str] args: ['a=b', 'c=d']
    """
    return f"http://{host}:{port}{route}?{'&'.join(args)}"


@app.route('/index.html')
def get():
    # response = render_template('index.html')
    response = """
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
    return response


@app.route('/index.html', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)  # security

    # save file to local temp folder
    # print(app.config[temp_dir])
    file.save(os.path.join(app.config[temp_dir], filename))
    file.seek(0)

    # upload to backend through gateway
    gateway_host = server_list['gateway']['host']
    gateway_port = server_list['gateway']['port']
    gateway_route = '/store-file'
    gateway_args = [f'ImageID={filename}', 'AppID=image']
    server = construct_address(gateway_host, gateway_port, gateway_route, gateway_args)
    upload_response = requests.post(server, files={'file': file})

    file.close()  # necessary?

    # return 201 created ?
    return redirect(f'/color?ImageID={filename}&Selection=None')


@app.route('/color', methods=['GET'])
def select_color():
    parser = reqparse.RequestParser()
    parser.add_argument('ImageID', required=True)
    parser.add_argument('Selection', required=True)
    args = parser.parse_args()
    image_name = args['ImageID']
    selected_color = args['Selection']

    response = make_response(
        f'''
        <!doctype html>
        <title>File Uploaded</title>
        <h1>Upload Successful</h1>
        <b>
        <p>
        current selection: {selected_color}
        </p>
        
            <a href="/id/{image_name}">
                <img src="/img/{image_name}"
                 alt="foo.bar"
                 ismap>
            </a>
        </b>
        ''')
    response.mimetype = 'text/html'
    return response


@app.route('/id/<path:image_id>', methods=['GET'])
def identify(image_id):
    parser = reqparse.RequestParser()
    x, y = map(int, request.query_string.decode().split(","))

    # get image rgb values from local temp copy
    image = Image.open(os.path.join(app.config[temp_dir], image_id))
    image_colors = image.convert('RGB')
    r, g, b = image_colors.getpixel((x, y))

    # load centralized server list
    with open(os.path.join(os.path.dirname(app.root_path), 'server_list.json'), 'r') as server_file:
        server_dict = json.load(server_file)

    # gateway color request construction
    server_id = 'gateway'
    server_info = server_dict[server_id]
    gateway_host = server_info['host']
    gateway_port = server_info['port']
    route = '/'
    args = ['AppID=image', f'ColorLookup={r},{g},{b}']
    gateway_color_request_address = construct_address(gateway_host, gateway_port, route, args)
    gateway_color_response = requests.get(gateway_color_request_address)

    response = redirect(f"/color?ImageID={image_id}&Selection={gateway_color_response.text}")

    return response


@app.route('/img/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config[temp_dir], filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    path = 'C:\\Users\\Computer\\github\\microservices\\server_list.json'
    with open(path, 'r') as f:
        server_list = json.load(f)
    host = server_list['client']['host']
    port = server_list['client']['port']
    app.run(host=host, port=port, debug=True)
