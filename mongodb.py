from pymongo import MongoClient
import json
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["pag2"]
collection = db["months"]


for year in range(1):
    folder_path = fr"C:\Users\filo1\Desktop\szkola_sem5\PAG2\jsony_proj2\wojewodztwa\geojson_woj\2014"
    for filename in os.listdir(folder_path):
        if filename.endswith(".geojson"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    collection.insert_one(data)
                print(f"Zaimportowano {filename}")
            except Exception as e:
                print(f"Błąd przy imporcie {filename}: {e}")