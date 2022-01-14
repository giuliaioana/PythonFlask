#!/usr/bin/env python
import unittest
from main import api

class TestHello(unittest.TestCase):

    def setUp(self):
        api.testing = True
        self.app = api.test_client()

    def test_hello(self):
        rv = self.app.get('/persons')
        self.assertEqual(rv.status, '200 OK')
        

    def test_hello_hello(self):
        rv = self.app.get('/products')
        self.assertEqual(rv.status, '200 OK')
        

    # def test_hello_name(self):
    #     id = '1'
    #     rv = self.app.get(f'/products/{id}')
    #     self.assertEqual(rv.status, '200 OK')
        

if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()
