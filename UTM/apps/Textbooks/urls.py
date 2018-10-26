from django.conf.urls import url
from . import views     
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
	url(r'^$', views.index),
	#Do we still need this add url?
	url(r'^add$', views.addNewbook),
	################################
	###### BOOKS FOR SALE ###############
	url(r'^sell/(?P<id>\d+)/show$', views.show_sell, name='show_sell'),
	url(r'^sell$', views.sell_book),
	url(r'^sell/process$', views.sell_book_process),
	url(r'^sell/(?P<id>\d+)/edit$', views.edit_sell),
	url(r'^sell/update$', views.update_sell),
	url(r'^sell/(?P<id>\d+)/delete$', views.delete_sell),
	######## BOOKS WISHLIST ##############
	url(r'^want/(?P<id>\d+)/show$', views.show_want, name='show_want'),
	url(r'^want$', views.want_book),
	url(r'^want/process$', views.want_book_process),
	url(r'^want/update', views.want_book_update),
	url(r'^want/(?P<id>\d+)/edit$', views.edit_want),
	url(r'^want/(?P<id>\d+)/delete$', views.delete_want),


	# Can the wishlist and for sale messages/comments be used by the same route? #
	url(r'^message$', views.message, name = 'message'),
	url(r'^comment$', views.comment, name = 'comment'),
	##############################################################################

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
