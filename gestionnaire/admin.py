from django.contrib import admin
from . import models
 
# Register your models here.

class JoueurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'd_creation')
    search_fields = ['nom', 'prenom', 'email']
    ordering = ['nom']
    list_filter = ['nom']
    date_hierarchy = 'd_creation'
    #prepopulated_fields = {'slug': ('nom','prenom','id',)}
 
admin.site.register(models.JeuVariantes)
admin.site.register(models.Match)
admin.site.register(models.Frame)
admin.site.register(models.Joueur, JoueurAdmin)
admin.site.register(models.EventType)
admin.site.register(models.FrameEvent)


