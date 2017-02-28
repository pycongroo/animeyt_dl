from	django.conf.urls	import	url
from	.	import	views

urlpatterns	=	[
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search_list, name='search_list'),
    url(r'^img/poster/(?P<name>\w{0,50}.jpeg)$', views.serve_image, name='serve_image'),
    url(r'^img/poster/(?P<name>\w{0,50}.jpg)$', views.serve_image, name='serve_image'),
    url(r'^prueba$', views.prueba),
]
