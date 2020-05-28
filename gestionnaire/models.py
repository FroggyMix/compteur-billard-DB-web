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
from datetime import datetime
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator 


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
	TYPE_JEU = (
		('fr', 'Carambole'),
		('sn', 'Snooker'),
		('po', 'Pool'),
		('us', 'Américain')
	)
	jeu_type = models.CharField(max_length=2, choices=TYPE_JEU, verbose_name='Type de jeu', default='fr')
	slug = models.SlugField(max_length=100, unique=True)
	description = models.CharField(max_length=128, blank=True)
	regles = models.CharField(max_length=512, blank=True, help_text='Permet de résumer les règles')
	regles_url = models.URLField(blank=True, verbose_name='Lien vers les règles', help_text='Permet de renvoyer vers un site décrivant les règles')
	#code = models.CharField(max_length=64, null=True, blank=True)
	ordre = models.SmallIntegerField(default=1,verbose_name="Ordre d'affichage",help_text='Ordre dans lequel les variantes seront affichées')
	class Meta:
		db_table = 'Jeu_Variantes'
		verbose_name_plural = "JeuVariantesModel"
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets Book dans la base de données."""
		return self.slug
	def get_absolute_url(self):
		return reverse('jv_detail', args=[self.slug])

###########  J O U E U R  #############
class Joueur(models.Model):
	nom = models.CharField(max_length=32, blank=True)
	prenom = models.CharField(max_length=32)
	email = models.EmailField(max_length=128, unique=True,)
	d_creation = models.DateTimeField(default=timezone.now,verbose_name='date d\'inscription')
	joueur_actif = models.IntegerField(blank=True,null=True) #A QUOI SERT CE CHAMP (vide= aucun, 1= joueur1, 2= joueur2)
	
	def fullname(self):
		return "{p} {n}".format(p=self.prenom.title(),n=self.nom.upper())
	def fullname_score_board(self):
		return construit_nom(self.prenom.title(),self.nom.upper(),15)
	def moyenne(self,jt,jv):
		### Retourne la moyenne des moyennes des frames jouées poar le joueur
		### dans le type de jeu et vaiante fournis
		### Retourne : vide si pas de frame trouvée, la moyenne sinon
		fj1=Frame.objects.filter(match__jeu_type=jt, match__jeu_variante__nom=jv, match__joueur1=self, d_fin__isnull=False)
		fj2=Frame.objects.filter(match__jeu_type=jt, match__jeu_variante__nom=jv, match__joueur2=self, d_fin__isnull=False)
		nbf=0
		somme_moyennes=0
		for f in fj1:
			somme_moyennes += f.moyennef_j1()
			nbf +=1
		for f in fj2:
			somme_moyennes += f.moyennef_j2()
			nbf +=1
		return round(somme_moyennes/nbf,3) if nbf>0 else ""
	class Meta:
		db_table = 'Joueur'
		verbose_name_plural = "JoueurModel"
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		return f'{self.prenom} {self.nom}'
	def get_absolute_url(self):
		return reverse('joueur_detail', args=[self.pk, slugify(self.nom), '_'+self.prenom])

###########  M A T C H #############
class Match(models.Model):
	d_debut = models.DateTimeField(verbose_name='Début réel du match',blank=True, null=True)
	d_fin = models.DateTimeField(verbose_name='Fin réel du match',blank=True, null=True)
	joueur1 = models.ForeignKey(Joueur,default=1,related_name='joueur1', on_delete=models.PROTECT, verbose_name='Joueur 1',db_column='joueur1_id')
	joueur2 = models.ForeignKey(Joueur,default=1,related_name='joueur2', on_delete=models.PROTECT, verbose_name='Joueur 2',db_column='joueur2_id')
	TYPE_JEU = (
		('fr', 'Carambole'),
		('sn', 'Snooker'),
		('po', 'Pool'),
		('us', 'Américain')
	)
	jeu_type = models.CharField(max_length=2, choices=TYPE_JEU, verbose_name='Type de jeu', default='fr')
	jeu_variante = models.ForeignKey(JeuVariantes,default=5, on_delete=models.PROTECT,verbose_name='Variante de jeu', db_column='Jeu_Variantes_id')	# Field name made lowercase.
	nb_frames = models.SmallIntegerField(default=3,verbose_name='Nombre de frames',help_text='Nombre de frames maximum à jouer dans ce match',
			validators=[MaxValueValidator(100,message="Le nombre de frame doit être inférieur à 100"),MinValueValidator(1,message="Le nombre de frame doit être supérieur ou égal à 1")])
	shot_time_limit = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name='Temps max par coup (sec)',help_text='Durée maximum pour réaliser un coup (0 = pas de limite)',
			validators=[MinValueValidator(0,message="Le temps doit être un nombre positif")])
	fr_distance_j1 = models.SmallIntegerField(default=10,blank=True, null=True,verbose_name='Distance joueur 1',help_text='Optionnel, ne concerne que la carambole',
			validators=[MinValueValidator(1,message="La distance doit être un nombre positif")])
	fr_distance_j2 = models.SmallIntegerField(default=10,blank=True, null=True,verbose_name='Distance joueur 2',help_text='Optionnel, ne concerne que la carambole',
			validators=[MinValueValidator(1,message="La distance doit être un nombre positif")])
	fr_limite_nb_reprises = models.SmallIntegerField(default=10,blank=True, null=True,verbose_name='Limite du nombre de reprises',help_text='Optionnel, ne concerne que la carambole',
			validators=[MinValueValidator(1,message="Le nombre de reprises doit être un nombre positif")])
	fr_reprise_egalisatrice = models.BooleanField(default=True)	

	def fullname_j1(self): #lecture
		return "{p} {n}".format(p=self.joueur1.prenom.title(),n=self.joueur1.nom.upper())
	def fullname_j2(self): #lecture
		return "{p} {n}".format(p=self.joueur2.prenom.title(),n=self.joueur2.nom.upper())
	def fullname_score_board_j1(self): #lecture
		return construit_nom(self.joueur1.prenom.title(),self.joueur1.nom.upper(),15)
	def fullname_score_board_j2(self): #lecture
		return construit_nom(self.joueur2.prenom.title(),self.joueur2.nom.upper(),15)
	def reprises_limitees(self): #lecture
		return  (self.fr_limite_nb_reprises is not None)
	def besoin_de_reprise_egalisatrice(self): #lecture
		return (self.fr_limite_nb_reprises is not None or self.fr_reprise_egalisatrice)	
	def scorem_j1(self): #lecture
		return FrameEvent.objects.filter(frame__in=Frame.objects.filter(match=self)).filter(crediteur=1, event_type__nom='victoire-frame').count()
	def scorem_j2(self): #lecture
		return FrameEvent.objects.filter(frame__in=Frame.objects.filter(match=self)).filter(crediteur=2, event_type__nom='victoire-frame').count()
	def dureem_reelle(self): #lecture
		dureeM=0
		for f in Frame.objects.filter(match=self):
			dureeM = dureeM + f.dureef_reelle_en_secondes()
		str_duree=str(datetime.timedelta(seconds=dureeM))
		str_duree=str_duree.split(":")
		for i in range(3):
			if len(str_duree[i]) ==1 :str_duree[i]="0"+str_duree[i]
		#str_duree=str_duree[0]+":"+str_duree[1]+":"+str_duree[2]
		str_duree=str_duree[0]+":"+str_duree[1]
		
		return str_duree#str(datetime.timedelta(seconds=dureeM))
	def vainqueurm(self): #lecture
		### Renvoie : 	-1 si le match n'est pas encore terminé
		###				1 ou 2 si un des joueurs a gangé
		fr = Frame.objects.filter(match=self).order_by('-num').first()
		vq = FrameEvent.objects.filter(event_type__nom='victoire-match',frame=fr).values_list('crediteur',flat=True).first()
		if not vq is None:
				return vq
		else:
			return -1		
	def match_termine(self): #ECRITURE
		if self.d_fin is None:	
			objectif = self.nb_frames // 2 +1
			vainqueurm = 0			
			if self.scorem_j1() >= objectif: vainqueurm=1
			if self.scorem_j2() >= objectif: vainqueurm=2
			if vainqueurm > 0:
				#c'est la fin du match
				if self.d_fin is None: 
					Match.objects.filter(pk=self.pk).update(d_fin=timezone.localtime(timezone.now()))
					# print('[M{}] Le joueur {} remporte la frame'.format(self.pk,vainqueurm))
				#on determine la frame du match dans laquelle il faut ecrire la fin de match
				fr = Frame.objects.filter(match=self).order_by('-num').first()
				if not fr.frameevent_exists('victoire-match'):
					fr = Frame.objects.filter(match=self).order_by('-num').first()
					fr.ajoute_evt('victoire-match',vainqueurm)
					#FrameEvent.objects.create(event_type=EventType.objects.get(nom='victoire-match'),frame=fr,crediteur=vainqueurm)
	def score_match_dans_framelive(self):
		return "{} ({}) {}".format(self.scorem_j1(),self.nb_frames,self.scorem_j2())
	def debutem(self): #ECRITURE
		if not self.d_debut : Match.objects.filter(pk=self.pk).update(d_debut=timezone.localtime(timezone.now()))

	class Meta:
		db_table = 'Match'
		verbose_name_plural = "MatchModel"
		ordering = ['-pk']
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		#return "{} / le {} : {} vs {} ({} - {})".format(self.id,self.d_debut.strftime('%d %m %y'),{self.joueur1},{self.joueur2},self.jeu_type,self.jeu_variante)
		return f'{self.id} : {self.joueur1} vs {self.joueur2} ({self.jeu_type} - {self.jeu_variante})'
	def get_absolute_url(self):
		return reverse('match_detail', args=[self.pk])
	def save(self, *args, **kwargs):
		creer_frame = self._state.adding
		super(Match, self).save(*args, **kwargs)
		if creer_frame:
			Frame.objects.create(match=self,num=1)#Test pour éviter que quand on modifie un match depuis l'admin ça declenche aussi save !!!
				
###########  F R A M E #############
class FrameManager(models.Manager):
	def frame_en_cours(self): # A appeler en ecrivant : Frame.objects.frame_en_cours()
		return Frame.objects.filter(~Q(d_debut=None) & Q(d_fin=None))
	def frame_terminee(self):
		return Frame.objects.filter(d_fin__isnull=False).order_by('-d_fin')[0:5]
	def frame_a_venir(self): # A appeler en ecrivant : Frame.objects.frame_a_venir()		
		l=Frame.objects.filter(d_debut=None).values('match').annotate(idmin=Min('id')).values_list('idmin')
		l2=list(zip(*l))
		if l2:
			return Frame.objects.filter(pk__in=l2[0])
		else:
			return None
		
class Frame(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE, db_column='Match_id')  # Field name made lowercase.
	d_debut = models.DateTimeField(blank=True, null=True)
	d_fin = models.DateTimeField(blank=True, null=True)
	num = models.SmallIntegerField(default=1,verbose_name='N° de frame dans le match')
		
	objects=FrameManager()# Custom manager
	
	class Meta:
		db_table = 'Frame'
		verbose_name_plural = "FrameModel"
		ordering = ['-match__id','-num']
		
	def __str__(self):
		dateM= ''
		if self.d_debut is not None: dateM=f'({self.d_debut.strftime("%d/%m/%y")})'
		return f'Match {self.match_id} frame {self.id} : {self.match.joueur1.prenom.capitalize()} {self.match.joueur1.nom.upper()} vs {self.match.joueur2.prenom.capitalize()} {self.match.joueur2.nom.upper()} {dateM}'
	def get_absolute_url(self): #lecture
		return reverse('frame_live', args=[self.pk])	
	def scoref_j1(self): #lecture
		#score = FrameEvent.objects.filter(frame=self,crediteur=1,event_type__nom='score').values('points').aggregate(Sum('points'))['points__sum'] 
		score = FrameEvent.objects.filter((Q(event_type__nom='score') | Q(event_type__nom='correction')),frame=self, crediteur=1).values('points').aggregate(Sum('points'))['points__sum'] 
		return 0 if score is None else score
	def scoref_j2(self): #lecture
		score = FrameEvent.objects.filter((Q(event_type__nom='score') | Q(event_type__nom='correction')),frame=self, crediteur=2).values('points').aggregate(Sum('points'))['points__sum'] 		
		return 0 if score is None else score	
	def moyennef_j1(self):#lecture
		nb_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass',crediteur=1).count()
		breakj = self.break_en_cours() if self.joueur_actif()==1 else 0		
		return round((self.scoref_j1() - breakj) / nb_pass,3) if nb_pass > 0 else 0
	def moyennef_j2(self):#lecture
		nb_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass',crediteur=2).count()
		breakj = self.break_en_cours() if self.joueur_actif()==2 else 0		
		return round((self.scoref_j2() - breakj) / nb_pass,3) if nb_pass > 0 else 0
	def dureef_reelle_en_secondes(self):  #lecture
		if self.d_debut:
			if self.d_fin:
				return round((self.d_fin - self.d_debut).total_seconds(),0)
			else:
				return round((timezone.localtime(timezone.now()) - self.d_debut).total_seconds(),0)				
		else:
			return 0	
	def break_en_cours(self): #lecture
		## Est la somme des points marqués depuis le dernier changement de joueur(pass)
		liste_derniers_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass').order_by('-d_horodatage')
		if not liste_derniers_pass:
			return 0
		else:
			horo_dernier_pass = liste_derniers_pass.first().d_horodatage
			break_j = FrameEvent.objects.filter(frame=self, event_type__nom='score',d_horodatage__gt=horo_dernier_pass).values('points').aggregate(Sum('points'))['points__sum']
			return 0 if break_j is None else break_j		
	def reprise(self): #lecture
		## Est la somme Event=pass du joueur 2 +1 ou du joueur 1 si c'est j2 qui a débuté
		flag = 1 if self.vainqueurf() != -1 else 0
		frame1=Frame.objects.get(match=self.match, num=1)################
		toss_frame1 = FrameEvent.objects.filter(frame=frame1,event_type__nom='toss-engage').order_by('-d_horodatage').values_list("crediteur",flat=True).first()
		if toss_frame1 is not None:
			engageur = (((toss_frame1 + self.num) % 2) + 1)
			correction = FrameEvent.objects.filter(event_type__nom='correction',frame=self, crediteur=0).values('points').aggregate(Sum('points'))['points__sum']  
			if not correction : correction=0
			if engageur == 1:
				return FrameEvent.objects.filter(frame=self,crediteur=2,event_type__nom='pass').count()+1-flag + correction 
			elif engageur == 2:
				return FrameEvent.objects.filter(frame=self,crediteur=1,event_type__nom='pass').count()+1-flag + correction 
			else: return -1
		else:
			return 1 #le match (donc la frame) n'a pas encore commencé			
	def engageur_frame(self): #lecture
		frame1=Frame.objects.get(match=self.match, num=1)
		toss_frame1 = FrameEvent.objects.filter(frame=frame1,event_type__nom='toss-engage').order_by('-d_horodatage')
		if (self.num%2) == 0: #le numéro de frame est paire
			return 3-toss_frame1.first().crediteur
		else: #le numéro de frame est impaire
			return toss_frame1.first().crediteur			
	def frameevent_exists(self,evt): #lecture
		list = FrameEvent.objects.filter(frame=self,event_type__nom=evt).count()
		return True if list else False 
	def joueur_actif(self): #lecture
		liste_event_pass = FrameEvent.objects.filter(frame=self,event_type__nom='pass').order_by('-d_horodatage')
		liste_event_toss = FrameEvent.objects.filter(frame=self,event_type__nom='toss-engage').order_by('-d_horodatage')
		if self.num == 1:
			if liste_event_pass:
				return 3-liste_event_pass.first().crediteur	
			elif liste_event_toss:
				return liste_event_toss.first().crediteur
			else:
				if self.num ==1:
					return 0
				else:
					return self.engageur_frame()
		else:
			if liste_event_pass:
				return 3-liste_event_pass.first().crediteur	
			else:
				return self.engageur_frame()
	def vainqueurf(self): #lecture
		### Renvoie : 	-1 si la frame n'est pas encore terminé
		###				0 en cas d'égalité
		###				1 ou 2 si un des joueurs a gangé
		vainqueur = FrameEvent.objects.filter(frame=self,event_type__nom='victoire-frame').values_list('crediteur',flat=True)
		if vainqueur.first() is not None:
			return vainqueur.first()
		else:
			return -1
	def reprise_egalisatrice_detecte(self): #ECRITURE
		dernier_evt = FrameEvent.objects.filter(frame=self).order_by('-d_horodatage').values_list('event_type__nom',flat=True).first()
		if dernier_evt == 'pass':
			if self.match.reprises_limitees():
				# print('>>>>> match à Reprise limitée')
				dist1 = 999999 if not self.match.fr_distance_j1 else self.match.fr_distance_j1
				dist2 = 999999 if not self.match.fr_distance_j2 else self.match.fr_distance_j2
				if self.scoref_j1() < dist1 and self.scoref_j2() < dist2 and self.reprise() >= self.match.fr_limite_nb_reprises:
					print('>> Aucun joueur na atteint sa cible mais la reprise sa limite')
					if self.joueur_actif() == self.engageur_frame():
						#On informe que le joueur actif joue son dernier coup
						if not self.frameevent_exists('dernier-coup'):
							#FrameEvent.objects.create(event_type=EventType.objects.get(nom='dernier-coup'),frame=self,crediteur=self.joueur_actif())
							self.ajoute_evt('dernier-coup',self.joueur_actif())
						return "prochain"
					else:
						#On enregistre et informe de la reprise égalisatrice (à consition quelle n'ait pas déjà été enregistrée)
						if not self.reprise_egalisatrice_existe(): 
							self.ajoute_evt('reprise-egalisatrice',self.joueur_actif())
							#FrameEvent.objects.create(event_type=EventType.objects.get(nom='reprise-egalisatrice'),frame=self,crediteur=self.joueur_actif())
							return "maintenant"			
			score_engageur = self.scoref_j1() if self.engageur_frame()==1 else self.scoref_j2()
			if self.engageur_frame()==1:
				dist_engageur = self.match.fr_distance_j1 if self.match.fr_distance_j1 else 999999
			else:
				dist_engageur = self.match.fr_distance_j2 if self.match.fr_distance_j2 else 999999
				
			if self.match.besoin_de_reprise_egalisatrice() and score_engageur >= dist_engageur:
				print('>> match à Reprise egalisatrice avec engageur qui a atteint son score')				
				if not self.reprise_egalisatrice_existe():
					#FrameEvent.objects.create(event_type=EventType.objects.get(nom='reprise-egalisatrice'),frame=self,crediteur=self.joueur_actif())
					self.ajoute_evt('reprise-egalisatrice',self.joueur_actif())
					return "maintenant"	
		if dernier_evt == 'reprise-egalisatrice':
			#print('Dernier evt = REG => on envoie maintenant')
			return "maintenant"		
	def reprise_egalisatrice_existe(self): #lecture
		return  not (FrameEvent.objects.filter(frame=self,event_type__nom='reprise-egalisatrice').count() == 0)			
	def frame_terminee(self): #ECRITURE
		### Renvoie 
		dernier_evt = FrameEvent.objects.filter(frame=self).order_by('-d_horodatage').values_list('event_type__nom',flat=True).first()
		joueur_vainqueur=''
		if (FrameEvent.objects.filter(frame=self,event_type__nom='victoire-frame').count() == 0):
			if dernier_evt == "pass" and self.vainqueurf() == -1:
				id_autre = 3-self.engageur_frame()
				if id_autre == 1:
					score_autre = self.scoref_j1()
					dist_autre = 999999 if not self.match.fr_distance_j1 else self.match.fr_distance_j1
				else:
					score_autre = self.scoref_j2()
					dist_autre = 999999 if not self.match.fr_distance_j2 else self.match.fr_distance_j2
				if (self.match.besoin_de_reprise_egalisatrice() and self.reprise_egalisatrice_existe()) or not self.match.besoin_de_reprise_egalisatrice():
					dist1 = 999999 if not self.match.fr_distance_j1 else self.match.fr_distance_j1
					dist2 = 999999 if not self.match.fr_distance_j2 else self.match.fr_distance_j2
					if self.scoref_j1() >= dist1 and self.scoref_j2() < dist2: 
						joueur_vainqueur=1
					elif self.scoref_j1() < dist1 and self.scoref_j2() >= dist2: 
						joueur_vainqueur=2
					else: 
						# On compare les moyennes
						print('comparaison des moyennes')
						print('J1 : ',self.scoref_j1()/dist1)
						print('J2 : ',self.scoref_j2()/dist2)
						if self.scoref_j1()/dist1 > self.scoref_j2()/dist2: joueur_vainqueur=1
						elif self.scoref_j1()/dist1 < self.scoref_j2()/dist2: joueur_vainqueur=2
						else : joueur_vainqueur=0
				if (self.match.besoin_de_reprise_egalisatrice() and score_autre >= dist_autre and not self.reprise_egalisatrice_existe()): joueur_vainqueur = id_autre
			if self.frameevent_exists("concedeF"):
				joueur_vainqueur = 3 - FrameEvent.objects.filter(frame=self,event_type__nom='concedeF').values_list('crediteur',flat=True).first()
			if joueur_vainqueur != "":
				#on insere un évenement victoire-frame
				self.ajoute_evt('victoire-frame',joueur_vainqueur)
				#FrameEvent.objects.create(event_type=EventType.objects.get(nom='victoire-frame'),frame=self,crediteur=joueur_vainqueur)
				#on insere une fin de frame
				Frame.objects.filter(pk=self.pk).update(d_fin=timezone.localtime(timezone.now()))
				#on insere une nouvelle frame avec num+=1 si le match n'est pas fini
				self.match.match_termine()
				#print('[M{}-F{}] Le joueur {} remporte la frame'.format(self.match.pk,self.pk,joueur_vainqueur))
				if self.match.vainqueurm() < 1: Frame.objects.create(match=self.match,num=self.num+1)
	def reprise_egalisatrice(self):
		dernier_evt = FrameEvent.objects.filter(frame=self).order_by('-d_horodatage').values_list('event_type__nom',flat=True).first()
		if dernier_evt == 'reprise-egalisatrice':
			return "maintenant"		
		if dernier_evt == "dernier-coup":
			return "prochain"		
	def dureef(self): #lecture
		#### Cette fonction a été changée pour renvoyer unde durée : il faut changer son nom ainsi que dans frame_state qui l'appelle
		if self.d_debut:
			return str(datetime.timedelta(seconds=self.dureef_reelle_en_secondes()))
		else: return "00:00:00"		
	def debutant(self): #lecture
		f=FrameEvent.objects.filter(frame=self,event_type__nom='toss-engage')
		if not f:
			return -1
		else:
			return f.values_list("crediteur",flat=True)[0]
	def next_frame_existe(self): #lecture
		f=Frame.objects.filter(match=self.match, num=self.num+1)
		if f:
			return f.first().pk;
	def undo_last_event(self): #ECRITURE
		dernier_evt = FrameEvent.objects.filter(frame=self).order_by('-d_horodatage').first()
		if dernier_evt: dernier_evt.undo()
	def correction_score(self, crediteur, montant): #ECRITURE
		###Additionne montant points(accepte les negatifs) au créditeur(0, 1 ou 2)
		FrameEvent.objects.create(event_type=EventType.objects.get(nom='correction'),frame=self,crediteur=crediteur,points=montant)	
	def ajoute_evt(self,evt,crediteur=0,points=""): #ECRITURE
		temp=FrameEvent.objects.insere_evt(self,evt,crediteur,points)
	def debutef(self): #ECRITURE
		if not self.d_debut : Frame.objects.filter(pk=self.pk).update(d_debut=timezone.localtime(timezone.now()))
###########  E V E N T   T Y P E #############
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
		if self.jeu_type!="":
			return f'{self.nom} ({self.jeu_type})'
		else:
			return f'{self.nom}'
	def get_absolute_url(self):
		return reverse('event_type', args=[self.pk])
###########  F R A M E E V E N T #############
class FrameEventManager(models.Manager):
	def insere_evt(self,frame,evt,crediteur=0,points=""):
		if points:
			FrameEvent.objects.create(event_type=EventType.objects.get(nom=evt),frame=frame,crediteur=crediteur,points=points)
		else:
			FrameEvent.objects.create(event_type=EventType.objects.get(nom=evt),frame=frame,crediteur=crediteur)
		print('EVT-[M{}-F{}] Joueur {} : {} '.format(frame.match.pk,frame.pk,crediteur,evt.upper()))
class FrameEvent(models.Model):
	frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
	crediteur = models.SmallIntegerField() # 0 = reprise ; 1=joueur1 ; 2=joueur2
	event_type = models.ForeignKey(EventType, on_delete=models.PROTECT)
	points = models.SmallIntegerField(blank=True, null=True)
	d_horodatage = models.DateTimeField(default=timezone.now)
	TYPE_ORIGINE = (
		('system', 'Système'),
		('user', 'Utilisateur'),
		('ia-image', 'IA-image'),
		('ia-son', 'IA-son')
		)
	origine = models.CharField(max_length=15, choices=TYPE_ORIGINE, verbose_name="Origine de l'enregistrement", default='system')
	objects=FrameEventManager()# Custom manager
	
	class Meta:
		db_table = 'FrameEvent'
		verbose_name_plural = "FrameEventModel"
		ordering = ['-d_horodatage']
	def __str__(self):
		"""Fonction requise par Django pour manipuler les objets dans la base de données."""
		return f'{self.frame} - {self.d_horodatage.strftime("%H:%M:%S")} - {self.crediteur} : {self.event_type} (+ {self.points}pts)'
	def get_absolute_url(self):
		return reverse('frame_event', args=[self.pk])
	def undo(self,profondeur=""): #ECRITURE		
		if profondeur: 
			FrameEvent.objects.filter(pk__in=FrameEvent.objects.filter(frame=self.frame).order_by('-d_horodatage').values_list('pk')[0:profondeur]).delete()
			print('EVT-[M{}-F{}] Annulation de {} (profondeur : {})'.format(self.frame.match.pk,self.frame.pk,self.event_type.nom.upper(),profondeur))
		elif self.event_type.nom in ["score", "pass","toss-engage","engage"]: self.undo(1)
		elif self.event_type.nom == "reprise-egalisatrice": self.undo(2)
		elif self.event_type.nom == "correction": pass
		elif self.event_type.nom in ["victoire-frame", "victoire-match"]:pass
			