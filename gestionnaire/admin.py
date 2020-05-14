from django.contrib import admin
from . import models
 
# Register your models here.
class JoueurAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom', 'email', 'd_creation', 'moyenne_FR_libre')
	search_fields = ['nom', 'prenom', 'email']
	ordering = ['nom']
	list_filter = ['nom']
	date_hierarchy = 'd_creation'
	#prepopulated_fields = {'slug': ('nom','prenom','id',)}
	readonly_fields = ('moyenne_FR_libre',)
	def moyenne_FR_libre(self,obj):
		return obj.moyenne('fr','Libre')
	moyenne_FR_libre.admin_order_field='joueur__moyenne'

class FrameAdmin(admin.ModelAdmin):
	list_display = ('pk', 'match', 'num','d_debut', 'd_fin', 'frame_score')
	search_fields = ['pk', 'match', 'num']
	ordering = ['-pk']
	list_filter = ['match']
	date_hierarchy = 'd_debut'
	def frame_score(self,obj):
		return f'{obj.scoref_j1()}' +" - " + f'{obj.scoref_j2()}'
	frame_score.admin_order_field='match__jeu_type'
	
class MatchAdmin(admin.ModelAdmin):
	list_display = ('pk', 'joueur1', 'joueur2', 'jeu_type', 'jeu_variante','nb_frames','d_debut','d_fin')
	search_fields = ['joueur1', 'joueur2', 'jeu_type']
	ordering = ['-pk']
	list_filter = ['jeu_type']
	date_hierarchy = 'd_debut'
class FrameEventAdmin(admin.ModelAdmin):
	list_display = ('frame', 'EventType_name', 'points', 'crediteur', 'origine','d_horodatage')
	search_fields = ['frame', 'event_type', 'origine']
	ordering = ['-d_horodatage']
	list_filter = ['event_type', 'origine']
	date_hierarchy = 'd_horodatage'
	def EventType_name(self,obj):
		return obj.event_type.nom
	EventType_name.admin_order_field='event_type__name'	
class EventTypeAdmin(admin.ModelAdmin):
	list_display = ('nom', 'jeu_type', 'description')
	search_fields = ['nom', 'jeu_type', 'description']
	ordering = ['nom']
	list_filter = ['jeu_type']


 
admin.site.register(models.JeuVariantes)
admin.site.register(models.Match,MatchAdmin)
admin.site.register(models.Frame,FrameAdmin)
admin.site.register(models.Joueur, JoueurAdmin)
admin.site.register(models.EventType,EventTypeAdmin)
admin.site.register(models.FrameEvent,FrameEventAdmin)

