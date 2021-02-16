import geopy
from geopy.geocoders import Nominatim
lat = 49.838261
lon = 24.023239

country = Nominatim(user_agent='movie_map').reverse((lat, lon))
print(country)
