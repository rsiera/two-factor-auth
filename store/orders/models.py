from __future__ import unicode_literals

from decimal import Decimal

import xmltodict

from .utils import format_datetime, format_date


class DataContainer(object):
    def __getattr__(self, item):
        return self._data.get(item, '') or ''


class OrderItem(DataContainer):
    def __init__(self, data):
        self._data = data

    @property
    def ship_date(self):
        return self.actual_ship_date or self.expected_ship_date

    @property
    def expected_ship_date(self):
        if not self.ExpectedShipDate:
            return ''
        return format_date(self.ExpectedShipDate)

    @property
    def actual_ship_date(self):
        if not self.ActualShipDate:
            return ''
        return format_date(self.ActualShipDate)

    def to_json(self):
        return {
            'Name': self.Name,
            'OrderId': self.OrderId,
            'ProductId': self.ProductId,
            'Quantity': self.Quantity,
            'ShipDate': self.ship_date,
            'Status': self.Status,
            'Price': self.Price,
        }

    @property
    def total_price(self):
        return str(Decimal(self.Price or '0') * int(self.Quantity))


class Order(DataContainer):
    ROOT_TAG = 'Order'

    def __init__(self, data):
        self._data = data[self.ROOT_TAG]
        self.order_items = self.get_order_items()

    def get_order_items(self):
        order_detail = self._data.get('OrderDetail', {})
        for order_item in self.order_item_to_list(order_detail):
            yield OrderItem(order_item)

    def order_item_to_list(self, order_detail):
        order_item = order_detail.get('OrderItem', [])
        if not isinstance(order_item, list):
            return [order_item]
        return order_item

    def to_json(self):
        return {
            'Id': self.Id,
            'TotalPrice': self.TotalPrice,
            'OrderedDate': self.actual_ship_date,
            'ShippingAddress': self.shipping_address,
            'Items': [
                item.to_json() for item in self.get_order_items()]
        }

    @property
    def shipping_address(self):
        return "%s, %s" % (self.ShipFirstLastName, self.ShipAddress)

    @property
    def order_date(self):
        if not self.OrderDate:
            return ''
        return format_datetime(self.OrderDate)

    @classmethod
    def from_xml(cls, content):
        return cls(xmltodict.parse(content))

