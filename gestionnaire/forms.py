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
	d_debut = forms.SplitDateTimeField(widget= widgets.AdminSplitDateTime(),label='Début du match',initial=datetime.now)
    
	class Meta:
		model = Match
		exclude = ['d_fin','scorem_j1','scorem_j2','en_cours']
		