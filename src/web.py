import h5py
from flask import Flask, send_from_directory, render_template_string
import os
import config

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_current_info():
    file_size = os.path.getsize(config.file_path)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File</title>
    </head>
    <body>
        <p>File size: {{filesize}}MB</p>
    </body>
    </html>
    """
    # <form action="/download" method="get">
    # <button type="submit">Download</button>
# </form>
    return render_template_string(html, filesize=str(round(file_size / 1024 / 1024)))





# @app.route('/download')
# def download_file():
#     compress_data()
#     return send_from_directory('../datasets/', 'compressed_data.h5', as_attachment=True)


def runServer():
    app.run('0.0.0.0', 8000)
