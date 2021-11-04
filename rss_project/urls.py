from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rss_app import views
from rss_app.views import LatestPostsFeed, LatestPostsFeedTwo

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^rss_app/', include('rss_app.urls')),
    url(r'^rss_get$', views.rss_get, name='rss_get'),
    url(r'^rss_two_get$', views.rss_two_get, name='rss_two_get'),
    url(r'^get_check_ads_one/$', views.get_check_ads_one, name="get_check_ads_one"),
    url(r'^get_check_ads_two/$', views.get_check_ads_two, name="get_check_ads_two"),
    url(r'^feeds/$', LatestPostsFeed(), name='feeds'),
    url(r'^feedstwo/$', LatestPostsFeedTwo(), name='feedstwo')
]
