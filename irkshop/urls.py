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
]
