from pymongo import MongoClient
import random

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
apartment_list = db.apartment_list
users = db.users
# Connect collection
comment_list = ['a great place to call "home". The entire staff always greet you with a smile and are very helpful to our needs, and are quick to attend to any problems that arise . The grounds and facilities are kept clean every day by friendly courteous workers. The workout rooms are open 24//7 are rarely crowded and the pool area is lovely. ',
                'This community was an extremely beautiful, well kept and peaceful community. Everything was so beautiful that I felt like I was at a resort.',
                "I have lived at a Welcome Home property for three years and it's been a great experience. The recent staff change is a major PLUS! ",
                'NEVER LIVE HERE - for the price you think you are getting will raise and you could live some where WAY nicer.']
def refactor_user():
    apart_list = list(apartment_list.find())
    for apartment in apart_list:
        _id = apartment['_id']
        for info in apartment['info']:
            users_list = list(users.find())
            user_num = len(users_list)
            random_pos = random.randint(0, user_num - 1)
            user = users_list[random_pos]
            #print(user['_id'])
            info['user_id'] = user['_id']

        apartment_list.update_one({'_id': _id}, {'$set': {'info': apartment['info']}})

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

def refactor_comment():
    apart_list = list(apartment_list.find())
    for apart in apart_list:
        _id = apart['_id']
        for info in apart['info']:
            comments = []
            users_list = list(users.find())
            user_num = len(users_list)
            random_pos = random.randint(0, user_num - 1)
            user = users_list[random_pos]
            comment = {
                'user_id': user['_id'],
                'comment': random.choice(comment_list)
            }
            comments.append(comment)
            info['comments'] = comments #{'user_id': str, 'comment': str}
            print(info['comments'])
        apartment_list.update_one({'_id': _id}, {'$set': {'info': apart['info']}})


def refactor_desc():
    apart_list = list(apartment_list.find())
    for apart in apart_list:
        _id = apart['_id']
        location = apart['location']
        desc = f'The description of {location}: \n' \
               f"All new. All yours. Contemporary style blends with the finest in history and inspiration." \
               f"Start your day in style with a spa-inspired bathroom complete with white gloss vanities, stone " \
               f"countertops and frameless glass enclosed showers. Use your kitchen's stainless steel GE appliances " \
               f"and sleek white Caesarstone countertops to bring out your inner chef. Spending the day at home? Find" \
               f" time for yourself in our state-of-the-art fitness center. Relax by the pool and the fire pits on " \
               f"the outdoor roof terrace. Work from home in the resident Internet lounge or enjoy the comfort of " \
               f"your own home. And when you re ready for an adventure, the best apartment waits just outside your " \
               f"front door."
        print(_id)
        apartment_list.update_one({'_id': _id}, {'$set': {'desc': desc}})
#refactor_bath_sqft()
#refactor_user()
#refactor_desc()
refactor_comment()
