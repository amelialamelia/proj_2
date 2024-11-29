import requests, zipfile, io  
import datetime
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import re

wojewodztwa = gpd.read_file(r"C:\Studia\semestr_5\programowanie_aplikacji_geoinformacyjnych_2\cwiczenia\projekt_2\Dane\woj.shp")

stacje = gpd.read_file(r"C:\Studia\semestr_5\programowanie_aplikacji_geoinformacyjnych_2\cwiczenia\projekt_2\Dane\effacility.geojson")

file = requests.get("https://danepubliczne.imgw.pl/datastore/getfiledown/Arch/Telemetria/Meteo/2024/Meteo_2024-02.zip") 
zip = zipfile.ZipFile(io.BytesIO(file.content)) 
zip.extractall(R"C:\Studia\semestr_5\programowanie_aplikacji_geoinformacyjnych_2\cwiczenia\projekt_2\wyniki_request") 

give_year = "2024"
give_month = "02"
folder_path = r"C:\Studia\semestr_5\programowanie_aplikacji_geoinformacyjnych_2\cwiczenia\projekt_2\wyniki_request"
file_pattern = re.compile(r"(B\d+[AS]?)_(\d{4})_(\d{2})\.csv")

            
csv_data = {
    "air_temp": None,
    "ground_temp": None,
    "wind_direct": None,
    "av_wind_speed": None,
    "max_speed": None,
    "sum_rainfall_10": None,
    "sum_rainfall_day": None,
    "sum_rainfall_hour": None,
    "humidity": None,
    "poryw": None,
    "water_in_snow": None
}
def take_data_from_csv(folder_path):
        
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"): 
            match = file_pattern.match(file_name)
            if match:
                identifier = match.group(1)  
                year = match.group(2)       
                month = match.group(3)     
                if year == give_year and month == give_month:
                    file_path = os.path.join(folder_path, file_name)

                    if identifier == "B00300S":
                        csv_data["air_temp"] = pd.read_csv(file_path, sep=';', header=None)
                        csv_data["air_temp"].iloc[:, 3] = csv_data["air_temp"].iloc[:, 3].str.replace(',', '.').astype(float)
                        print(f"Wczytano temperature powietrza z pliku: {file_name}")
                    elif identifier == "B00305A":
                        csv_data["ground_temp"] = pd.read_csv(file_path, sep=';', header=None)
                        csv_data["ground_temp"].iloc[:, 3] = csv_data["ground_temp"].iloc[:, 3].str.replace(',', '.').astype(float)
                        print(f"Wczytano dane o temperaturze gruntu z pliku: {file_name}")
                    elif identifier == "B00202A":
                        csv_data["wind_direct"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o kierunku wiatru z pliku: {file_name}")
                    elif identifier == "B00702A":
                        csv_data["av_wind_speed"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o średniej prędkości wiatru z pliku: {file_name}")
                    elif identifier == "B00703A":
                        csv_data["max_speed"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o maksymalnej prędkości z pliku: {file_name}")
                    elif identifier == "B00608S":
                        csv_data["sum_rainfall_10"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o sumie opadów w ciągu 10min z pliku: {file_name}")
                    elif identifier == "B00604S":
                        csv_data["sum_rainfall_day"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o sumie opadów w ciągu dnia z pliku: {file_name}")
                    elif identifier == "B00606S":
                        csv_data["sum_rainfall_hour"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o sumie opadów w ciągu godziny z pliku: {file_name}")
                    elif identifier == "B00802A":
                        csv_data["humidity"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o wilgotności względem powietrza z pliku: {file_name}")
                    elif identifier == "B00714A":
                        csv_data["poryw"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o największym porywie z pliku: {file_name}")
                    elif identifier == "B00910A":
                        csv_data["water_in_snow"] = pd.read_csv(file_path, sep=';', header=None)
                        print(f"Wczytano dane o zapasie wody w śniegu z pliku: {file_name}")

def assign_wojewodztwo(stacja, wojewodztwa):
    for idx, woj in wojewodztwa.iterrows():
        if woj['geometry'].contains(stacja['geometry']):
            return woj['name']
    return None

take_data_from_csv(folder_path)


csv_data["air_temp"]['temperature'] = pd.to_numeric(csv_data["air_temp"].iloc[:, 3], errors='coerce')  
csv_data["air_temp"]['ifcid'] = csv_data["air_temp"].iloc[:, 0] 

temperature_avg = csv_data["air_temp"].groupby('ifcid')['temperature'].mean().reset_index()

#temperature_df = csv_data["air_temp"][["ifcid", "temperature"]]
#print(temperature_df.head())

#stacje_temp = stacje.merge(temperature_df, left_on="ifcid", right_on="ifcid", how="left")
stacje_temp = stacje.merge(temperature_avg, on="ifcid", how="left")
stacje_temp = stacje_temp.dropna(subset=["temperature"])
#stacje_temp = stacje_temp.dropna(subset=["temperature"])

#print(stacje_temp.head())
stacje_temp = stacje_temp.to_crs(wojewodztwa.crs)


stacje_temp["wojewodztwo"] = stacje_temp.apply(lambda row: assign_wojewodztwo(row, wojewodztwa), axis=1)

avg_temp_per_woj = stacje_temp.groupby("wojewodztwo")["temperature"].mean()
print(avg_temp_per_woj)
