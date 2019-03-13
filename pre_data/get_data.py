from pymongo import MongoClient
import csv
import codecs

# Connect mongodb
client = MongoClient('127.0.0.1', 27017)
# Connect database
db = client.duckbase
# Connect collection
apartments = db.apartment_list

# Search the database
cursor = apartments.find()

# Open CSV file
with codecs.open('raw_data.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write column_names
    writer.writerow(['bed', 'bath', 'square', 'city', 'year_built', 'home_type', 'price'])

    # Write raw data
    for data in cursor:

        # Get city info
        if data['city'] != 'None':
            city = data['city']
        else:
            for ct in ['Hoboken', 'Jersey City', 'Union City']:
                if ct in data['location']:
                    city = ct

        factors = data.get('factors')

        # Get bed, bath, square, price info
        for i in data['info']:
            bed = i['bed']
            bath = i['bath']
            square = i['sqft']
            price = i['price']

            if factors:
                home_info = factors.get('homeInfo')
                if home_info:
                    # Get yearBuilt homeType info
                    year_built = home_info.get('yearBuilt')
                    home_type = home_info.get('homeType')

                    # Write all info
                    writer.writerow([bed, bath, square, city, year_built, home_type, price])

                else:
                    writer.writerow([bed, bath, square, city, None, None, price])
            else:
                writer.writerow([bed, bath, square, city, None, None, price])
