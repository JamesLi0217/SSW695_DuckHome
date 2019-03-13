from pymongo import MongoClient
from gridfs import *
import time
from api_key import google_keys
from api import get_coordinate
import random
# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase


def filter_apartments(filters):
    # filter include: city, min_price, max_price, beds, baths, min_sqft, max_sqft
    # filter the price of the apartments in the list
    city = filters['city']
    min_price, max_price = filters['min_price'], filters['max_price']
    bed, bath = filters['bed'], filters['bath']
    min_sqft, max_sqft = filters['min_sqft'], filters['max_sqft']
    cond = {}
    if city:
        cond['city'] = city

    if min_price:
        if 'info.price' in cond.keys():
            cond['info.price']['$gte'] = min_price
        else:
            cond['info.price'] = {'$gte': min_price}

    if max_price:
        if 'info.price' in cond.keys():
            cond['info.price']['$lte'] = max_price
        else:
            cond['info.price'] = {'$lte': max_price}

    if bed:
        cond['info.bed'] = bed

    if bath:
        cond['info.bath'] = bath

    if min_sqft:
        if 'info.sqft' in cond.keys():
            cond['info.sqft']['$gte'] = min_sqft
        else:
            cond['info.sqft'] = {'$gte': min_sqft}

    if max_price:
        if 'info,sqft' in cond.keys():
            cond['info.sqft']['$lte'] = max_sqft
        else:
            cond['info.sqft'] = {'$lte': max_sqft}

    result = db.apartment_list.find(
        cond
    )
    res_list = list(result)

    if len(res_list) == 0:
        return {'success': False, 'desc': "can't find any apartment as filters in database"}
    else:
        return {'success': True, 'data': res_list}


# Get apartment list from homepage city filter
def get_list_city(city):
    """
    Finds and returns apartment list by city.
    Returns a list of dictionaries, each dictionary contains apartment info except  _id.
    Apartment info contains
    """
    try:
        result_city = list(db.apartment_list.find({"city": city}, {"_id": 0}).limit(1))

        if len(result_city) == 0:
            return {'success': False, 'desc': "can't find any apartment as filters in database"}
        else:
            return {'success': True, 'data': result_city}

    except Exception as e:
        return e


# Get image binary data by zpid
def get_img(zpid):
    fs = GridFS(db, collection="imgs")
    for grid_out in fs.find({'zpid': zpid}, no_cursor_timeout=True):
        img_data = grid_out.read()
        if len(img_data) == 0:
            return {'success': False, 'desc': "can't find any images by this zpid in database"}
        else:
            return {'success': True, 'data': img_data}


def add_user(user_info):
    name = user_info['name']
    email = user_info['email']
    pwd = user_info['password']
    mobile = user_info['mobile']
    gender = user_info['gender']
    tag = user_info['tag']

    # Connect to the collection users
    users = db.users

    # Add a new user to the collection
    users.insert_one(user_info)

# apartment_info: address, city, state, postal_code, bed, bath, sqft, price, title
def add_apartment(apartment_info, user_id):
    for key, value in apartment_info.items():
        if not value:
            return {'success': False, 'desc': f'The key of {key} is empty'}

    if not db.users.find_one({'_id': user_id}):
        return {'success': False, 'desc': f"Didn't find the user_id {user_id}in users Database"}

    address, city, state = apartment_info['address'], apartment_info['city'], apartment_info['state']
    postal_code, bed, bath = apartment_info['postal_code'], apartment_info['bed'], apartment_info['bath']
    sqft, price, title = apartment_info['sqft'], apartment_info['price'], apartment_info['title']
    location = ' '.join([address, city, state, postal_code])
    apartment = db.apartment_list.find({'location': location})

    try:
        info_dict = {
            "bed": float(bed),
            'price': float(price),
            'bath': float(bath),
            'sqft': float(sqft)
        }
    except ValueError:
        return {'success': False, 'desc': 'bed, price, bath, sqft should be numeral values'}

    if apartment: #have this location in tht database
        for info in apartment['info']: # check the info list
            if info_dict.__eq__(info): # already has this type of feature
                return {'success': False, 'desc': f'Already has this type of features under the location:{location}'}
        else:
            info_list = apartment['info']
            info_list.append(info_dict)
            result = db.apartment_list.update_one({'location': location}, {'$set': {'info': info_list}})
            if result.nUpserted == 1:
                return {'success': True, 'desc': f'Updated one new info under the location of {location}'}
            else:
                return {'success': False, 'desc': "Didn't update anything"}
    else: # a new apartment address added
        api_pool = google_keys()
        key = random.choice(api_pool)
        lat, lng = get_coordinate(address, key)

        apartment_info = {
            'zpid': time.time(),
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'info': [info_dict],
            'location': location,
            'property_url': '',
            'title': title,
            'coordinates': {
                'lat': lat,
                'lng': lng
            }
        }


def add_img_by_zpid(img, zpid):
    fs = GridFS(db, collection="imgs")
    dic = {
        'zpid': zpid,
        'url': 'Local data'
    }
    if not fs.find_one({"zpid": zpid}):
        fs.put(img, **dic)
        return {'success': True, 'desc': 'Image added successfully'}
    else:
        return {'success': False, 'desc': f'Already have an images under the zpid of {zpid}'}

def delete_img_by_zpid(zpid):
    fs = GridFS(db, collection='imgs')
    img = fs.find_one({"zpid": zpid})
    if not img:
        return {'success': False, 'desc': f"Didn't find zpid of {zpid} in the Database"}
    file_id = img['_id']
    fs.delete(file_id)
    return {'success': True, 'desc': f'Delete the image under the zpid of {zpid} successfully'}

if __name__ == '__main__':
    filters = {
        'city': 'Hoboken',
        'min_price': 0,
        'max_price': 2000,
        'bed': 1,
        'bath': 1,
        'min_sqft': 0,
        'max_sqft': 1500
    }
    res = filter_apartments(filters)
    if res['success'] is True:
        for item in res['data']:
            print(item['location'])
    else:
        print(res['desc'])

    # test function get_list_city()
    result_city = get_list_city('Hoboken')
    if result_city['success'] is True:
        for i in result_city['data']:
            print(i['zpid'])

    # # test function get_img(zpid)
    for i in result_city['data']:
        zpid = i['zpid']
        print(type(zpid))
        img_data = get_img(zpid)
        if img_data['success'] is True:
            img = open(str(zpid) + '.jpg', 'wb')
            img.write(img_data['data'])
            img.close()


    # for i in db.apartment_list.find().limit(2):
    #     print(type(i))
    #     print(i)
    #
    #     db.apartment_list.update({'_id': i['_id']}, {'$set': {'user_id': 'xxxxxxx'}})