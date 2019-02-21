from bs4 import BeautifulSoup as bs
import requests
import csv
city_dict = {'Hoboken': 'Hoboken-NJ_rb', 'Jersey city': 'Jersey-city-NJ_rb', 'Union city': 'Union-city-NJ_rb'}

pre_url = 'https://www.zillow.com/homes/for_rent/'

def get_data(city_dict): #get data from zillow for rent part, url consist of pre_url and items in city_dict
    DEFAULT_ADDRESS_NUMBER = 500
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    csvfile = open('addresslist', 'w', newline='')
    writer = csv.writer(csvfile)
    for city, suffix in city_dict.items():
        num = 0
        url = pre_url + suffix
        print(f'{city}:')
        writer.writerow([city])
        while num < DEFAULT_ADDRESS_NUMBER:
            print(url)
            html = requests.get(url, headers=headers).text
            #print(html)
            soup = bs(html, 'lxml')
            address_list = soup.find_all(class_ = 'zsg-photo-card-address')
            for address in address_list:
                num += 1
                print(address.text)
                writer.writerow([address.text, url])
                if num == DEFAULT_ADDRESS_NUMBER: #first DEFAULT_ADDRESS_NUMBER address each city
                    break

            if num < DEFAULT_ADDRESS_NUMBER:
                next = soup.find(class_ = 'zsg-pagination-next')
                if not next:
                    break
                url = 'https://www.zillow.com/' + next.a.get('href')


get_data(city_dict)