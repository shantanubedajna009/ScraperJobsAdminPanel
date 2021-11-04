from django.conf.urls import url
from rss_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rss_app'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^add_job$', views.add_job, name='add_job'),
    url(r'^list_job$', views.list_job, name='list_job'),
    #url(r'^show_notification$', views.show_notification, name='show_notification'),
    #url(r'^get_models/(?P<pk>.+)/$', views.get_models, name='get_models')
    url(r'^login$', views.user_login, name='user_login'),
    url(r'^logout$', views.user_logout, name='user_logout'),
    url(r'^get_job/(?P<pk>.+)/$', views.get_job, name='get_job'),
    url(r'^delete_job/(?P<pk>.+)/$', views.delete_job, name='delete_job'),
    url(r'^update_job$', views.update_job, name='update_job'),
    url(r'^update_status/(?P<pk>.+)/$', views.update_status, name='update_status'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
