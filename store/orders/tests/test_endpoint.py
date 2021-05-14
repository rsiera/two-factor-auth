from __future__ import unicode_literals

import mock
import requests
import xmltodict
from django.conf import settings
from django.test import TestCase

from store.orders.endpoint import Endpoint
from store.orders.exceptions import ApiConnectionError


class EndpointTest(TestCase):
    url = 'http://example.com'
    auth = ('username', 'password')

    def setUp(self):
        super(EndpointTest, self).setUp()
        self.requests = mock.Mock()

    def test_makes_post_requests(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        endpoint.post()
        self.requests.post.assert_called_with(
            self.url,
            auth=self.auth,
            timeout=settings.STORE_DEFAULT_TIMEOUT
        )

    def test_passes_data_to_post_json(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        payload = {'a': 1}
        payload_xml = xmltodict.unparse(payload)
        endpoint.post(payload_xml)
        self.requests.post.assert_called_with(
            self.url,
            auth=self.auth,
            data=payload_xml,
            headers={'Content-Type': 'application/xml'},
            timeout=settings.STORE_DEFAULT_TIMEOUT
        )

    def test_allows_all_methods_by_default(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        payload = {'name': 'alice'}
        payload_xml = xmltodict.unparse(payload)

        for method in ['post']:
            getattr(endpoint, method)(payload_xml)
            getattr(self.requests, method).assert_called_with(
                self.url,
                auth=self.auth,
                headers={'Content-Type': 'application/xml'},
                data=payload_xml,
                timeout=settings.STORE_DEFAULT_TIMEOUT
            )

        for method in ['get']:
            getattr(endpoint, method)(name='alice')
            getattr(self.requests, method).assert_called_with(
                self.url,
                auth=self.auth,
                params={'name': 'alice'},
                timeout=settings.STORE_DEFAULT_TIMEOUT
            )

    def test_can_disallow_methods(self):
        endpoint = Endpoint(
            self.url, self.auth, methods=['get'], _requests=self.requests)
        self.assertRaises(Endpoint.MethodNotAllowed, endpoint.post)

    def test_returns_requests_response(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        response = endpoint.get()
        self.assertEqual(response, self.requests.get())

    def test_call_get_raise_api_exception_when_request_exception(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        self.requests.get.side_effect = requests.exceptions.RequestException
        self.assertRaises(ApiConnectionError, endpoint.get)

    def test_call_post_raise_api_exception_when_request_exception(self):
        endpoint = Endpoint(self.url, self.auth, _requests=self.requests)
        self.requests.post.side_effect = requests.exceptions.RequestException
        self.assertRaises(ApiConnectionError, endpoint.post)
