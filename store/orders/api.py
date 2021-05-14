from __future__ import unicode_literals

from django.conf import settings

from .endpoint import Endpoint

ROOT_URL = settings.STORE_API_BASE
GET_ONLY = ('get',)
PUT_ONLY = ('put',)
POST_ONLY = ('post',)


class BaseApi(object):
    def __init__(self, username, password):
        self.auth = (username, password)

    def _url(self, url_parts):
        parts = [ROOT_URL]
        parts.extend(url_parts)
        return '/'.join(str(part) for part in parts)

    def _endpoint(self, url_parts, methods, params=None, timeout=None):
        url = self._url(url_parts)
        return Endpoint(url, self.auth, methods, params, timeout=timeout)


class StoreOrderApi(BaseApi):
    BASE_PART = 'v1'

    def check_participant_order(self):
        parts = (self.BASE_PART, 'orders')
        return self._endpoint(parts, POST_ONLY)

    def store_url(self):
        parts = (self.BASE_PART, 'resources', 'store')
        return self._endpoint(parts, POST_ONLY)
