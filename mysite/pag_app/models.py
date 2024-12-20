from django.db import models
from db_connection import db, redis_db
import json

# Create your models here.
person_collection = db["Person"]

#redis
keys = redis_db.keys("stations_coords:*")
values = redis_db.json().mget(keys, '$')
stations = {key: value[0] for key, value in zip(keys, values)}
stations = json.dumps(stations)