import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Job:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = int(os.getenv("MONGO_PORT"))
        self._client = MongoClient(mongo_host, mongo_port)
        self._db = self._client['jobs_db']
        self._jobs = self._db['jobs']

    def insert(self, id: str, filename: str):
        self._jobs.insert_one({
            '_id': id, 
            'status': 'downloading', 
            'result': '', 
            'filename': filename,
            'timestamp': datetime.utcnow()
        })

    def update(self, id:str, content: dict, ):
        self._jobs.update_one({'_id': id}, {'$set': content})

    def find(self, id:str):
        return self._jobs.find_one({'_id': id})
    
    def find_by(self, condition: dict, **kwargs):
        return self._jobs.find_one(condition, **kwargs)
    
    def list(self):
        return self._jobs.find().sort('timestamp', -1)