from pymongo import MongoClient

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
# Connect collection

def filter_apartments(filters):
    # filter include: city, min_price, max_price, beds, baths, min_sqft, max_sqft
    # filter the price of the apartments in the list
    city = filters['city']
    min_price, max_price = filters['min_price'], filters['max_price']
    bed, bath = filters['bed'], filters['bath']
    min_sqft, max_sqft = filters['min_sqft'], filters['max_sqft']
    result = db.apartment_list.find(
        {'city': city,
        'info.price': {'$gte': min_price, '$lte': max_price},
        'info.bed': bed,
        'info.bath': bath,
        'info.sqft': {'$gte': min_sqft, '$lte': max_sqft}
        }
    )
    if len(result) == 0:
        return {'success': False, 'desc': "can't find any apartment as filters in database"}
    return {'success': True, 'data': list(result)}


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
    filter_apartments(filters)