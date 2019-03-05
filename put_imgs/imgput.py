from pymongo import MongoClient
from gridfs import *
import requests

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
# Connect collection
fs = GridFS(db, collection="imgs")

# Get image urls
f = open("img_url.csv", 'r')
for line in f.readlines():
    line_list = line.replace('\n', '').split(',')
    zpid = line_list[0]
    url = line_list[1]
    dic = {
        'zpid': zpid,
        'url': url
    }
    # print(zpid, url)

    if url == 'None':
        continue

    data = requests.get(url, timeout=100).content

    if not fs.find_one({"url": url}):
        fs.put(data, **dic)

f.close()

