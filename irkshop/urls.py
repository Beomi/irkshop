from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.views.static import serve

from goods import views as goods_views


urlpatterns = [
    url(r'^accounts/login/$', login,
        {'template_name': 'login_page/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', goods_views.index, name='index'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^add/$', goods_views.add_cart, name='shopping-cart-add'),
    url(r'^show/$', goods_views.show_cart, name='shopping-cart-show'),
    url(r'^remove/$', goods_views.remove_cart, name='shopping-cart-remove'),
    url(r'^update/$', goods_views.update_cart, name='shopping-cart-update'),
    url(r'^current/$', goods_views.current_cart, name='shopping-cart-current'),
    url(r'^clear/$', goods_views.clear_cart, name='shopping-cart-clear'),
    url(r'^payment-local/$', goods_views.payment_local, name='payment-local'),
    url(r'^payment-paypal/(?P<order_number>[0-9]+)$', goods_views.payment_paypal, name='payment-paypal'),
    url(r'^thankyou/$', goods_views.thank_you, name='thank-you'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^orderlist/$', goods_views.orderlist, name='orderlist'),
    url(r'^my_orders/$', goods_views.get_my_order, name='get_my_order'),
    url(r'^ht/', include('health_check.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]