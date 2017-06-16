from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^submit/',views.submit,name='submit'),
    url(r'^Isbn',views.predict,name='predict'),
    url(r'^Pricing/',views.Pricing, name = 'Pricing'),
    #url(r'^SalesData',views.SalesData, name = 'SalesData'),
    url(r'^SalesData',views.person_list, name = 'people'),
]
