from django.conf.urls import url
from .views import shop_main
from .views import add_cart
from .views import show_cart
from .views import remove_cart
from .views import update_cart
from .views import current_cart
from .views import clear_cart
from .views import payment
from .views import korea_bank_payment
from .views import thank_you
from .views import orderlist
from .views import get_my_order

urlpatterns = [
    url(r'^bank_payment/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', korea_bank_payment, name='korea_bank_payment'),
    url(r'^add/$', add_cart, name='shopping-cart-add'),
    url(r'^show/$', show_cart, name='shopping-cart-show'),
    url(r'^remove/$', remove_cart, name='shopping-cart-remove'),
    url(r'^update/$', update_cart, name='shopping-cart-update'),
    url(r'^current/$', current_cart, name='shopping-cart-current'),
    url(r'^clear/$', clear_cart, name='shopping-cart-clear'),
    url(r'^payment/$', payment, name='payment'),
    url(r'^thankyou/(?P<order_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', thank_you, name='thank-you'),
    url(r'^orderlist/$', orderlist, name='orderlist'),
    url(r'^my_orders/$', get_my_order, name='get_my_order'),
    url(r'^', shop_main, name='shop_main'),
]
