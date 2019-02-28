from lxml import html
import requests
import random
import time
import re
import csv
from api import get_coordinate
city_dict = {'Hoboken': 'Hoboken-NJ/rentals', 'Jersey city': 'Jersey-city-NJ/rentals', 'Union city': 'Union-city-NJ/rentals'}
#city_dict = {'Jersey city': 'Jersey-city-NJ_rb'}
pre_url = 'https://www.zillow.com/'

def get_data(city_dict, file): #get data from zillow for rent part, url consist of pre_url and items in city_dict
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']

    csvfile = open(file, 'w', newline='') #open a csv file and ready to pull data
    writer = csv.writer(csvfile)
    for city, suffix in city_dict.items(): # go through the city list
        cur_page = 1
        url = pre_url + suffix #combin the url of the first page of the city
        while url: #go through each page under the city and inspect if it the last page
            headers = {'User-Agent': random.choice(user_agents)}  #randomly pick a browser to form the header
            #print(url)
            response = requests.get(url, headers=headers)
            print(f'current page is :{cur_page}')
            #print(response.text)
            parser = html.fromstring(response.text)
            search_results = parser.xpath("//div[@id='search-results']//article") #crawl all apartment info in the page
            next_suffix = parser.xpath("//li[@class='zsg-pagination-next']/a[1]/@href") #crawl the suffix of next page
            #print(next_suffix)
            if next_suffix != []:
                next_url = pre_url + next_suffix[0]
                cur_page += 1
            else:
                next_url = None
            for properties in search_results:
                raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
                raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
                raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
                raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
                raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
                raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
                raw_location = properties.xpath(".//span[@class='zsg-photo-card-address']//text()")

                link = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
                raw_title = properties.xpath(".//h4//text()")

                address = ' '.join(' '.join(raw_address).split()).replace(',', '') if raw_address else 'None'
                city = ''.join(raw_city).strip().replace(',', '') if raw_city else 'None'
                state = ''.join(raw_state).strip().replace(',', '') if raw_state else 'None'
                postal_code = ''.join(raw_postal_code).strip().replace(',', '') if raw_postal_code else 'None'
                #matchobj = re.match(r"(\$\S+)" ,''.join(raw_price).strip())
                #price = matchobj.group(1) if matchobj else 'None'
                price = ''.join(raw_price).strip().replace(',', '') if raw_price else 'None'
                #print(price)
                info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7", '').replace(',', '') #replace dot with comma
                location = raw_location[0].replace(',', '') if raw_location else 'None'
                # if location:
                #     print(f"The location is {location}")
                #     api_pool = ['AIzaSyCC9JC6uRITBWXydnWLrDk8j2Fl5ECshPU', 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI',
                #                 'AIzaSyDaUwm7EEMzsy-h9hSkOxnYedJ3CRnhclw']
                #     #AIzaSyCC9JC6uRITBWXydnWLrDk8j2Fl5ECshPU
                #     #AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI
                #     key = random.choice(api_pool)
                #     print(key)
                #     coordinate_x, coordinate_y = get_coordinate(location, key)
                #     time.sleep(random.randint(1, 3))
                # else:
                #     coordinate_x, coordinate_y = 'None', 'None'
                title = ''.join(raw_title).replace(',', '') if raw_title else 'None'
                property_url = ("https://www.zillow.com" + link[0]).replace(',', '') if link else 'None'

                # print(address)
                # print(city)
                # print(state)
                # print(postal_code)
                # print(price)
                # print(info)
                # print(location)
                # print(property_url)
                # print(title)

                info = [address, city, state, postal_code, price, info, location, property_url, title]
                print(info)
                writer.writerow(info)
            url = next_url
            time.sleep(random.randint(1, 3))
    csvfile.close()

def add_coordinate(file): #apartmentlist, target_file
    f1 = open(file, 'r+')
    lines = f1.readlines()
    print(lines)
    f1.close()

    f2 = open(file, 'w+')
    for i in range(len(lines)): # add coordinates after each line.
        item_list = lines[i].split(',')
        if len(item_list) == 1: #if the city name, pass
            continue
        elif item_list[0] == item_list[1] == item_list[2] == item_list[3] == 'None': #dont have detail address, going to have location info
            addr = item_list[6]
        else:
            addr = ','.join([item_list[0], item_list[1], item_list[2], item_list[3]])
        api_pool = ['AIzaSyCC9JC6uRITBWXydnWLrDk8j2Fl5ECshPU', 'AIzaSyDSWaAKEr2g5e9_IfJCLdTm_xkql0A3ALI',
                    'AIzaSyDaUwm7EEMzsy-h9hSkOxnYedJ3CRnhclw']
        key = random.choice(api_pool)
        x, y = get_coordinate(addr, key)
        lines[i] = lines[i].replace('\n', '') + f', {x}, {y}\n'
        print(lines[i])
    print(lines)
    f2.writelines(lines)
    f2.close()
    print('Done!')


if __name__ == '__main__':
    #go first then run add_coordinate()
    #get_data(city_dict, 'completed_info.csv')
    add_coordinate('completed_info.csv')
# from bs4 import BeautifulSoup as bs
# import requests
# import csv
# city_dict = {'Hoboken': 'Hoboken-NJ_rb', 'Jersey city': 'Jersey-city-NJ_rb', 'Union city': 'Union-city-NJ_rb'}
#
# pre_url = 'https://www.zillow.com/homes/for_rent/'
#
# def get_data(city_dict): #get data from zillow for rent part, url consist of pre_url and items in city_dict
#     DEFAULT_ADDRESS_NUMBER = 500
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'accept-encoding': 'gzip, deflate, sdch, br',
#         'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
#         'cache-control': 'max-age=0',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
#     }
#     csvfile = open('addresslist', 'w', newline='')
#     writer = csv.writer(csvfile)
#     for city, suffix in city_dict.items():
#         num = 0
#         url = pre_url + suffix
#         print(f'{city}:')
#         writer.writerow([city])
#         while num < DEFAULT_ADDRESS_NUMBER:
#             print(url)
#             html = requests.get(url, headers=headers).text
#             print(html)
#             soup = bs(html, 'lxml')
#             address_list = soup.find_all(class_ = 'zsg-photo-card-address')
#             for address in address_list:
#                 num += 1
#                 print(address.text)
#                 writer.writerow([address.text, url])
#                 if num == DEFAULT_ADDRESS_NUMBER: #first DEFAULT_ADDRESS_NUMBER address each city
#                     break
#
#             if num < DEFAULT_ADDRESS_NUMBER:
#                 next = soup.find(class_ = 'zsg-pagination-next')
#                 if not next:
#                     break
#                 url = 'https://www.zillow.com/' + next.a.get('href')
#
#
# get_data(city_dict)