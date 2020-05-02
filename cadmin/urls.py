from django.conf.urls import url, include
from . import views
 
urlpatterns = [
    url(r'^joueur/add/$', views.joueur_add, name='joueur_add'),
    url(r'^match/add/$', views.match_add, name='match_add'),
    url(r'^JeuVariante/add/$', views.jv_add, name='jv_add'),
	url(r'^joueur/update/(?P<pk>[\d]+)/$', views.joueur_update, name='joueur_update'),
	url(r'^match/update/(?P<pk>[\d]+)/$', views.match_update, name='match_update'),
	url(r'^jeuvariante/update/(?P<slug>[\w-]+)/$', views.jv_update, name='jv_update'),
]
