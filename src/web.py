from flask import Flask, request, jsonify
import os
import config

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_current_info():
    file_size = os.path.getsize(config.file_path)

    return jsonify({
        'file_size': str(round(file_size / 1024 / 1024)) + 'MB'
    })


def runServer():
    app.run('0.0.0.0', 8000)
