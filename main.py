from fastapi import FastAPI, BackgroundTasks
from urllib.parse import urlparse
import os
import uuid
import requests

from pipeline import run_pipeline

app = FastAPI()

# local datastore. Should be a database instead
job_status = {}
job_result = {}

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1]
    return filename

def create_job(url: str, id: str):
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

@app.get("/summarize")
def run_summarization_chain(url: str, background_tasks: BackgroundTasks):
    id = str(uuid.uuid4())
    background_tasks.add_task(create_job, url, id)
    return {"message": "Job has been submitted", "id": id}

@app.get("/status/{id}")
def read_job_status(id):
    status = job_status.get(id, 'not found')
    return {"id": id, "status": status}

@app.get("/result/{id}")
def read_job_result(id):
    status = job_result.get(id, 'not found')
    return {"id": id, "result": status}

if __name__ == '__main__':
    app.run(port=5000)