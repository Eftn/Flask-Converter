from converter import result, code_is_valid, num_is_valid, RatesNotAvailableError
from app import app
from unittest import TestCase

app.config["TESTING"] = True

class ConverterTestCase(TestCase):
    def test_valid_number(self):
        """ Function determines correctly if input value is valid number """
        self.assertTrue(num_is_valid('2'))
        self.assertTrue(num_is_valid('2.0'))
        self.assertTrue(num_is_valid(2))
        self.assertTrue(num_is_valid(2.0))
        self.assertFalse(num_is_valid('two'))
        self.assertFalse(num_is_valid('0'))
        self.assertFalse(num_is_valid(0))
        self.assertFalse(num_is_valid('-2'))
        self.assertFalse(num_is_valid(-2))

    def test_valid_curr_code(self):
        """ Function determines correctly if currency code is a valid code """
        self.assertTrue(code_is_valid('USD'))
        self.assertTrue(code_is_valid('eur'))
        self.assertTrue(code_is_valid('Mxn'))
        self.assertTrue(code_is_valid('GBP'))
        self.assertFalse(code_is_valid('aaa'))
        self.assertFalse(code_is_valid('MEX'))
        self.assertFalse(code_is_valid('a'))
        self.assertFalse(code_is_valid('aaaaaaa'))
        self.assertFalse(code_is_valid('122'))
        self.assertFalse(code_is_valid(12))

    def test_converter(self):
        """ Function returns correct string and handles input values appropriately"""        
        self.assertEqual(result('USD', 'USD', '20'), 'US$20.00')
        self.assertRaises(RatesNotAvailableError, result, 'AAA', 'USD', '20')        
        self.assertEqual(result('USD', 'USD', 20), 'US$20.00')        
        self.assertIn('1.00', result('GBP', 'GBP', '1'))
        self.assertIn('5.10', result('GBP', 'gbp', '5.10'))
        self.assertIsInstance(result('USD', 'USD', '20'), str)

class ConverterToutesTestCase(TestCase):
    def test_index(self):
        "Tests if index route is followed correctly"
        with app.test_client() as client:
            res= client.get("/")
            html= res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn("<h1>Forex Converter</h1>")
    def test_post_with_valid_info(self):
        "Test to see if when the post route is followed, data passed in populates"
        def test_post_with_valid_info(self):
        """ Test to see if when post route is followed, passed in data makes it to the html as intended """
        with app.test_client() as client:
            res = client.post('/', data={'curr-from': 'MXN', 'curr-to': 'MXN', 'amt':'20'})
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('$20.00', html)

    def test_post_with_invalid_info(self):
        """ Test to see if redirect code is received when invalid currency code is passed """
        with app.test_client() as client:
            res = client.post('/', data={'curr-from': 'ABC', 'curr-to': 'MXN', 'amt':'20'})

            self.assertEqual(res.status_code, 302)
        
    def test_invalid_code_redirect_with_flash(self):
        """ Test to see if redirect is followed to correct page when invalid currency code is passed """
        with app.test_client() as client:
            res = client.post('/', data={'curr-from': 'ABC', 'curr-to': 'MXN', 'amt':'20'}, follow_redirects= True)

            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('currency code is not valid', html) #proper flash msg displayed

    def test_invalid_amt_redirect_with_flash(self):
        """ Test to see if redirect is followed to correct page when invalid amount is passed """
        with app.test_client() as client:
            res = client.post('/', data={'curr-from': 'USD', 'curr-to': 'MXN', 'amt':'ten'}, follow_redirects= True)

            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('enter a valid currency amount', html) #proper flash msg displayed

    def test_missing_info_redirect_with_flash(self):
        """ Test to see if redirect is followed to correct page when form is missing information"""
        with app.test_client() as client:
            res = client.post('/', data={'curr-from': 'None', 'curr-to': 'MXN', 'amt':'ten'}, follow_redirects= True)

            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('currency code is not valid', html) #proper flash msg displayed
