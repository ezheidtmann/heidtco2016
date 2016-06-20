from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.rsvp_page, name='rsvp_page'),
    url(r'^api/', include(views.router.urls)),
]
