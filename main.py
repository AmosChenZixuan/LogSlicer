from flask import Flask, jsonify, request
from flask_executor import Executor
from urllib.parse import urlparse
import os
import uuid
import requests

from pipeline import run_pipeline

app = Flask(__name__)
executor = Executor(app) # add support for background jobs

# local datastore. Should be a database instead
job_status = {}
job_result = {}

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1]
    return filename

def create_job(url, id):
    try:
        # download file
        job_status[id] = 'downloading'
        r = requests.get(url, allow_redirects=True)
        filename = get_filename_from_url(url)
        filedir = os.path.join('tmp', id)
        os.makedirs(filedir, exist_ok=True)
        filepath = os.path.join(filedir, filename)
        open(filepath, 'wb').write(r.content)
        # execute job
        job_status[id] = 'executing'
        res = run_pipeline(filepath)
        # finish job
        job_status[id] = 'finished'
        job_result[id] = res
    except Exception as e:
        job_status[id] = 'failed'
        job_result[id] = str(e)

@app.route('/summarize', methods=['GET'])
def run_summarization_chain():
    url = request.args.get('url')
    id = str(uuid.uuid4())
    executor.submit(create_job, url, id)
    return jsonify({"message": "Job started", "id": id}), 200

@app.route('/status/<id>', methods=['GET'])
def check_status(id):
    status = job_status.get(id, 'not found')
    return jsonify({"id": id, "status": status})

@app.route('/result/<id>', methods=['GET'])
def check_result(id):
    status = job_result.get(id, 'not found')
    return jsonify({"id": id, "result": status})

if __name__ == '__main__':
    app.run(port=5000)