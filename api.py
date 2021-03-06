import requests
import json
import xmltodict
import random
from api_key import zillow_keys, google_keys

#Zillow API
def get_neighborhood(state):
    zwsid =zillow_keys()
    url = f"http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id={zwsid}&state={state}&childtype=city"
    r = requests.get(url)
    print(r.text)
    return r.text

def xml_to_json(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = json.dumps(xmlparse, indent=1)
    print(jsonstr)
    return jsonstr

def get_search_result(address, city, state): #return XML
    zwsid = zillow_keys()
    address = zillow_validformat(address)
    city = zillow_validformat(city)
    url = f'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={zwsid}&address={address}&citystatezip={city}%2C+{state}'
    r = requests.get(url)
    #print(r.text)
    return r.text

def zillow_validformat(string): # replace the ' ' with '-'
    #print(('-').join(string.replace(',', ' ').split()))
    return '-'.join(string.replace(',', ' ').split())


# google geocoding API
def google_validformat(string):
    return '+'.join(string.strip().replace('#', '').split())

#according to the latitude and longitude, return the specific address.
def get_address(lat, lng):
    gid = random.choice(google_keys())
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={str(lat)},{str(lng)}&location_type=ROOFTOP&result_type=street_address&key={gid}'
    r = requests.get(url)
    res_json = json.loads(r.text)
    print(res_json)

#aquire coordinate info with Google API
def get_coordinate(addr, gid):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent': random.choice(user_agents)}
    valid_addr = google_validformat(addr)
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={valid_addr}&components=administrative_area:NJ|country:US&key={gid}'
    print(url)
    r = requests.get(url, headers=headers)
    #print(r.text)
    res_json = json.loads(r.text)
    if res_json['status'] == 'OK':
        #formatted_addr = res_json['results'][0]['formatted_address']
        coordinate_x = res_json['results'][0]['geometry']['location']['lat']
        coordinate_y = res_json['results'][0]['geometry']['location']['lng']
        return coordinate_x, coordinate_y
    elif res_json['status'] == 'ZERO_RESULTS':
        return 'None', 'None'
    else:
        print(res_json)
        print(f"{res_json['status']}: {res_json['error_message']}")
        return 'None', 'None'

def get_boundry(city):


    valid_city = google_validformat(city)
    # https://nominatim.openstreetmap.org/search.php?q=Warsaw+Poland&polygon_geojson=1&format=json
    url = f'https://nominatim.openstreetmap.org/search.php?q={valid_city}&polygon_geojson=1&format=json&format=geojson'
    r = requests.get(url)
    res_json = json.loads(r.text)
    boundry_set = res_json['features'][0]['geometry']['coordinates']
    with open(city.replace(' ', '') + '.txt', 'w', newline='') as f:
        for set in boundry_set:
            for i in set:
                lat, lng = i[0], i[1]
                coord = {'lat': lat, 'lng': lng}
                f.write(str(coord).replace("'", '') + ',\n')

    f.close()
    print(boundry_set)

def read_coor(path1, path2):
    f1 = open(path1, 'r')
    f2 = open(path2, 'w')
    for line in f1.readlines():
        line_list = line.split()
        lat, lng = line_list[1], line_list[0]
        coord = {'lat': lat, 'lng': lng}
        f2.write(str(coord).replace("'", '') + ',\n')

    f1.close()
    f2.close()
#xmlstr = get_neighborhood('NJ')
# xmlstr = get_search_result('333 River St', 'Hoboken', 'NJ')
# jsonstr = xml_to_json(xmlstr)
#get_boundry('Union city')
read_coor('/Users/franklin/SSW695/SSW695_DuckHome/jersey_coor.txt', '/Users/franklin/SSW695/SSW695_DuckHome/Jerseycity.txt')
