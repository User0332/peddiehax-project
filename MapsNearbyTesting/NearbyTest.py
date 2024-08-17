import googlemaps

def miles_to_meters(miles):
    '''Helper function for conversions'''
    try:
        return miles * 1609.34
    except:
        return -1
    
API_KEY = open('API_KEY.txt', 'r').read()

map_client = googlemaps.Client(API_KEY)

location = (40.31302063254212, -74.62031783336619)

distance = miles_to_meters(0.05)

place_list = []

response = map_client.places_nearby(
    location = location,
    radius = distance
)


print(response.get("status"))


place_list.extend(response["results"])

for place in place_list:
    print(
        (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]),
        place.get('name')
    )
