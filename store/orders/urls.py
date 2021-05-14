from django.conf.urls import url

from .views import StoreView, OrderDetailView

urlpatterns = [
    url(r'^store/$', StoreView.as_view(), name='home'),
    url(r'^orders/$', OrderDetailView.as_view(), name='orders'),
]
