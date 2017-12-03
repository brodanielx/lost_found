from django.conf.urls import url
from contacts import views

app_name = 'contacts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/(?P<pk>[\w\-]+)/$',
        views.show_contact, name='show_contact'),
]
