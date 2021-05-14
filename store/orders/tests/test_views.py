from __future__ import unicode_literals

import os

import mock
import xmltodict
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from store.orders.tests.utils import read_file
from store.orders.exceptions import ApiError
from store.orders.models import Order
from store.orders.views import OrderDetailView

COMPLETE_ORDER_STATUS = os.path.join(
    os.path.dirname(__file__), 'complete_order_status_two_orders_ok.xml')


class StoreViewTest(TestCase):
    def setUp(self):
        super(StoreViewTest, self).setUp()
        self.url = reverse('store:home')

    def test_redirect_when_no_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/accounts/login/?next=/store/')

    @mock.patch('store.orders.views.StoreApiClient')
    def test_has_correct_context(self, mocked__client):
        mocked__client.from_settings.return_value.get_store_url.return_value = 'http://example.com'
        logged_user = get_user_model().objects.create_user('test', email='e@example.com', password='test')
        self.client.login(username=logged_user, password='test')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('http://example.com', response.context[-1]['store_url'])

    @mock.patch('store.orders.views.StoreApiClient')
    def test_should_raise404_when_error_from_api_client(self, mocked__client):
        mocked__client.from_settings.return_value.get_store_url.side_effect = ApiError()
        logged_user = get_user_model().objects.create_user('test', email='e@example.com', password='test')
        self.client.login(username=logged_user, password='test')
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)


class StoreOrdersViewTest(TestCase):
    def setUp(self):
        super(StoreOrdersViewTest, self).setUp()
        self.url = reverse('store:orders')
        rf = RequestFactory()
        self.request = rf.get(self.url)
        self.user = mock.Mock()

    @mock.patch('store.orders.views.StoreApiClient')
    def test_should_redirect_when_user_not_logged_in(self, mocked__client):
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/accounts/login/?next=/orders/')

    @mock.patch('store.orders.views.StoreApiClient')
    def test_should_raise_404_when_error_from_api_client(self, mocked__client):
        logged_user = get_user_model().objects.create_user('test', email='e@example.com', password='test')
        self.client.login(username=logged_user, password='test')
        mocked__client.from_settings.return_value.get_check_participant_order.side_effect = ApiError()
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    @mock.patch('store.orders.views.StoreApiClient')
    def test_should_return_json_when_existing_order(self, mocked__client):
        mocked__client.from_settings.return_value.get_check_participant_order.return_value = Order(
            xmltodict.parse(read_file(COMPLETE_ORDER_STATUS))
        )
        self.request.user = self.user
        response = OrderDetailView.as_view()(self.request)

        self.assertEqual(200, response.status_code)

        order = response.context_data['order']
        self.assertEqual('10001', order.Id)
        self.assertEqual('July 18 2010 12:13:15', order.order_date)
        self.assertEqual('John Doe, 123 State St, Burlington, VT 05491', order.shipping_address)

        order_items = list(order.order_items)
        self.assertEqual(2, len(order_items))

        self.assertEqual('ACME Drill Set', order_items[0].Name)
        self.assertEqual('39393', order_items[0].OrderId)
        self.assertEqual('4847292', order_items[0].ProductId)
        self.assertEqual('July 22 2010', order_items[0].ship_date)
        self.assertEqual('2', order_items[0].Quantity)
        self.assertEqual('500.00', order_items[0].Price)
        self.assertEqual('1000.00', order_items[0].total_price)

        self.assertEqual('ACME Other thing', order_items[1].Name)
        self.assertEqual('39394', order_items[1].OrderId)
        self.assertEqual('979826', order_items[1].ProductId)
        self.assertEqual('July 18 2010', order_items[1].ship_date)
        self.assertEqual('1', order_items[1].Quantity)
        self.assertEqual('150.00', order_items[1].Price)
        self.assertEqual('150.00', order_items[1].total_price)
