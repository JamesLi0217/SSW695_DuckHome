from lxml import html
import requests
import random
import time
import re
import csv
from api_key import google_keys
from api import get_coordinate
city_dict = {'Hoboken': 'Hoboken-NJ/rentals', 'Jersey city': 'Jersey-city-NJ/rentals', 'Union city': 'Union-city-NJ/rentals'}
#city_dict = {'Jersey city': 'Jersey-city-NJ_rb'}
pre_url = 'https://www.zillow.com/'

def get_data(city_dict, file1, file2): #get data from zillow for rent part, url consist of pre_url and items in city_dict
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']

    csvfile1 = open(file1, 'w', newline='') #open a csv file and ready to pull data
    csvfile2 = open(file2, 'w', newline='')

    writer1 = csv.writer(csvfile1)
    writer2 = csv.writer(csvfile2)

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
                raw_zpid = properties.xpath("./@data-zpid")
                raw_lat = properties.xpath("./@data-latitude")
                raw_lng = properties.xpath("./@data-longitude")
                raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
                raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
                raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
                raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
                raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
                raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
                raw_location = properties.xpath(".//span[@class='zsg-photo-card-address']//text()")
                load_pic = properties.xpath(".//div[@class='zsg-photo-card-img']/img[contains(@src, 'https:')]/@src")
                raw_pic = properties.xpath(".//div[@class='zsg-photo-card-img']/img/@data-src")
                # reg = 'src="(.+?\.jpg)" alt='
                # imgre = re.compile(reg)
                # imglist = re.findall(imgre, properties)

                link = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
                raw_title = properties.xpath(".//h4//text()")

                if not load_pic and raw_pic:
                    pic = raw_pic[0]
                elif not raw_pic and load_pic:
                    pic = load_pic[0]
                else:
                    pic = 'None'

                zpid = raw_zpid[0] if raw_zpid else int(time.time())
                print(zpid)
                address = ' '.join(' '.join(raw_address).split()).replace(',', '') if raw_address else 'None'
                city = ''.join(raw_city).strip().replace(',', '') if raw_city else 'None'
                state = ''.join(raw_state).strip().replace(',', '') if raw_state else 'None'
                postal_code = ''.join(raw_postal_code).strip().replace(',', '') if raw_postal_code else 'None'
                price = ''.join(raw_price).strip().replace(',', '') if raw_price else 'None'
                #print(price)
                info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7", '').replace(',', '') #replace dot with comma
                location = raw_location[0].replace(',', '') if raw_location else 'None'
                title = ''.join(raw_title).replace(',', '') if raw_title else 'None'
                property_url = ("https://www.zillow.com" + link[0]).replace(',', '') if link else 'None'

                if not raw_lat or not raw_lng:
                    if address == city == state == postal_code == 'None':  # dont have detail address, going to have location info
                        addr = location
                    else:
                        addr = ','.join([address, city, state, postal_code])
                    api_pool = google_keys()
                    key = random.choice(api_pool)
                    lat, lng = get_coordinate(addr, key)
                else:
                    lat_str, lng_str = raw_lat[0], raw_lng[0]
                    lat, lng = f"{lat_str[:2]}.{lat_str[2:]}", f"{lng_str[:3]}.{lng_str[3:]}"
                # print(address)
                # print(city)
                # print(state)
                # print(postal_code)
                # print(price)
                # print(info)
                # print(location)
                # print(property_url)
                # print(title)

                info = [zpid, address, city, state, postal_code, price, info, location, property_url, title, lat, lng]
                print(info)
                img = [zpid, pic]
                #print(img)
                writer1.writerow(info)
                writer2.writerow(img)
            url = next_url
            time.sleep(random.randint(1, 3))
    csvfile1.close()
    csvfile2.close()

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
        api_pool = google_keys()
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
    get_data(city_dict, 'completed_info.csv', 'img.csv')
    #add_coordinate('completed_info.csv')
