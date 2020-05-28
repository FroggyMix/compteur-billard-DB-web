from django.conf.urls import url
from gestionnaire import views
from django.urls import path
from django.contrib.flatpages import views as flat_views #pour les static pages
 
urlpatterns = [
#    path('time/', views.today_is, name='todays_time'),
#    url(r'^$', views.index, name='gestionnaire_index'),
	url(r'^(?P<pk>\d+)/$', views.match_detail, name='match_detail'), #tout ce qui s'ecrit ip/n/ appellera post match_detail(request, id=n)
	url(r'^$', views.frame_liste, name='frame_liste'),
	url(r'^joueur_liste/$', views.joueur_liste, name='joueur_liste'),
	url(r'^joueur/(?P<pk>\d+)/(?P<joueur_nom>[\w\d-]+)_(?P<joueur_prenom>[\w\d-]+)$', views.joueur_detail, name='joueur_detail'),
	url(r'^jv_detail/(?P<jv_slug>[\w-]+)/$', views.jv_detail, name='jv_detail'),
	url(r'^jv_liste/$', views.jv_liste, name='jv_liste'),
	url(r'match_liste/$',views.match_liste, name='match_liste' ),
	url(r'matchs/$',views.match_redirect, name='match_redirect' ),
	#url(r'^joueur/(?P<pk>\d+)/$', views.joueur_detail, name='joueur_detail'),
	url(r'frame_liste/$',views.frame_liste, name='frame_liste'),
]	
# Admin part
urlpatterns += [
	url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^admin_page/$', views.admin_page, name='admin_page')
]

#Static pages
urlpatterns += [
	url(r'^about/$', flat_views.flatpage, {'url': '/about/'}, name='about'),
]

# Frame_live
urlpatterns += [
	url(r'^frame/(?P<frame_id>\d+)/$',views.frame_live,name='frame_live'),
]

#Debuugage menu
urlpatterns += [
	url(r'^base/$',views.base,name='base'),
]

#Ajax service pour chargement dynamique des formulaure
urlpatterns += [
	path('ajax/load-jv/', views.load_jv, name='ajax_load_jv'),
]