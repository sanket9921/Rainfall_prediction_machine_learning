import requests

API_KEY = "84ab8aee3c08e48f02450cc7580714cc"


def direct_geocoding(location):
    api = "http://api.openweathermap.org/geo/1.0/direct?q=" + location + ",IN&limit=5&appid=" + API_KEY
    json_data = requests.get(api).json()
    lat_lon_list = []
    for i in range(0, len(json_data)):
        lat_lon_list.append([json_data[i]['lat'], json_data[i]['lon'], json_data[i]['state']])
    return lat_lon_list


def reverse_geocoding(lat, lon):
    api = "http://api.openweathermap.org/geo/1.0/reverse?lat=" + str(lat) + "&lon=" + str(
        lon) + "&limit=5&appid=" + API_KEY
    json_data = requests.get(api).json()
    city_list = []
    for i in range(0, len(json_data)):
        city_list.append([json_data[0]['name'], json_data[0]['state']])
    return city_list
if __name__ == '__main__':

    list = direct_geocoding('pune')
    print(list)
    print(reverse_geocoding(list[0][0], list[0][1]))
