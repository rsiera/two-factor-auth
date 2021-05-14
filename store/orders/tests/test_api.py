from __future__ import unicode_literals

from django.test import TestCase

from store.orders.api import BaseApi, ROOT_URL


class BaseApiTest(TestCase):
    def test_generates_url_from_parts(self):
        api = BaseApi('user', 'pass')
        url = api._url(['a', 2, 'b'])
        self.assertEqual(url, '%s/a/2/b' % ROOT_URL)

    def test_creates_correct_endpoint(self):
        api = BaseApi('user', 'pass')
        endpoint = api._endpoint(['resources'], ['get'])
        self.assertEqual(('user', 'pass'), endpoint.auth)
        self.assertEqual(api._url(['resources']), endpoint.url)
        self.assertEqual(['get'], endpoint._methods)
