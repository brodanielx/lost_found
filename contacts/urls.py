from django.conf.urls import url
from contacts import views

app_name = 'contacts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/user/data/$', views.user_activity),
    url(r'^mycontacts/(?P<username>[\w\-]+)/$',
        views.my_contacts, name='my_contacts'),
    url(r'^addcontact/$', views.add_contact, name='add_contact'),
    url(r'^importcontacts/$', views.import_contacts, name='import_contacts'),
    url(r'^importcontacts/success/$', views.import_success, name='import_success'),
    url(r'^importcontacts/fail/$', views.import_failure, name='import_failure'),
    url(r'^contact/(?P<pk>[\w\-]+)/$',
        views.show_contact, name='show_contact'),
    url(r'^editcontact/(?P<pk>[\w\-]+)/$',
        views.edit_contact, name='edit_contact'),
    url(r'^search/$', views.search, name='search'),
    url(r'^history/$', views.history, name='history'),
]
