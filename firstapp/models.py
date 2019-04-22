from django.db import models
from mongoengine import *
# Create your models here.

connect('duckbase', host='127.0.0.1', port=27017)

class Apartment_list(Document):
    zpid = StringField()
    desc = StringField()
    address = StringField()
    factors = ListField()
    info = ListField()
    coordinates = StringField()
    city = StringField()
    state = StringField()
    postal_code = StringField()
    location = StringField()
    property_url = StringField()
    title = StringField()
    meta = {'collection' : 'apartment_list'}

