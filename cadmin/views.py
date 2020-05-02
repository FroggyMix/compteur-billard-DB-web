from django.shortcuts import render, redirect, get_object_or_404, reverse
from gestionnaire import models
from gestionnaire.models import Match, Joueur, JeuVariantes, Frame
from gestionnaire.forms import JoueurForm, MatchForm, JeuVariantesForm
from django.contrib import messages

# Create your views here.
 
def joueur_add(request):
	# If request is POST, create a bound form (form with data)
	print ("definition de joueur_add")
	if request.method == "POST":
		f = JoueurForm(request.POST)
		# If form is invalid show form with errors again
		if f.is_valid():
			#  save data to db
			f.save()
			messages.add_message(request, messages.INFO, 'Joueur ajouté.')
			return redirect('joueur_add')
	# if request is GET the show unbound form to the user
	else:
		print ("methode = GET")
		f = JoueurForm()
	return render(request, 'cadmin/joueur_add.html', {'form': f})

def joueur_update(request, pk):
	joueur = get_object_or_404(Joueur, pk=pk) 
	# If request is POST, create a bound form(form with data)
	if request.method == "POST":
		f = JoueurForm(request.POST, instance=joueur)
		# If form is invalid show form with errors again
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Joueur updated.')
			return redirect(reverse('joueur_update', args=[joueur.id])) 
	# if request is GET the show unbound form to the user, along with data
	else:
		f = JoueurForm(instance=joueur) 
	return render(request, 'cadmin/joueur_update.html', {'form': f, 'joueur': joueur})
	
def match_add(request):
	# If request is POST, create a bound form (form with data)
	if request.method == "POST":
		f = MatchForm(request.POST)
		if f.is_valid():
			#  save data to db
			f.save()
			messages.add_message(request, messages.INFO, 'Match ajouté.')
			return redirect('match_add')
	# if request is GET the show unbound form to the user
	else:
		f = MatchForm()
	return render(request, 'cadmin/match_add.html', {'form': f})

def match_update(request, pk):
	match = get_object_or_404(Match, pk=pk) 
	# If request is POST, create a bound form(form with data)
	if request.method == "POST":
		f = MatchForm(request.POST, instance=match)
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'Match updated.')
			return redirect(reverse('match_update', args=[match.id]))
	# if request is GET the show unbound form to the user, along with data
	else:
		f = MatchForm(instance=match)
	return render(request, 'cadmin/match_update.html', {'form': f, 'match': match})

def jv_add(request):
	# If request is POST, create a bound form (form with data)
	if request.method == "POST":
		f = JeuVariantesForm(request.POST)
		if f.is_valid():
			#  save data to db
			f.save()
			messages.add_message(request, messages.INFO, 'Variante de jeu ajoutée.')
			return redirect('jv_add') 
	# if request is GET the show unbound form to the user
	else:
		f = JeuVariantesForm()
	return render(request, 'cadmin/jv_add.html', {'form': f})	
	
def jv_update(request, pk):
	jv = get_object_or_404(JeuVariantes, pk=pk) 
	# If request is POST, create a bound form(form with data)
	if request.method == "POST":
		f = JeuVariantesForm(request.POST, instance=jv)
		# If form is invalid show form with errors again
		if f.is_valid():
			f.save()
			messages.add_message(request, messages.INFO, 'JeuVariantes updated.')
			return redirect(reverse('jv_update', args=[jv.id])) 
	# if request is GET the show unbound form to the user, along with data
	else:
		f = JeuVariantesForm(instance=jv) 
	return render(request, 'cadmin/jv_update.html', {'form': f, 'jv': jv})