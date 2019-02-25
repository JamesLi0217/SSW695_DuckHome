import requests
import json
import xmltodict


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
    address = validformat(address)
    city = validformat(city)
    url = f'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={zwsid}&address={address}&citystatezip={city}%2C+{state}'
    r = requests.get(url)
    #print(r.text)
    return r.text

def validformat(string): # replace the ' ' with '-'
    return ('-').join(string.split())


# google geocoding API

#according to the latitude and longitude, return the specific address.
def get_address(lat, lng):
    gid = 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={str(lat)},{str(lng)}&location_type=ROOFTOP&result_type=street_address&key={gid}'
    r = requests.get(url)
    print(r.text)
#xmlstr = get_neighborhood('NJ')
xmlstr = get_search_result('333 River St', 'Hoboken', 'NJ')
jsonstr = xml_to_json(xmlstr)
#get_address(-75.09575530499995,39.946575858000074)