from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

import os
import uuid
import requests
import tempfile
from urllib.parse import urlparse
from markdown import markdown

from pipeline import run_pipeline
from data_model import Job

# Connect to MongoDB
jobs = Job()

# Create FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    filename = path_parts[-1]
    return filename

def create_job(url: str, log_type: str, id: str):
    try:
        # download file
        jobs.insert(id, get_filename_from_url(url))
        #r = requests.get(url, allow_redirects=True)  ## download log file from url
        os.makedirs('tmp', exist_ok=True)
        with tempfile.NamedTemporaryFile(dir='tmp', mode='wb', delete=True) as tmp:
            #tmp.write(r.content)
            tmp.write(open(url, 'rb').read())
            filepath = tmp.name

            # execute job
            jobs.update(id, {'status': 'executing'})
            res = run_pipeline(filepath, log_type)
        # finish job
        jobs.update(id, {'status': 'finished',
                        'result': res})
    except Exception as e:
        jobs.update(id, {'status': 'failed',
                        'result': str(e)})

@app.get("/run")
async def run_summarization_chain(url: str, log_type: str, background_tasks: BackgroundTasks):
    id = str(uuid.uuid4())
    background_tasks.add_task(create_job, url, log_type, id)
    return JSONResponse(status_code=201,
                        content = {"message": "Job has been submitted", 
                                   "id": id})

@app.get("/status/{id}")
async def read_job_status(id: str):
    job = jobs.find(id)
    if job is not None:
        return {"status": job['status']}
    else:
        return HTTPException(status_code=404,
                             detail={"message": "Job id not found"})

@app.get("/result/{id}")
async def read_job_result(id: str):
    job = jobs.find(id)
    if job is not None:
        return {"result": job['result']}
    else:
        return HTTPException(status_code=404,
                             detail={"message": "Job id not found"})

@app.get("/")
async def home():
    job_list = jobs.list()
    return {"jobs": list(job_list)}

@app.get("/view/{id}", response_class=HTMLResponse)
async def view_report(request: Request, id: str):
    job = jobs.find(id)
    if job is not None:
        report_html = markdown(job['result']['report'])
        previous_job = jobs.find_by({'timestamp': {'$gt': job['timestamp']}}, sort=[('timestamp', 1)])
        next_job = jobs.find_by({'timestamp': {'$lt': job['timestamp']}}, sort=[('timestamp', -1)])

        prev_id = previous_job['_id'] if previous_job else None
        next_id = next_job['_id'] if next_job else None
        return templates.TemplateResponse(
            name="view.html", context={"request":request, 
                                       "filename": job['filename'],
                                       "report_html": report_html, 
                                       "prev_id": prev_id, 
                                       "next_id": next_id}
        )
    else:
        raise HTTPException(status_code=404, detail="Job id not found")

@app.get("/write/{id}")
async def read_job_result(id: str):
    job = jobs.find(id)
    if job is not None:
        file_name = job['filename']
        with open(f"output/{file_name}.md", 'w') as f:
            f.write(job['result']['report'])
        return {"message": "OK"}
    else:
        return HTTPException(status_code=404,
                             detail={"message": "Job id not found"})

@app.delete("/teardown")
async def delete_all(token: str):
    if token == "volvo":
        jobs._jobs.delete_many({})
        return {"message": "All documents have been deleted"}
    else:
        raise HTTPException(status_code=403, detail="Invalid token")