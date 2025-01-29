import requests, io, zipfile
import geopandas as gpd
import pyproj
from conect_redis import r
import json

def download_single_zip(URL: str, directory: str) -> None:
    try:
        r = requests.get('S/getfiledown/Arch/Telemetria/Meteo/2024/Meteo_2024-01.zip')
        zip_file = zipfile.ZipFile(io.BytesIO(r.content))
        zip_file.extractall(directory)
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"Request error: {err}")
    except zipfile.BadZipFile as err:
        raise SystemExit(f"Bad zip file error: {err}")
    
def translate_to_4326(coords: tuple) -> list:
    proj_2180 = pyproj.CRS.from_epsg(2180)
    proj_4326 = pyproj.CRS.from_epsg(4326)
    transformer = pyproj.Transformer.from_crs(proj_2180, proj_4326)
    x, y = coords
    lat, lng = transformer.transform(y, x)
    return [lat, lng]

def get_stations_coords(geojson_path: str = r'dane\effacility.geojson'):
    gdf = gpd.read_file(geojson_path)
    additionals = gdf['additional'].unique()
    additionals = ["Regionalna Stacja Hydrologiczno-Meteorologiczna", "Stacja hydrologiczno-meteorologiczna I rzędu", "Automatyczna Stacja Synoptyczna"]
    gdf = gdf[gdf['additional'].isin(additionals)]
    gdf: gpd.GeoDataFrame
    stations_dict = gdf[['ifcid', 'geometry', 'additional', 'name1', 'activitype']].set_index('ifcid').to_dict('index')
    coordinates_dict = {
        ifcid: {
            "lat" : translate_to_4326(geom.coords[0])[0],
            "lng" : translate_to_4326(geom.coords[0])[1],
            "type": type, 
            "name": name1,
            "activitype": str(activitype).split()[0]
        } 
        for ifcid, data in stations_dict.items() 
        for geom, type, name1, activitype in [(data['geometry'], data['additional'], data['name1'], data['activitype'])]
    }
    return coordinates_dict

def convert_to_geojson(data):
    features = []
    for station_id, props in data.items():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [props['lng'], props['lat']]
            },
            "properties": {
                "id": station_id,
                "name": props['name'],
                "type": props['type'],
                "activitype": props['activitype']
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson 
   
def main():
    data = get_stations_coords()
    data_geojson = convert_to_geojson(data)
    with open('stations_geo.geojson', 'w') as f:
        json.dump(data_geojson, f, indent=4)

    r.json().set('stations_coords', '$', data_geojson)

if __name__ == "__main__":
    main()