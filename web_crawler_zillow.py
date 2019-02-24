from lxml import html
import requests
import csv
city_dict = {'Hoboken': 'Hoboken-NJ_rb', 'Jersey city': 'Jersey-city-NJ_rb', 'Union city': 'Union-city-NJ_rb'}
#city_dict = {'Jersey city': 'Jersey-city-NJ_rb'}
pre_url = 'https://www.zillow.com/homes/for_rent/'

def get_data(city_dict): #get data from zillow for rent part, url consist of pre_url and items in city_dict
    #DEFAULT_ADDRESS_NUMBER = 500
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    csvfile = open('apartmentlist', 'w', newline='')
    writer = csv.writer(csvfile)
    for city, suffix in city_dict.items():
        url = pre_url + suffix #combin the url of the first page of the city
        while url: #inspect if the url is none
            response = requests.get(url, headers=headers)
            print(response.text)
            parser = html.fromstring(response.text)
            search_results = parser.xpath("//div[@id='search-results']//article") #crawl all apartment info in the page
            next_url = parser.xpath("//li[@class='zsg-pagination-next']/a/@href") #crawl the URL of next page
            print(next_url)

            for properties in search_results:
                raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
                raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
                raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
                raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
                raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
                raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
                raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
                url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
                raw_title = properties.xpath(".//h4//text()")

                address = ' '.join(' '.join(raw_address).split()) if raw_address else None
                city = ''.join(raw_city).strip() if raw_city else None
                state = ''.join(raw_state).strip() if raw_state else None
                postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
                price = ''.join(raw_price).strip() if raw_price else None
                info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7", ',')
                broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
                title = ''.join(raw_title) if raw_title else None
                property_url = "https://www.zillow.com" + url[0] if url else None

                print(address)
                print(city)
                print(state)
                print(postal_code)
                print(price)
                print(info)
                print(broker)
                print(property_url)
                print(title)
                info = [address, city, state, postal_code, price, info, broker, property_url, title]
                writer.writerow(info)
            url = next_url

get_data(city_dict)

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
#             #print(html)
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