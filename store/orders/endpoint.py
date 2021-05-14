from __future__ import unicode_literals

import logging

import requests
from django.conf import settings

from .exceptions import ApiConnectionError
from .timer import timer

HTTP_VERBS = frozenset(('get', 'post', 'put', 'delete'))

logger = logging.getLogger(__name__)


class Endpoint(object):
    """
    Takes endpoint URL, authentication tuple (username, password),
    list of methods supported by the API.

    Exposes two methods (get, post) that will make call to
    the API. `post` and `get` take one argument `data` that will be XML.
    """

    class MethodNotAllowed(Exception):
        pass

    class ParameterError(Exception):
        pass

    def __init__(
            self, url, auth, methods=HTTP_VERBS, params=None, timeout=None,
            _requests=requests):

        self.url = url
        self.auth = auth
        self._params_spec = params or {}
        self._methods = methods
        self._requests = _requests
        self.timeout = timeout
        if self.timeout is None:
            self.timeout = settings.STORE_DEFAULT_TIMEOUT

    def get(self, **kwargs):
        return self._call_method('get', params=kwargs)

    def post(self, data=None):
        if data is None:
            return self._call_method('post')
        return self._call_method('post', data=data, headers=self.default_headers)

    @property
    def default_headers(self):
        return {'Content-Type': 'application/xml'}

    def _call_method(self, method_name, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        method = self._get_method(method_name)
        with timer(self._log(method_name)):
            try:
                logger.info("Order API %s request. Request: %s", method_name, kwargs)
                response = method(self.url, auth=self.auth, **kwargs)
            except requests.exceptions.RequestException as e:
                raise ApiConnectionError('Error calling Store API: %s' % e)
            else:
                logger.info("Order API %s completed. Response: %s, Status: %s",
                            method_name, response.content, response.status_code)
                return response

    def _get_method(self, method_name):
        if method_name not in self._methods:
            msg = '%s not allowed for endpoint %s' % (method_name, self.url)
            raise self.MethodNotAllowed(msg)
        return getattr(self._requests, method_name)

    def _log(self, method_name):
        msg = 'store api | %.6s | %s | %s'
        return msg % (method_name.upper(), self.auth[0], self.url)
