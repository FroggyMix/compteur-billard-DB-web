from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
import datetime
from django import template
from django.conf import settings
from .models import Frame, Match, Joueur, JeuVariantes
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from compteur_billard import helpers
from django.contrib import auth
from django.contrib import messages
from gestionnaire.forms import JoueurForm, MatchForm, JeuVariantesForm

# Descriptions des vues

def index(request):
	return HttpResponse("Hello Django") 
	
def joueur_liste(request):
	joueurs=Joueur.objects.all().order_by('-prenom')
	joueurs = helpers.pg_records(request, joueurs, 3) #Pagination
	return render(request, 'gestionnaire/joueur_liste.html', {'joueurs':joueurs})

def match_liste(request):
	matchs=Match.objects.all()
	matchs = helpers.pg_records(request, matchs, 10) #Pagination
	return render(request, 'gestionnaire/match_liste.html', {'matchs':matchs})

# def frame_liste(request):
	# framesEC=Frame.objects.frame_en_cours()
	# framesAV=Frame.objects.frame_a_venir()
	# framesRT=Frame.objects.frame_terminee()
	# context = {
		# 'framesEC':framesEC,
		# 'framesAV':framesAV,
		# 'framesRT':framesRT,
	# }
	# return render(request, 'gestionnaire/frame_liste.html', context)
	
def frame_liste(request):
	if request.method == "POST":
		f = MatchForm(request.POST)
		if f.is_valid():
			#  save data to db
			f.save()
			messages.add_message(request, messages.INFO, 'Match ajouté.')
			return redirect('frame_liste')
	# if request is GET the show unbound form to the user
	else:
		f = MatchForm()
		framesEC=Frame.objects.frame_en_cours()
		framesAV=Frame.objects.frame_a_venir()
		framesRT=Frame.objects.frame_terminee()

		context = {
			'framesEC':framesEC,
			'framesAV':framesAV,
			'framesRT':framesRT,
			'form': f
		}
		return render(request, 'gestionnaire/frame_liste.html', context)

def match_detail(request,pk):
	#match = Match.objects.get(pk=pk)
	match = get_object_or_404(Match,pk=pk) #permet la gestion de l'erreur 404
	#frames = Frame.objects.filter(match__id=match.pk)#.values_list("scoref_j1","scoref_j2","en_cours")
	frames = get_list_or_404(Frame,match__id=match.pk)
	context = {
		'match': match,
		'frames': frames
	}
	return render(request, 'gestionnaire/match_detail.html', context)

def joueur_detail(request,pk,joueur_nom,joueur_prenom):
	joueur = Joueur.objects.get(pk=pk)
	nb_match = Match.objects.filter(Q(joueur1__id=pk) | Q(joueur2__id=pk)).count()
	liste_match = Match.objects.filter(Q(joueur1__id=pk) | Q(joueur2__id=pk))
	context = {
		'joueur': joueur,
		'nb_match': nb_match,
		'liste_match': liste_match
	}
	return render(request, 'gestionnaire/joueur_detail.html', context)

def jv_liste(request):
	jvs=JeuVariantes.objects.all()
	return render(request, 'gestionnaire/jv_liste.html', {'jvs':jvs})

def jv_detail(request,jv_slug):
	jv=JeuVariantes.objects.get(slug=jv_slug)
	return render(request, 'gestionnaire/jv_detail.html', {'jv':jv})

def match_redirect(request):
	return redirect('match_liste')
	#On peut aussi transmetre une classe de models :
	#c = Match.objects.get(id=1)
	#return redirect(c)

# ADMIN pages
def login(request):
	if request.user.is_authenticated:
		return redirect('admin_page')

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)
 
		if user is not None:
			# correct username and password login the user
			auth.login(request, user)
			return redirect('admin_page')
 
		else:
			messages.error(request, 'Error wrong username/password')

	return render(request, 'gestionnaire/login.html')
 
def logout(request):
	auth.logout(request)
	return render(request,'gestionnaire/logout.html')
 
 
def admin_page(request):
	if not request.user.is_authenticated:
		return redirect('blog_login')
 
	return render(request, 'gestionnaire/admin_page.html')

def frame_live(request, frame_id):
	return render(request,'gestionnaire/frame_live.html',{'frame_id':frame_id})
	
	
#debuggage pb de menudef
def base(request):
	return render(request,'gestionnaire/base.html')
