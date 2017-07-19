from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login,
        {'template_name': 'login_page/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ht/', include('health_check.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^shop/', include('goods.urls')),
    url(r'^', TemplateView.as_view(template_name='index.html')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
                       url(r'^__debug__/', include(debug_toolbar.urls)),
                       url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                   ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
