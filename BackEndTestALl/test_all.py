import unittest
from db import filter_apartments
from db import get_list_city
from db import add_user
from db import add_apartment_by_userID
from db import get_apartment_by_userID
from db import delete_apart_by_userid
from db import add_img_by_zpid
from db import delete_img_by_zpid
from db import predict_post_price


class TestALl(unittest.TestCase):
    print('test filter_apartments')
    def test_filter_apartments(self):
        valid_apartment_info = {
            'city': 'Jersey city',
            'min_sqft': 0,
            'max_sqft': 5000,
            'bed': 1,
            'bath': 1,
            'min_price': 0,
            'max_price': 5000,
            'title': 'Apartment for rent'
        }
        response = filter_apartments(valid_apartment_info)
        self.assertGreater(len(response['data']), 0, msg='res_list should greater than 0')

    print('test invalid filter_apartments')
    def test_invalid_filter_apartments(self):
        invalid_apartment_info = {
            'city': 'Heights',
            'min_sqft': 0,
            'max_sqft': 5000,
            'bed': 2,
            'bath': 2,
            'min_price': 1100,
            'max_price': 0,
            'title': 'Apartment for rent'
        }
        response = filter_apartments(invalid_apartment_info)
        self.assertEqual(response['success'], False, msg='The response is error')


    print('test get_list_city')
    def test_get_list_city(self):
        response = get_list_city('Hoboken')
        self.assertEqual(response['success'], True, msg='Return a list of apartments under the entered city.')
        self.assertGreater(len(response['data']), 0, msg='The len of the list should more than 0.')

    print('test invalid get_list_city')
    def test_invalid_get_list_city(self):
        response = get_list_city('Heights')
        self.assertEqual(response['success'], False, msg='Return a list of apartments under the entered city.')
        self.assertIn('desc', response, msg='response of False should have a desc to describe the error.')

    print('test add_user')
    def test_add_user(self):
        pass

    print('test add_apartment_by_userID')
    def test_add_apartment_by_userID(self):
        apartment_info = {
            'address': '20 River Ct',
            'city': 'Jersey city',
            'state': 'NJ',
            'postal_code': '07310',
            'bed': 2,
            'bath': 2,
            'sqft': 1200,
            'price': 3900,
            'title': 'Apartment for rent'
        }
        user_ID = '5c86bace0840c437cf3d6939'
        response = add_apartment_by_userID(apartment_info, user_ID)
        self.assertEqual(response['success'], True, msg='The status of success should be True.')
        self.assertIsNotNone(response['data'], msg='The new item in database should be added.')

    print('test invalid_add_apartment_by_userID')
    def test_invalid_add_apartment_by_userID(self):
        apartment_info = {
            'address': '20 River Ct',
            'city': 'Jersey city',
            'state': 'NJ',
            'postal_code': '07310',
            'bed': 2,
            'bath': 2,
            'sqft': 1200,
            'price': 3900,
            'title': 'Apartment for rent'
        }
        user_ID = '5c86bace0840c437cf3d6939'
        response = add_apartment_by_userID(apartment_info, user_ID)
        self.assertEqual(response['success'], False, msg='The status of success should be True.')
        self.assertIsNotNone(response['desc'], msg='The inserted item shouldnt be added')

    print('test get_apartment_by_userID')
    def test_get_apartment_by_userID(self):
        user_ID = '5c86bace0840c437cf3d6939'
        response = get_apartment_by_userID(user_ID)
        self.assertEqual(response['success'], True, msg='The status of success should be True.')
        self.assertIsNotNone(response['data'], msg='data in response should have the item from database.')

    print('test invalid_get_apartment_by_userID')
    def test_invalid_get_apartment_by_userID(self):
        user_ID = 'something may be wrong'
        response = get_apartment_by_userID(user_ID)
        self.assertEqual(response['success'], False, msg='The user_ID doesnt exist in apartment_list, it should be False')
        self.assertIn('desc', response, msg='response of False should have a desc to describe the error.')

    print('test delete_apart_by_userid')
    def test_delete_apart_by_userid(self):
        apartment_info = {
            'address': '20 River Ct',
            'city': 'Jersey city',
            'state': 'NJ',
            'postal_code': '07310',
            'bed': 2,
            'bath': 2,
            'sqft': 1200,
            'price': 3900,
            'title': 'Apartment for rent'
        }
        user_ID = '5c86bace0840c437cf3d6939'
        response = delete_apart_by_userid(apartment_info, user_ID)
        self.assertEqual(response['success'], True, msg='The status of success should be True')



if __name__ == '__main__':
    test_suit = unittest.TestSuite()
    suit = [test_filter_apartments()]