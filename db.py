from pymongo import MongoClient

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
# Connect collection

def filter_apartments(filters):
    # filter include: city, min_price, max_price, beds, baths, min_sqft, max_sqft
    # filter the price of the apartments in the list
    city = str(filters['city'])
    min_price, max_price = str(filters['min_price']), str(filters['max_price'])
    bed, bath = str(filters['bed']), str(filters['bath'])
    min_sqft, max_sqft = str(filters['min_sqft']), str(filters['max_sqft'])
    result = db.apartment_list.find(
        {'city': city},
        {'info.price': {'$gte': min_price, '$lte': max_price}},
        {'info.bed': bed},
        {'info.bath': bath},
        {'info.sqft': {'$gte': min_sqft, '$lte': max_sqft}}
    )
    for item in list(result):
        print(item)

if __name__ == '__main__':
    filters = {
        'city': 'Hoboken',
        'min_price': '500',
        'max_price': '1300',
        'bed': '2',
        'bath': '1',
        'min_sqft': '30',
        'max_sqft': '1500'
    }
    filter_apartments(filters)