from django.db import models
from db_connection import mongo_db, redis_db
import json

# Create your models here.

#mongoDB
month_collection = mongo_db['months']

#redis
stations_data = redis_db.json().get('stations_coords')
stations_data = json.dumps(stations_data, default=str)