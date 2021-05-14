from __future__ import unicode_literals

import os

from django.test import TestCase

from store.orders.tests.utils import read_file
from store.orders.models import OrderItem, Order

XML_PATH = os.path.join(os.path.dirname(__file__))


class OrderTest(TestCase):
    def test_from_xml_should_parse_xml_with_two_orders_when_correct(self):
        data_ok = read_file(os.path.join(XML_PATH, 'complete_order_status_two_orders_ok.xml'))
        order = Order.from_xml(data_ok)
        self.assertIsInstance(order, Order)
        self.assertEqual('10001', order.Id)
        self.assertEqual('July 18 2010 12:13:15', order.order_date)

        order_items = list(order.order_items)
        self.assertEqual(2, len(order_items))

        self.assertIsInstance(order_items[0], OrderItem)
        self.assertEqual('39393', order_items[0].OrderId)
        self.assertEqual('July 22 2010', order_items[0].expected_ship_date)
        self.assertEqual('', order_items[0].actual_ship_date)

        self.assertIsInstance(order_items[1], OrderItem)
        self.assertEqual('39394', order_items[1].OrderId)
        self.assertEqual('July 18 2010', order_items[1].expected_ship_date)
        self.assertEqual('', order_items[1].actual_ship_date)

    def test_from_xml_should_parse_xml_with_one_orders_when_correct(self):
        data_ok = read_file(os.path.join(XML_PATH, 'complete_order_status_one_order_ok.xml'))
        order = Order.from_xml(data_ok)
        self.assertIsInstance(order, Order)
        self.assertEqual('10001', order.Id)
        self.assertEqual('July 18 2010 12:13:15', order.order_date)

        order_items = list(order.order_items)
        self.assertEqual(1, len(order_items))

        self.assertIsInstance(order_items[0], OrderItem)
        self.assertEqual('39393', order_items[0].OrderId)
        self.assertEqual('July 11 2010', order_items[0].expected_ship_date)
        self.assertEqual('', order_items[0].actual_ship_date)
