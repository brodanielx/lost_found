from django.conf.urls import url
from contacts import views

app_name = 'contacts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[\w\-]+)/$',
        views.my_profile, name='my_profile'),
    url(r'^addcontact/$', views.add_contact, name='add_contact'),
    url(r'^contact/(?P<pk>[\w\-]+)/$',
        views.show_contact, name='show_contact'),
]
