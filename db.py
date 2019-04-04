from pymongo import MongoClient
from gridfs import *
import time
from api_key import google_keys
from api import get_coordinate
import random
from bson import ObjectId
import pandas as pd
import numpy as np
from scipy.integrate import simps
from numpy import trapz
from sklearn.externals import joblib




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
def add_apartment_by_userID(apartment_info, user_id):
    for key, value in apartment_info.items():
        if not value:
            return {'success': False, 'desc': f'The key of {key} is empty'}

    #print(db.users.find_one({'_id': ObjectId('5c86bace0840c437cf3d6938')}))

    if not db.users.find_one({'_id': ObjectId(user_id)}):
        return {'success': False, 'desc': f"Didn't find the user_id {user_id} in users Database"}

    address, city, state = apartment_info['address'], apartment_info['city'], apartment_info['state']
    postal_code, bed, bath = apartment_info['postal_code'], apartment_info['bed'], apartment_info['bath']
    sqft, price, title = apartment_info['sqft'], apartment_info['price'], apartment_info['title']
    location = ' '.join([address, city, state, postal_code])
    #print(location)
    apartments = db.apartment_list.find({'location': location})
    #print(apartments)
    try:
        info_dict = {
            "bed": float(bed),
            'price': float(price),
            'bath': float(bath),
            'sqft': float(sqft),
            'user_id': user_id
        }
    except ValueError:
        return {'success': False, 'desc': 'bed, price, bath, sqft should be numeral values'}
    apart_list = list(apartments)
    if apart_list: #have this location in tht database
        print('go inside the apartments')
        for apartment in apart_list: # check the info list
            print(apartment)
            for info in apartment['info']:
                if info_dict.__eq__(info): # already has this type of feature
                    print('already have a same one')
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
        print('add a new set in database')
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
        print(apartment_info)
        result = db.apartment_list.insert_one(apartment_info)
        new_id = result.inserted_id
        new_apart = db.apartment_list.find_one({'_id': new_id})
        if not new_apart:
            return {'success': False, 'desc': "Can't insert for some reason."}
        else:
            return {'success': True, 'data': new_apart}

def get_apartment_by_userID(user_id):
    if not user_id:
        return {'success': False, 'desc': 'The user ID is empty'}

    apartments = db.apartment_list.find()
    apart_list = list(apartments)
    res = []

    for apart in apart_list:
        user_apart = apart
        apart_info = apart['info'][:]
        user_apart['info'] = []

        for info in apart_info:
            if str(info['user_id']) == user_id:
                user_apart['info'].append(info)

        if len(user_apart['info']) > 0:
            res.append(user_apart)

    print(res)
    if len(res) == 0:
        return {'success': False, 'desc': f"Didn't find the matched apartment with the user id: {user_id}"}
    else:
        return {'success': True, 'data': res}

def delete_apart_by_userid(apartment_info, user_id):
    for key, value in apartment_info.items():
        if not value:
            return {'success': False, 'desc': f'The key of {key} is empty'}

    if not db.users.find_one({'_id': ObjectId(user_id)}):
        return {'success': False, 'desc': f"Didn't find the user_id {user_id} in users Database"}

    address, city, state = apartment_info['address'], apartment_info['city'], apartment_info['state']
    postal_code, bed, bath = apartment_info['postal_code'], apartment_info['bed'], apartment_info['bath']
    sqft, price, title = apartment_info['sqft'], apartment_info['price'], apartment_info['title']
    location = ' '.join([address, city, state, postal_code])

    apartments = db.apartment_list.find({'location': location})

    try:
        info_dict = {
            "bed": float(bed),
            'price': float(price),
            'bath': float(bath),
            'sqft': float(sqft),
            'user_id': user_id
        }
    except ValueError:
        return {'success': False, 'desc': 'bed, price, bath, sqft should be numeral values'}
    apart_list = list(apartments)

    if apart_list: #find this location in database
        for i, apartment in enumerate(apart_list):
            #print(apartment)
            _id = apartment['_id']
            if len(apartment['info']) == 1 and info_dict.__eq__(apartment['info'][0]): #if len of info == 1 and match the delete item. Remove it
                apart_list.pop(i)
                print('Delete whole list:')
                res = db.apartment_list.delete_one({'_id': _id})
                if res.deleted_count == 1:
                    return {'success': True, 'desc': f'Delete an apartment info:{_id} successfully'}
                else:
                    return {'success': False, 'desc': "Didn't delete successfully"}
            else:
                for j, info in enumerate(apartment['info']):
                    if info_dict.__eq__(info): #if find the matched info in the apartment
                        info.pop(j)
                        print('Delete one item:')
                        res = db.apartment_list.update_one({'_id': _id}, {'$set': {'info': info}})
                        if res.modified_count == 1:
                            return {'success': True, 'desc': f'Delete an item in apartment:{_id} successfully'}
                        else:
                            return {'success': False, 'desc': "Didn't delete successfully"}

        return {'success': False, 'desc': "Didn't find the matched info in the database"}

    else:
        return {'success': False, 'desc': "Did't find this address of apartment in database"}

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

def predict_post_price(info, pkl_path):
    try:
        bed, bath, sqft, city = info['bed'], info['bath'], info['sqft'], info['city'].lower()
        min, max = 180, 5000
        sqft = (sqft - min) / (max - min)  #normalization of sqft

        dict = {
            'bed': bed,
            'bath': bath,
            'hoboken': 0,
            'jersey city': 0,
            'union city': 0,
            'sqft': sqft
        }

        dict[city] = 1
        # print(dict)

        res = [dict['bed'], dict['bath'], dict['hoboken'], dict['jersey city'], dict['union city'], dict['sqft']]
        a = np.array(res)

        # print(a)

        model = joblib.load(pkl_path)
        pred_price = model.predict([a])
        pred_price = np.round(pred_price[0], 0)
        return {'success': True, 'data': pred_price}

    except Exception as e:
        return {'success': False, 'desc': e}

def update_recommendation():
    apart_list = list(db.apartment_list.find())
    for apart in apart_list:
        _id = apart['_id']

        for ct in ['hoboken', 'jersey city', 'union city']:
            if ct in apart['location'].lower():
                city = ct

        print(apart['location'])

        for info in apart['info']:
            bed, bath, sqft = info['bed'], info['bath'], info['sqft']
            min, max = 180, 5000
            sqft = (sqft - min)/(max - min)

            dict = {
                'bed': bed,
                'bath': bath,
                'hoboken': 0,
                'jersey city': 0,
                'union city': 0,
                'sqft': sqft
            }

            dict[city] = 1
            #print(dict)
            res = [dict['bed'], dict['bath'], dict['hoboken'], dict['jersey city'], dict['union city'], dict['sqft']]
            a = np.array(res)
            #print(a)
            model = joblib.load('/Users/franklin/SSW695/SSW695_DuckHome/build_model/SGDRegression_model.pkl')
            pred_price = model.predict([a])
            pred_price = np.round(pred_price[0], 0)
            print(pred_price)
            price = info['price']

            if price <= pred_price:
                recommend = True
            else:
                recommend = False
            print(recommend)
            info['recommend'] = recommend

        res = db.apartment_list.update_one({'_id': _id}, {'$set': {'info': apart['info']}})
        if res.modified_count == 0:
            return {'success': False, 'desc': f"Didn't update recommendation when _id: {_id}"}

    # return {'success': True, 'desc': 'Completed'}

# calculate money saved
def chart_calculus(city, start_date):
    p = [i.capitalize() for i in city.split()]
    city = ''.join(p)

    path = f'/Users/franklin/SSW695/SSW695_DuckHome/build_model/{city}_result_long.csv'
    try:
        df = pd.read_csv(path).tail(24)
        array = list(df[df['index'] >= start_date]['price'])

    except:
        return {'success': False, 'desc': f'Failed to read {path}.'}

    y = array
    start_price = y[0]
    new_y = [(array[i] - start_price) for i in range(len(y))]

    # get the slope
    if new_y[1] - new_y[0] >= 0:
        signal = 1
    else:
        signal = -1

    pre_area = 0
    for i in range(1, len(new_y)):
        # Compute the area using the composite trapezoidal rule.
        area = trapz(new_y[0:i+1], dx=1)
        if pre_area * area < 0: # area=0 between last i and i
            if i <= 6:  # if it less than 6 months, it should be short-term rental.
                if new_y[i] > 0 or (new_y[i] == 0 and signal == 1):
                    return {'success': True, 'desc': 'recommended for 6< months rental.'}
                elif new_y[i] < 0 or (new_y[i] == 0 and signal == -1):
                    return {'success': True, 'desc': 'recommended for short-term rental (less than 6 months).'}
                else:
                    return {'success': False, 'desc': 'Failed to calculate.'}

            elif 6 < i <= 12:
                if new_y[i] > 0 or (new_y[i] == 0 and signal == 1):
                    return {'success': True, 'desc': f'recommended for {int(i)}-{int(i)+2} months rental.'}
                elif new_y[i] < 0 or (new_y[i] == 0 and signal == -1):
                    return {'success': True, 'desc': f'recommended for <={int(i)} months rental (unrecommended for any'
                                                     ' longer rental).'}
            else:
                if new_y[i] > 0 or (new_y[i] == 0 and signal == 1):
                    return {'success': True, 'desc': f'recommended for {int(i)}-{int(i)+2} months rental.'}
                elif new_y[i] < 0 or (new_y[i] == 0 and signal == -1):
                    return {'success': True, 'desc': f'recommended for <={int(i)} months rental (unrecommended for any'
                                                     ' longer rental).'}
                else:
                    return {'success': False, 'desc': 'Failed to calculate.'}

        pre_area = area

    else:
        if signal == -1:
            return {'success': True, 'desc': 'recommended for short-term rental (less than 6 months).'}
        else:
            return {'success': True, 'desc': 'recommended for long-term rental (2 years).'}





if __name__ == '__main__':
    apartment_info = {
        'address': '20 River Ct',
        'city': 'Jersey city',
        'state': 'NJ',
        'postal_code': '07310',
        'bed': 2,
        'bath': 2,
        'sqft': 1200,
        'price': 3900,
        'title': 'Apartment for rent'
    }
    user_id = "5c86bace0840c437cf3d6938"
    #new_apart = add_apartment_by_userID(apartment_info, user_id)
    #print(new_apart)
    #apart = get_apartment_by_userID("5c86bace0840c437cf3d697d")
    #print(len(apart['data']))
    #res = delete_apart_by_userid(apartment_info, user_id)
    #print(res)
    # a = predict_post_price(apartment_info, '/Users/franklin/SSW695/SSW695_DuckHome/build_model/SGDRegression_model.pkl')
    # print(a)
    #update_recommendation()

    res = chart_calculus('Jersey City', '2019-06-01')
    print(res)
