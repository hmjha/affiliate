from django.conf.urls import patterns, url
from tyaffiliate import views

urlpatterns = patterns('',
                       url(r'^login$', views.login, name='login'),
                       url(r'^$', views.home, name='home'),
                       url(r'^realtime_data/$', views.get_google_data, name='realtime'),
                       url(r'topyaps_data/$', views.get_topyaps_data, name='topyaps'),
                       url(r'^account$', views.accounts, name='accounts'),
                       url(r'^search$', views.search, name='search'),
                       url(r'additional_data/$', views.page_additional_data, name='additional'),
                       url(r'^published/(\d)+$', views.view_published_posts, name='published'),
                       url(r'^publish_data/$', views.get_published_posts, name='publish_data'),
                       url(r'sync_data/$', views.sync_posts, name='sync_posts'),
                       url(r'^logout$', views.logout, name='logout'),
)
