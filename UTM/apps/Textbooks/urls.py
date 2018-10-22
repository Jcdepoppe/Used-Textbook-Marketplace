from django.conf.urls import url
from . import views          
urlpatterns = [
	url(r'^$', views.index),
	url(r'^(?P<id>\d+)/show$', views.showbook),
	url(r'^add$', views.addAbook),

]
