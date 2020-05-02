from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
import uuid
from django.db.models import F, Func
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q


# base =  Inspectdb de la version superlight de mysqlworkbench importé dans mariadb
# Retouche en fonction des tuto et doc Django

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	* Rearrange models' order
#	* Make sure each model has one field with primary_key=True
#	* Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#	* Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

def construit_nom(prenom,nom,taille_max):
	if len(nom) + len(prenom) > taille_max:
		return '{p}. {n}'.format(p=prenom[:1],n=nom[:taille_max-2])
	else:
		return "{p} {n}".format(p=prenom.title(),n=nom.upper())



class JeuVariantes(models.Model):
	#code = models.CharField(max_length=16, unique=True)
	nom = models.CharField(max_length=32, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	description = models.CharField(max_length=128, blank=True)
	regles = models.CharField(max_length=512, blank=True, help_text='Permet de résumer les règles')
	regles_url = models.URLField(blank=True, verbose_name='Lien vers les règles', help_text='Permet de renvoyer vers un site décrivant les règles')
	#code = models.CharField(max_length=64, null=True, blank=True)

	class Meta:
		db_table = 'Jeu_Variantes'
		verbose_name_plural = "JeuVariantesModel"
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets Book dans la base de données."""
		return self.slug
	def get_absolute_url(self):
		return reverse('jv_detail', args=[self.slug])

class Joueur(models.Model):
	nom = models.CharField(max_length=32, blank=True)
	prenom = models.CharField(max_length=32)
	email = models.EmailField(max_length=128, unique=True,)
	d_creation = models.DateTimeField(default=timezone.now,verbose_name='date d\'inscription')
	joueur_actif = models.IntegerField(blank=True,null=True) #vide= aucun, 1= joueur1, 2= joueur2
	
	def fullname(self):
		return "{p} {n}".format(p=self.prenom.title(),n=self.nom.upper())
	def fullname_score_board(self):
		return construit_nom(self.prenom.title(),self.nom.upper(),15)


	class Meta:
		db_table = 'Joueur'
		verbose_name_plural = "JoueurModel"
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		return f'{self.prenom} {self.nom}'
	# def save(self, *args, **kwargs):
		# self.slug = slugify(self.nom+self.prenom)
		# super(Post, self).save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('joueur_detail', args=[self.pk, slugify(self.nom), '_'+self.prenom])

class Match(models.Model):
	d_debut = models.DateTimeField(default=timezone.now,verbose_name='Début du match', help_text='laissez la valeur par défaut pour un démarrage immédiat')
	d_fin = models.DateTimeField(blank=True, null=True)
	joueur1 = models.ForeignKey(Joueur,related_name='joueur1', on_delete=models.PROTECT, verbose_name='Joueur 1',db_column='joueur1_id')
	joueur2 = models.ForeignKey(Joueur,related_name='joueur2', on_delete=models.PROTECT, verbose_name='Joueur 2',db_column='joueur2_id')
	TYPE_JEU = (
		('fr', 'Carambole'),
		('sn', 'Snooker'),
		('po', 'Pool'),
		('us', 'Américain')
	)
	jeu_type = models.CharField(max_length=2, choices=TYPE_JEU, verbose_name='Type de jeu', default='fr')
	jeu_variante = models.ForeignKey(JeuVariantes, on_delete=models.PROTECT,verbose_name='Variante de jeu', db_column='Jeu_Variantes_id')	# Field name made lowercase.
	nb_frames = models.SmallIntegerField(default=1,verbose_name='Nombre de frames',help_text='Nombre de frames maximum à jouer dans ce match')
	# scorem_j1 = models.SmallIntegerField(default=0,db_column='scoreM_J1', blank=True, null=True)	# Field name made lowercase.
	# scorem_j2 = models.SmallIntegerField(default=0,db_column='scoreM_J2', blank=True, null=True)	# Field name made lowercase.
	# en_cours = models.BooleanField(default='False', help_text='Indique si le match est en cours ou non')
	distanceFR_j1 = models.SmallIntegerField(blank=True, null=True,verbose_name='Distance joueur 1',help_text='Optionnel, ne concerne que la carambole')
	distanceFR_j2 = models.SmallIntegerField(blank=True, null=True,verbose_name='Distance joueur 2',help_text='Optionnel, ne concerne que la carambole')

	def fullname_j1(self):
		return "{p} {n}".format(p=self.joueur1.prenom.title(),n=self.joueur1.nom.upper())
	def fullname_j2(self):
		return "{p} {n}".format(p=self.joueur2.prenom.title(),n=self.joueur2.nom.upper())
	def fullname_score_board_j1(self):
		return construit_nom(self.joueur1.prenom.title(),self.joueur1.nom.upper(),15)
	def fullname_score_board_j2(self):
		return construit_nom(self.joueur2.prenom.title(),self.joueur2.nom.upper(),15)
	def scorem_j1(self):
		return '0'
	def scorem_j2(self):
		return '0'

	class Meta:
		db_table = 'Match'
		verbose_name_plural = "MatchModel"
		ordering = ['-d_fin']
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		#return "{} / le {} : {} vs {} ({} - {})".format(self.id,self.d_debut.strftime('%d %m %y'),{self.joueur1},{self.joueur2},self.jeu_type,self.jeu_variante)
		return f'{self.id} / le {self.d_debut.strftime("%d/%m/%y")} : {self.joueur1} vs {self.joueur2} ({self.jeu_type} - {self.jeu_variante})'
	def get_absolute_url(self):
		return reverse('match_detail', args=[self.pk])
	def save(self, *args, **kwargs):
		super(Match, self).save(*args, **kwargs)
		Frame.objects.create(match=self,d_debut=self.d_debut,num=1)

class FrameManager(models.Manager):
	def frame_en_cours(self): # A appeler en ecrivant : Frame.objects.frame_en_cours()
		return Frame.objects.filter(~Q(d_debut=None) & Q(d_fin=None))
	def frame_a_venir(self): # A appeler en ecrivant : Frame.objects.frame_a_venir()
		l=Frame.objects.filter(d_debut=None).values('match').annotate(idmin=Min('id')).values_list('idmin')
		l2=list(zip(*l))
		return Frame.objects.filter(pk__in=l2[0])
class Frame(models.Model):
	match = models.ForeignKey(Match, on_delete=models.PROTECT, db_column='Match_id')  # Field name made lowercase.
	d_debut = models.DateTimeField(blank=True, null=True)
	d_fin = models.DateTimeField(blank=True, null=True)
	num = models.SmallIntegerField(default=1,verbose_name='Numéro de la frame dans le match')

	objects=FrameManager()# Custom manager
	
	class Meta:
		db_table = 'Frame'
		verbose_name_plural = "FrameModel"
		
	def __str__(self):
		dateM= ''
		if self.d_debut is not None: dateM=f'({self.d_debut.strftime("%d/%m/%y")})'
		return f'Match {self.match_id} frame {self.id} : {self.match.joueur1.prenom.capitalize()} {self.match.joueur1.nom.upper()} vs {self.match.joueur2.prenom.capitalize()} {self.match.joueur2.nom.upper()} {dateM}'
	def get_absolute_url(self):
		return reverse('frame_live', args=[self.pk])	
	def scoref_j1(self):
		score = FrameEvent.objects.filter(frame=self,crediteur=1,event_type__nom='score').values('points').aggregate(Sum('points'))['points__sum'] 
		return 0 if score is None else score
	def scoref_j2(self):
		score = FrameEvent.objects.filter(frame=self,crediteur=2,event_type__nom='score').values('points').aggregate(Sum('points'))['points__sum'] 
		return 0 if score is None else score
	def break_en_cours(self):
		## Est la somme des points marqués depuis le dernier changement de joueur(pass)
		liste_derniers_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass').order_by('-d_horodatage')
		if not liste_derniers_pass:
			return 0
		else:
			horo_dernier_pass = liste_derniers_pass.first().d_horodatage
			break_j = FrameEvent.objects.filter(frame=self, event_type__nom='score',d_horodatage__gt=horo_dernier_pass).values('points').aggregate(Sum('points'))['points__sum']
			return 0 if break_j is None else break_j		
	def reprise(self):
		## Est la somme Event=pass du joueur 2 +1
		return FrameEvent.objects.filter(frame=self,crediteur=2,event_type__nom='pass').count()+1,
	def joueur_actif(self):
		liste_event_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass').order_by('-d_horodatage')
		if not liste_event_pass:
			return 1
		else:
			return 3-liste_event_pass.first().crediteur	
		return 1 if dernier_joueur_pass is None else 3-dernier_joueur_pass
	def heure_debut(self):
		return self.match.d_debut.strftime("%H:%M:%S")

class EventType(models.Model):
	nom = models.CharField(max_length=32, unique=True)
	TYPE_JEU = (
		('fr', 'Carambole'),
		('sn', 'Snooker'),
		('po', 'Pool'),
		('us', 'Américain')
	)
	jeu_type = models.CharField(max_length=2, choices=TYPE_JEU, default='fr', blank=True)
	description = models.CharField(max_length=256, blank=True)

	class Meta:
		db_table = 'EventType'
		verbose_name_plural = "EventTypeModel"
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets Book dans la base de données."""
		return f'{self.jeu_type} - {self.nom}'
	def get_absolute_url(self):
		return reverse('event_type', args=[self.pk])

class FrameEvent(models.Model):
	frame = models.ForeignKey(Frame, on_delete=models.PROTECT)
	crediteur = models.SmallIntegerField() # 0 = reprise ; 1=joueur1 ; 2=joueur2
	event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
	points = models.SmallIntegerField(blank=True, null=True)
	d_horodatage = models.DateTimeField(default=timezone.now)

	class Meta:
		db_table = 'FrameEvent'
		verbose_name_plural = "FrameEventModel"
		ordering = ['-d_horodatage']
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		return f'{self.frame} - {self.d_horodatage.strftime("%H:%M:%S")} - {self.crediteur} : {self.event_type} (+ {self.points}pts)'
	def get_absolute_url(self):
		return reverse('frame_event', args=[self.pk])