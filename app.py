from flask import Flask, request, send_from_directory
import os
import random
import string
import json
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Gets configs
with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = config['UPLOAD_FOLDER']
app.config['SHARES_FOLDER'] = config['SHARES_FOLDER']
app.config['ALLOWED_EXTENSIONS'] = set(config['ALLOWED_EXTENSIONS'])
app.config['MAX_CONTENT_LENGTH'] = config['MAX_SIZE']
URL_PLACEHOLDER = config['URL_PLACEHOLDER']

# Makes sure that the directories do exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SHARES_FOLDER'], exist_ok=True)

# Making limits (bad method. please don't use it')
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]  # Optional global limit
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Routes the main page (index.html)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Routes the about page (about.html)
@app.route('/about')
def about():
    return send_from_directory('static', 'about.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

# Routes for the saved sites
@app.route('/shares/<code>')
def share_file(code):
    return send_from_directory(app.config['SHARES_FOLDER'], f"{code}.html")

# Limiting to 5 uploads per IP
@app.route('/upload', methods=['POST'])
@limiter.limit("5 per minute")
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):

        # Generates a code for the shared images (please don't use this')
        code = ''.join(random.choice(string.ascii_letters) for _ in range(6))

        # Makes sure if the file exists
        _, file_extension = os.path.splitext(file.filename)

        # Renaming the file to be the code
        new_filename = f"{code}{file_extension}"

        # Save the file with the new name
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        # Write to a file in the /shares directory with the new filename
        share_file_path = os.path.join(app.config['SHARES_FOLDER'], f"{code}.html")
        with open(share_file_path, "w") as share_file:
            share_file.write(
                f"""
                <!doctype html>
                <html>
                    <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <meta charset="UTF-8" />
                        <title>{code}</title>
                        <link rel="stylesheet" href="/static/style.css" />
                        <meta property="og:image" content="{URL_PLACEHOLDER}/uploads/{new_filename}" />
                    </head>
                    <body>
                        <img src="/uploads/{new_filename}" />
                        <footer>
                            <a href="/">MeowImage</a>
                        </footer>
                    </body>
                </html>
                """)

        return f"""
            <!doctype html>
            <html>
                <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <meta charset="UTF-8" />
                    <title>File uploaded!</title>
                    <link rel="stylesheet" href="/static/style.css" />
                </head>
                <body>
                    <h1>File uploaded!</h1>
                    <a class="btn" href="/shares/{code}">Here's the link</a>
                </body>
                <footer>
                    <a href="/">MeowImage</a>
                </footer>
            </html>
        """, 200

    return 'Invalid file type', 400


# Runs the website
if __name__ == '__main__':
    app.run(port=8080)
