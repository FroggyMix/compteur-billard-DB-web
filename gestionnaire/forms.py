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
		print("jeu_type",self.data.get('jeu_type'))
		print("self.data = ",self.data)
		print("self.instance.pk = ",self.instance.pk)
		if 'jeu_type' in self.data:
			print(" jeu_type in self.data")
			try:
				jeu_type_id = self.data.get('jeu_type')
				#print("jeu_type_id = ",jeu_type_id)
				self.fields['jeu_variante'].queryset = JeuVariantes.objects.filter(jeu_type=jeu_type_id).order_by('ordre')
				print("self.fields['jeu_variante'].queryset = ",self.fields['jeu_variante'].queryset)
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			print('else')
			self.fields['jv'].queryset = self.instance.jeu_type.jv_set.order_by('ordre')
			#JeuVariantes.objects.filter(self.instance.jeu_type).order_by('nom')
	def clean_nb_frames(self):
		nbf = self.cleaned_data['nb_frames']
		#Finalement fait dans le models ! 
		#if not  1 <= nbf <= 100:
			# raise ValidationError("Le nombre de frames doit être compris entre 1 et 100")
			#self.add_error("nb_frames", "nb incorrect")
		return nbf
		