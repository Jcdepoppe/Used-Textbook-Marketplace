from django.conf.urls import url
from . import views     
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
	url(r'^$', views.index),
	###### BOOKS FOR SALE ###############
	url(r'^sell/(?P<id>\d+)/show$', views.show_sell),
	url(r'^sell$', views.sell_book),
	url(r'^sell/process$', views.sell_book_process),
	url(r'^sell/(?P<id>\d+)/edit$', views.edit_sell),
	url(r'^sell/(?P<id>\d+)/delete$', views.delete_sell),
	######## BOOKS WISHLIST ##############
	url(r'^want/(?P<id>\d+)/show$', views.show_want),
	url(r'^want$', views.want_book),
	url(r'^want/process$', views.want_book_process),
	url(r'^want/(?P<id>\d+)/edit$', views.edit_want),
	url(r'^want/(?P<id>\d+)/delete$', views.delete_want),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
