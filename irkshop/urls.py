from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings

from goods import views as goods_views


urlpatterns = [
    url(r'^accounts/login/$', login,
        {'template_name': 'login/login.html'}),
    url(r'^accounts/logout/$', logout),
    url(r'^admin/', admin.site.urls),
    url(r'^$', goods_views.index),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^add/$', goods_views.add_cart, name='shopping-cart-add'),
    url(r'^show/$', goods_views.show_cart, name='shopping-cart-show'),
    url(r'^remove/$', goods_views.remove_cart, name='shopping-cart-remove'),
]
