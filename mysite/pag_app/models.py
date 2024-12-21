from django.db import models
from db_connection import mongo_db, redis_db
import json

# Create your models here.
year_collection = mongo_db["year"]
# month_collection = mongo_db["month"]

#redis
keys = redis_db.keys("stations_coords:*")
values = redis_db.json().mget(keys, '$')
stations_data = {key: value[0] for key, value in zip(keys, values)}
stations_data = json.dumps(stations_data, default=str)