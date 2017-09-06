from django.conf.urls import url
from .views import index
from .views import add_cart
from .views import show_cart
from .views import remove_cart
from .views import update_cart
from .views import current_cart
from .views import clear_cart
from .views import payment_local
from .views import thank_you
from .views import orderlist
from .views import get_my_order

urlpatterns = [
    url(r'^add/$', add_cart, name='shopping-cart-add'),
    url(r'^show/$', show_cart, name='shopping-cart-show'),
    url(r'^remove/$', remove_cart, name='shopping-cart-remove'),
    url(r'^update/$', update_cart, name='shopping-cart-update'),
    url(r'^current/$', current_cart, name='shopping-cart-current'),
    url(r'^clear/$', clear_cart, name='shopping-cart-clear'),
    url(r'^payment-local/$', payment_local, name='payment-local'),
    url(r'^thankyou/(?P<order_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', thank_you, name='thank-you'),
    url(r'^orderlist/$', orderlist, name='orderlist'),
    url(r'^my_orders/$', get_my_order, name='get_my_order'),
    url(r'^', index, name='index'),
]
