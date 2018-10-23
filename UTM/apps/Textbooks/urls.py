from django.conf.urls import url
from . import views          
urlpatterns = [
	url(r'^$', views.index),
	url(r'^(?P<id>\d+)/show$', views.showbook),
	url(r'^add$', views.addNewbook),
	url(r'^(?P<id>\d+)/edit$', views.editBookInfo),
	url(r'^(?P<id>\d+)/delete$', views.deleteBook)

]
