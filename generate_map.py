from math import radians, cos, sin, asin, sqrt
import folium
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable


def read_file(path: str, year: int) -> list:
    """
    Read file with locations.
    """
    with open(path, encoding='utf-8', errors='ignore') as f:
        lines_after_14 = f.read().splitlines()[14:]
    locations = [
        list(filter(lambda x: bool(x), i.split('\t')))[:2] for i in lines_after_14
    ]
    new_locations = []
    for i in locations:
        try:
            i[0] = i[0].split('"')[1:]
            i[0][1] = int(i[0][1][2:6])
            if i[0][1] == year:
                i[0].remove(i[0][1])
                i[0].append(i[1])
                new_locations.append(i[0])
        except:
            pass
    return new_locations[:200]


def distance(lat1: float, lat2: float, lon1: float, lon2: float):
    """
    Return distance between two points.
    """
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))
    r = 6371

    return c * r


def filter_by_location(lat: float, len: float, films: list) -> list:
    locations = []
    geolocator = Nominatim(user_agent='movie_map')
    for film in films:
        name, location = film[:2]
        try:
            loc = geolocator.geocode(location)
            if loc is not None:
                locations.append((name, [loc.latitude, loc.longitude]))
        except GeocoderUnavailable:
            pass
    locations.sort(key=lambda x: distance(x[1][0], lat, x[1][1], len))
    return locations[:10]


def generate_map(lat: float, lon: float, films: list):
    movie_map = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker(
        [lat, lon], popup='<strong>You are here</strong>').add_to(movie_map)
    for film in films:
        caption = '<strong>' + film[0] + '</strong>'
        folium.Marker(film[1],
                      popup=caption,
                      icon=folium.Icon(color='purple')).add_to(movie_map)
    movie_map.save('movie_map.html')
