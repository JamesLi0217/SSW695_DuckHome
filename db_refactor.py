from pymongo import MongoClient
import random

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
apartment_list = db.apartment_list
users = db.users
# Connect collection

def refactor_user():
    apart_list = list(apartment_list.find())
    for apartment in apart_list:
        _id = apartment['_id']
        users_list = list(users.find())
        user_num = len(users_list)
        random_pos = random.randint(0, user_num - 1)
        user = users_list[random_pos]
        #print(user['_id'])
        apartment_list.update_one({'_id': _id}, {'$set': {'user_id': user['_id']}})

def refactor_bath_sqft():
    apart_list = list(apartment_list.find())
    for apartment in apart_list:
        _id = apartment['_id']
        print(apartment['info'])
        for info in apartment['info']:
            bed = info['bed']
            if info['bath'] is None:
                if bed == 0:
                    info['bath'] = 1.0
                if bed == 1:
                    info['bath'] = 1.0
                if bed == 2:
                    info['bath'] = 1.5
                if bed == 3:
                    info['bath'] = 1.5
                if bed == 4:
                    info['bath'] = 2.0
                if bed == 5:
                    info['bath'] = 3.0

            if info['sqft'] is None:
                if bed == 0:
                    info['sqft'] = 640.0
                if bed == 1:
                    info['sqft'] = 733.0
                if bed == 2:
                    info['sqft'] = 1006.0
                if bed == 3:
                    info['sqft'] = 1423.0
                if bed == 4:
                    info['sqft'] = 1654.0
                if bed == 5:
                    info['sqft'] = 3723.0
        print(apartment['info'])
        apartment_list.update_one({'_id': _id}, {'$set': {'info': apartment['info']}})

refactor_bath_sqft()
refactor_user()
