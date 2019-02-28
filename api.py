import requests
import json
import xmltodict
import random

#Zillow API
def get_neighborhood(state):
    zwsid = "X1-ZWz1gw8rzyrfgr_4lr3d"
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
    zwsid = "X1-ZWz1gw8rzyrfgr_4lr3d"
    address = zillow_validformat(address)
    city = zillow_validformat(city)
    url = f'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={zwsid}&address={address}&citystatezip={city}%2C+{state}'
    r = requests.get(url)
    #print(r.text)
    return r.text

def zillow_validformat(string): # replace the ' ' with '-'
    #print(('-').join(string.replace(',', ' ').split()))
    return ('-').join(string.replace(',', ' ').split())


# google geocoding API
def google_validformat(string):
    return '+'.join(string.strip().replace('#', '').split())

#according to the latitude and longitude, return the specific address.
def get_address(lat, lng):
    gid = 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={str(lat)},{str(lng)}&location_type=ROOFTOP&result_type=street_address&key={gid}'
    r = requests.get(url)
    res_json = json.loads(r.text)
    print(res_json)

#aquire coordinate info with Google API
def get_coordinate(addr, gid):
    #'AIzaSyCC9JC6uRITBWXydnWLrDk8j2Fl5ECshPU', 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI',
    #'AIzaSyDaUwm7EEMzsy-h9hSkOxnYedJ3CRnhclw'
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


#xmlstr = get_neighborhood('NJ')
# xmlstr = get_search_result('333 River St', 'Hoboken', 'NJ')
# jsonstr = xml_to_json(xmlstr)
coordinate_x, coordinate_y = get_coordinate('The Junction, Unit 106', 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI')
print(coordinate_x, coordinate_y)
