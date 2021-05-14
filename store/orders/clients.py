from __future__ import unicode_literals

import logging

import xmltodict
from django.conf import settings

from .api import StoreOrderApi
from .exceptions import ApiError, AuthError
from .models import Order

logger = logging.getLogger(__name__)


class BaseApiClient(object):
    Error = ApiError
    api_class = None

    def __init__(self, username=None, password=None, parser=None, _api=None):
        self._username = username
        self._password = password
        self.parser = parser
        self.api = _api or self.api_class(username, password)

    def _handle_response(self, response):
        if not response.ok:
            code, reason = response.status_code, response.reason
            if code == 403:
                logger.error(reason)
                raise AuthError(reason)
            msg = 'Restapi returned %s: %s' % (code, reason)
            logger.error(msg)
            raise ApiError(msg)
        return self.parser.parse_response(response.content)

    @classmethod
    def from_settings(cls, **kwargs):
        return cls(
            username=settings.STORE_API_USERNAME,
            password=settings.STORE_API_PASSWORD,
            **kwargs
        )


class StoreApiClient(BaseApiClient):
    api_class = StoreOrderApi

    def get_check_user_order(self, order_id):
        payload = {
            'checkUserOrder':
            {
                'AuthorizationUsername': self._username,
                'AuthorizationPassword': self._password,
                'OrderId': order_id,
            }
        }

        xml_payload = xmltodict.unparse(payload)
        response = self.api.check_participant_order().post(data=xml_payload)
        order_data = self._handle_response(response)
        return Order(data=order_data)

    def get_store_url(self, user):
        payload = {
            'getUrl': {
                'AuthorizationUsername': self._username,
                'AuthorizationPassword': self._password,
                'AccountID': user.id,
                'FirstName': user.first_name,
                'LastName': user.last_name,
                'Email': user.email,
            }
        }

        xml_payload = xmltodict.unparse(payload)
        response = self.api.store_url().post(data=xml_payload)
        response_content = self._handle_response(response)
        return response_content['Response'].get('url', '')
