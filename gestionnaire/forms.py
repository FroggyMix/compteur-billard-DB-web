from django import forms
from django.core.exceptions import ValidationError
from .models import JeuVariantes, Joueur, Frame, Match
from django.contrib.admin import widgets									   
from django.contrib import admin									
from datetime import datetime
 
 
class JoueurForm(forms.ModelForm):

	class Meta:
		model = Joueur
		fields = ['nom','prenom','email']
		#fields = '__all__'
		#exclude = ['d_creation']
		print ("definition de JoueurForm")
 
	def clean_nom(self):
		nom = self.cleaned_data['nom']
		nom_l = nom.lower()
		if nom_l == "admin" or nom_l == "author":
			raise ValidationError("Le nom du joueur ne peut pas être 'admin/author'")
		return nom_l

	def clean_prenom(self):
		prenom = self.cleaned_data['prenom']
		prenom_l = prenom.lower()
		if prenom_l == "admin" or prenom_l == "author":
			raise ValidationError("Le prenom du joueur ne peut pas être 'admin/author'")
		return prenom_l

 
	def clean_email(self):
		return self.cleaned_data['email'].lower()
		
class JeuVariantesForm(forms.ModelForm):
	class Meta:
		model = JeuVariantes
		fields = '__all__'
 
	def clean_slug(self):
		return self.cleaned_data['slug'].lower()

class MatchForm(forms.ModelForm):

	#d_debut = forms.SplitDateTimeField(widget= widgets.AdminSplitDateTime(),label='Début du match',initial=datetime.now)
	class Meta:
		model = Match
		exclude = ['d_debut','d_fin','scorem_j1','scorem_j2','en_cours']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.fields['jeu_variante'].queryset = JeuVariantes.objects.none()
		self.fields['jeu_variante'].queryset = JeuVariantes.objects.filter(jeu_type="fr").order_by('ordre')
		if 'jeu_type' in self.data:
			try:
				jeu_type_id = self.data.get('jeu_type')
				self.fields['jeu_variante'].queryset = JeuVariantes.objects.filter(jeu_type=jeu_type_id).order_by('ordre')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['jv'].queryset = self.instance.jeu_type.jv_set.order_by('ordre')
			#JeuVariantes.objects.filter(self.instance.jeu_type).order_by('nom')
	def clean(self):
		super(MatchForm, self).clean()
		dist_j1 = self.cleaned_data.get('fr_distance_j1')
		dist_j2 = self.cleaned_data.get('fr_distance_j2')
		dist_rep = self.cleaned_data.get('fr_limite_nb_reprises')
		if (dist_j1 == dist_j2 == dist_rep == 0) or (not dist_j1 and not dist_j2 and not dist_rep) :
			self.add_error('fr_distance_j1', "distance J1, distance J2 et Distance Reprise ne peuvent être tous les 3 nuls") #erreur associée à un champ
			self.add_error('fr_distance_j2', "distance J1, distance J2 et Distance Reprise ne peuvent être tous les 3 nuls") #erreur associée à un champ
			self.add_error('fr_limite_nb_reprises', "distance J1, distance J2 et Distance Reprise ne peuvent être tous les 3 nuls") #erreur associée à un champ
			raise ValidationError("Il y'a un erreur de cohérence sur les distances de jeu, cf. ci-dessous") #erreur en tête de formulaire
		if ((dist_j1 == 0 or not dist_j1) and (dist_j2>0)) or ((dist_j2 == 0 or not dist_j2) and (dist_j1>0)):
			self.add_error('fr_distance_j1', "soit les deux joueurs ont une distance, soit aucun") #erreur associée à un champ
			self.add_error('fr_distance_j2', "soit les deux joueurs ont une distance, soit aucun") #erreur associée à un champ
			raise ValidationError("Il y'a un erreur de cohérence sur les distances des joueurs, cf. ci-dessous") #erreur en tête de formulaire
		