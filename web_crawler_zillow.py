from bs4 import BeautifulSoup as bs
import requests

city_dict = {'Hoboken': 'Hoboken-NJ_rb', 'Jersey city': 'Jersey-city-NJ_rb', 'Union city': 'Union-city-NJ_rb'}

pre_url = 'https://www.zillow.com/homes/'

def get_data(city_dict): #get data from zillow for rent part, url consist of pre_url and items in city_dict
    for city, suffix in city_dict.items():
        url = pre_url + suffix
        print(url)

        html = requests.get(url).text
        print(html)
        soup = bs(html, 'lxml')
        pic_list = soup.find_all(class_ = 'photo-cards')
        print(pic_list[0])
        break

get_data(city_dict)