from pymongo import MongoClient
import json
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["pag2"]
collection = db["months"]

obreby = [
    "powiaty",
    "woj"
    ]


for year in range(2014, 2019):
    folder_path = fr"C:\Users\filo1\Desktop\szkola_sem5\PAG2\jsony_proj2\json_pow_woj\json_pow_woj\{year}"
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file) 
                if isinstance(data, list):
                    collection.insert_many(data)  # Wstaw listę dokumentów
                else:
                    collection.insert_one(data)  # Wstaw pojedynczy dokument
            print(f"Zaimportowano {filename}")
