## Functions

### 1. get_list_city(city)
----
+ Get apartment list from homepage city filter by city name.
+ Arguments:
    + city: string
+ Return: dictionary
    + True: {'success': True, 'data': result_city}
        + result_city type: list
            + elements type: dictionary 
                + 'zpid': string
                + 'address': string
                + 'city': string
                + 'state': string
                + 'postal_code': string
                + 'info': list
                    + elements type: dict
                        + 'bed': float
                        + 'price': float
                        + 'bath': float
                        + 'sqft': int
                + 'location': string
                + 'property_url': string
                + 'title': string
                + 'coordinates': dict
                    + 'lat': string
                    + 'lng': string
    + False: {'success': False, 'desc': "can't find any apartment as filters in database"}
    
### 2. get_img(zpid)
----
+ Get image binary data by apartment zpid
+ Arguments:
    + zpid: string
+ Return: dictionary
    + True: {'success': True, 'data': img_data}
        + img_data: binary   
    + False: {'success': False, 'desc': "can't find any images by this zpid in database"}
    
### 3. filter_apartments(filters)
----
+ Filter the apartments by arguments
+ Arguments:
    + city: string
    + min_price: float 
    + max_price: float
    + beds: float
    + baths: float
    + min_sqft: int
    + max_sqft: int
+ Return:
    + True: {'success': True, 'data': res_list}
        + res_list type: list
            + elements type: dictionary 
                + 'zpid': string
                + 'address': string
                + 'city': string
                + 'state': string
                + 'postal_code': string
                + 'info': list
                    + elements type: dict
                        + 'bed': float
                        + 'price': float
                        + 'bath': float
                        + 'sqft': int
                + 'location': string
                + 'property_url': string
                + 'title': string
                + 'coordinates': dict
                    + 'lat': string
                    + 'lng': string              
    + False: {'success': False, 'desc': "can't find any apartment as filters in database"}
   
   