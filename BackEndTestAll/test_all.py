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
from db import chart_calculus

class TestAll(unittest.TestCase):
    def test_filter_apartments(self):
        """test filter_apartments"""

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


    def test_invalid_filter_apartments(self):
        """test invalid filter_apartments"""

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



    def test_get_list_city(self):
        """test get_list_city"""

        response = get_list_city('Hoboken')
        self.assertEqual(response['success'], True, msg='Return a list of apartments under the entered city.')
        self.assertGreater(len(response['data']), 0, msg='The len of the list should more than 0.')


    def test_invalid_get_list_city(self):
        """test invalid get_list_city"""

        response = get_list_city('Heights')
        self.assertEqual(response['success'], False, msg='Return a list of apartments under the entered city.')
        self.assertIn('desc', response, msg='response of False should have a desc to describe the error.')


    def test_add_user(self):
        pass


    def test_add_apartment_by_userID(self):
        """test add_apartment_by_userID"""

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
        delete_apart_by_userid(apartment_info, user_ID)

    def test_invalid_add_apartment_by_userID(self):
        """test invalid_add_apartment_by_userID"""

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
        add_apartment_by_userID(apartment_info, user_ID)
        response = add_apartment_by_userID(apartment_info, user_ID)
        #print(response)
        self.assertEqual(response['success'], False, msg='The status of success should be False.')
        self.assertIsNotNone(response['desc'], msg='The inserted item shouldnt be added')
        delete_apart_by_userid(apartment_info, user_ID)

    def test_get_apartment_by_userID(self):
        """test get_apartment_by_userID"""

        user_ID = '5c86bace0840c437cf3d6939'
        response = get_apartment_by_userID(user_ID)
        #print(response)
        self.assertEqual(response['success'], True, msg='The status of success should be True.')
        self.assertIsNotNone(response['data'], msg='data in response should have the item from database.')


    def test_invalid_get_apartment_by_userID(self):
        """test invalid_get_apartment_by_userID"""
        user_ID = 'something may be wrong'
        response = get_apartment_by_userID(user_ID)
        #print(response)
        self.assertEqual(response['success'], False, msg='The user_ID doesnt exist in apartment_list, it should be False')
        self.assertIn('desc', response, msg='response of False should have a desc to describe the error.')


    def test_delete_apart_by_userid(self):
        """test delete_apart_by_userid"""
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
        add_apartment_by_userID(apartment_info, user_ID)
        response = delete_apart_by_userid(apartment_info, user_ID)
        #print(response)
        self.assertEqual(response['success'], True, msg='The status of success should be True')

    def test_invalid_delete_apart_by_userid(self):
        """test invalid_delete_apart_by_userid"""
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
        self.assertEqual(response['success'], False, msg='The status of success should be False')

    def test_invalid_add_img_by_zpid(self):
        """test invalid_add_img_by_zpid"""
        zpid = '1001483623'
        img = 'a img'
        response = add_img_by_zpid(img, zpid)
        self.assertEqual(response['success'], False, msg='The status of success should be False.')

    def test_invalid_delete_img_by_zpid(self):
        """test invalid_delete_img_by_zpid"""
        zpid = 'a wrong zpid'
        response = delete_img_by_zpid(zpid)
        self.assertEqual(response['success'], False, msg='The status of success should be False.')

    def test_predict_post_price(self):
        """test predict_post_price"""
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
        response = predict_post_price(apartment_info,
                                      '/Users/franklin/SSW695/SSW695_DuckHome/build_model/SGDRegression_model.pkl')
        self.assertEqual(response['success'], True, msg='The status of response should be True.')
        self.assertEqual(isinstance(response['data'], float), True, msg='The returned data should be an integer.')

    def test_invalid_predict_post_price(self):
        """test invalid_predict_post_price"""
        apartment_info = {
            'address': '20 River Ct',
            'city': 'Heights',
            'state': 'NJ',
            'postal_code': '07310',
            'bed': 2,
            'bath': 2,
            'sqft': 1200,
            'price': 3900,
            'title': 'Apartment for rent'
        }
        response = predict_post_price(apartment_info,
                                      '/Users/franklin/SSW695/SSW695_DuckHome/build_model/SGDRegression_model.pkl')
        self.assertEqual(response['success'], False, msg='The status of the response should be False.')

    def test_chart_calculus(self):
        """test chart_calculus"""
        city = 'Hoboken'
        start_date = '2019-04-01'
        response = chart_calculus(city, start_date)
        self.assertEqual(response['success'], True, msg='The status of the response should be True.')

    def test_invalid_chart_calculus(self):
        """test invalid_chart_calculus"""
        city = 'Heights'
        start_date = '2019-04-01'
        response = chart_calculus(city, start_date)
        self.assertEqual(response['success'], False, msg='The status of the response should be False.')

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # tests = [TestAll("test_filter_apartments"), TestAll("test_invalid_filter_apartments"),
    #          TestAll("test_get_list_city"), TestAll("test_invalid_get_list_city"),
    #          TestAll("test_add_apartment_by_userID"), TestAll("test_invalid_add_apartment_by_userID"),
    #          TestAll("test_get_apartment_by_userID"), TestAll("test_invalid_get_apartment_by_userID"),
    #          TestAll("test_delete_apart_by_userid")]
    #
    # suite.addTests(tests)
    # runner = unittest.TextTestRunner(verbosity=1)
    # runner.run(suite)
