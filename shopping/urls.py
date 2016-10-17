from django.conf.urls import url

from .views import add, remove, show

urlpatterns = [
    url(r'^add/$', add, name='shopping-cart-add'),
    url(r'^remove/$', remove, name='shopping-cart-remove'),
    url(r'^show/$', show, name='shopping-cart-show'),
]