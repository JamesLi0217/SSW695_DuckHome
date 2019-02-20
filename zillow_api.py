import requests
import json
import xmltodict

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

def get_search_result(address, city, state):
    zwsid = "X1-ZWz1gw8rzyrfgr_4lr3d"
    address = validformat(address)
    city = validformat(city)
    url = f'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={zwsid}&address={address}&citystatezip={city}%2C+{state}'
    r = requests.get(url)
    #print(r.text)
    return r.text

def validformat(string): # replace the ' ' with '-'
    return ('-').join(string.split())
#xmlstr = get_neighborhood('NJ')
xmlstr = get_search_result('20+River+Ct', 'Jersey+city', 'NJ')
jsonstr = xml_to_json(xmlstr)
