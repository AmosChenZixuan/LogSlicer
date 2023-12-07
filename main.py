from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from urllib.parse import urlparse
from pymongo import MongoClient
import os
import uuid
import requests
import tempfile

from pipeline import run_pipeline

client = MongoClient('localhost', 27017)
db = client['jobs_db']
jobs = db['jobs']

app = FastAPI()

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1]
    return filename

def create_job(url: str, id: str):
    try:
        # download file
        jobs.insert_one({'_id': id, 'status': 'downloading', 'result': ''})
        #r = requests.get(url, allow_redirects=True)
        os.makedirs('tmp', exist_ok=True)
        with tempfile.NamedTemporaryFile(dir='tmp', mode='wb', delete=False) as tmp:
            #tmp.write(r.content)
            tmp.write(open(url, 'rb').read())
            filepath = tmp.name

        # execute job
        jobs.update_one({'_id': id}, {'$set': {'status': 'executing'}})
        res = run_pipeline(filepath)
        # finish job
        jobs.update_one({'_id': id}, {'$set': {'status': 'finished'}})
        jobs.update_one({'_id': id}, {'$set': {'result': res}})
    except Exception as e:
        jobs.update_one({'_id': id}, {'$set': {'status': 'failed'}})
        jobs.update_one({'_id': id}, {'$set': {'result': str(e)}})

@app.get("/summarize")
async def run_summarization_chain(url: str, background_tasks: BackgroundTasks):
    id = str(uuid.uuid4())
    background_tasks.add_task(create_job, url, id)
    return JSONResponse(status_code=201,
                        content = {"message": "Job has been submitted", 
                                   "id": id})

@app.get("/status/{id}")
async def read_job_status(id):
    job = jobs.find_one({'_id': id})
    if job is not None:
        return {"status": job['status']}
    else:
        return JSONResponse(status_code=404,
                            content = {"message": "Job id not found"})

@app.get("/result/{id}")
async def read_job_result(id):
    job = jobs.find_one({'_id': id})
    if job is not None:
        return {"result": job['result']}
    else:
        return JSONResponse(status_code=404,
                            content = {"message": "Job id not found"})

@app.get("/")
async def home():
    job_list = jobs.find()
    return {"jobs": list(job_list)}