from __future__ import unicode_literals

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.base import TemplateView

from .clients import StoreApiClient
from .exceptions import ApiError
from .parsers import JsonParser, XMLParser

logger = logging.getLogger(__name__)


class StoreView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/store_home.html'

    def get_context_data(self, **kwargs):
        ctx = super(StoreView, self).get_context_data(**kwargs)
        store_client = StoreApiClient.from_settings(parser=JsonParser)
        try:
            store_url = store_client.get_store_url(self.request.user)
        except ApiError as e:
            logger.error(e)
            raise Http404

        ctx['store_url'] = store_url
        return ctx


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_details.html'

    def get_context_data(self, **kwargs):
        ctx = super(OrderDetailView, self).get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id')
        client = StoreApiClient.from_settings(parser=XMLParser)
        try:
            order = client.get_check_participant_order(order_id)
        except ApiError as e:
            logger.error('Api Error: %s, order number %s' % (e, order_id))
            raise Http404

        ctx['order'] = order
        return ctx
