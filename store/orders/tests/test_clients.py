import json
import os

import mock
import xmltodict
from django.test import TestCase

from store.orders.parsers import JsonParser, XMLParser
from store.orders.clients import StoreApiClient
from store.orders.exceptions import ApiError
from store.orders.models import Order

COMPLETE_ORDER_STATUS = os.path.join(
    os.path.dirname(__file__), 'complete_order_status_ok.xml')


class StoreApiClientTest(TestCase):
    def setUp(self):
        self.api = mock.Mock()

    def test_get_check_user_order_should_call_api_with_proper_params_when_ok(self):
        store_client = StoreApiClient(
            username='test_user', password='password', parser=XMLParser(), _api=self.api)
        self.api.check_participant_order().post.return_value = FakeResponse(
            xmltodict.unparse({"Order": {}}), True)
        store_client.get_check_user_order('123')

        expected_payload_xml = xmltodict.unparse({
            'checkUserOrder':
                {
                    'AuthorizationUsername': 'test_user',
                    'AuthorizationPassword': 'password',
                    'OrderId': '123',
                }
        })

        self.api.check_participant_order().post.assert_called_with(
            data=expected_payload_xml)

    def test_get_check_user_order_should_raise_api_error_when_post_response_not_ok(self):
        store_client = StoreApiClient(
            username='test_user', password='password', parser=XMLParser(), _api=self.api)
        self.api.check_participant_order().post().ok = False
        with self.assertRaises(ApiError):  # TODO: make exception better
            store_client.get_check_user_order('wrong')

    def test_get_check_user_order_order_should_create_order_status_when_response_ok(self):
        store_client = StoreApiClient(
            username='test_user', password='password', parser=XMLParser(), _api=self.api)
        with open(COMPLETE_ORDER_STATUS) as f:
            data = f.read()
        self.api.check_participant_order().post.return_value = FakeResponse(data, True)
        order_statuses = store_client.get_check_user_order('123')
        self.assertIsInstance(order_statuses, Order)
        self.assertEqual('10001', order_statuses.Id)
        self.assertEqual('1381.50', order_statuses.TotalPrice)

    def test_get_store_url_should_call_api_with_proper_params_when_ok(self):
        store_client = StoreApiClient(
            username='test_user', password='password', parser=JsonParser(), _api=self.api)
        self.api.store_url().post.return_value = FakeResponse(
            json.dumps({"Response": {
                "url": "http://example.com", "ErrorCode": 0}
            }), True)

        user = mock.Mock(id=1, first_name='user', last_name='test', email='user@gmail.com')
        store_client.get_store_url(user)

        expected_payload_xml = xmltodict.unparse({
            'getUrl':
                {
                    'AuthorizationUsername': 'test_user',
                    'AuthorizationPassword': 'password',
                    'AccountID': user.id,
                    'FirstName': user.first_name,
                    'LastName': user.last_name,
                    'Email': user.email,
                }
        })

        self.api.store_url().post.assert_called_with(data=expected_payload_xml)

    def test_get_store_url_should_return_url_when_response_ok(self):
        store_client = StoreApiClient(
            username='test_user', password='password', parser=JsonParser(), _api=self.api)
        data = {
            'Response': {'url': 'https://example.com', "ErrorCode": 0}
        }

        user = mock.Mock()
        self.api.store_url().post.return_value = FakeResponse(
            json.dumps(data), True)
        store_url = store_client.get_store_url(user)
        self.assertEqual('https://example.com', store_url)


class FakeResponse(object):
    def __init__(self, content, ok):
        self.content = content
        self.ok = ok
        self.status_code = 'status_code'
        self.reason = 'response reason'
