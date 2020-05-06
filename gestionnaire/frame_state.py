from gestionnaire.models import *
from django.db.models import F, Func
from django.db.models import Avg, Count, Min, Sum

def frame_states(frame_id):
	fr=Frame.objects.get(pk=frame_id)

	etat_json = {
		"match":{
			"nb_frames":fr.match.nb_frames,
			"scorem_j1":fr.match.scorem_j1(),
			"scorem_j2":fr.match.scorem_j2(),
			"dureeM":fr.match.dureem_reelle(),
			"distanceFR_j1":fr.match.fr_distance_j1,
			"distanceFR_j2":fr.match.fr_distance_j2,
			#"nom_joueur1":construit_nom(Match.objects.values_list('joueur1__prenom', flat=True).get(pk=id_match),Match.objects.values_list('joueur1__nom', flat=True).get(pk=id_match)),
			"nom_joueur1":fr.match.joueur1.fullname_score_board(),
			#"nom_joueur2":construit_nom(Match.objects.values_list('joueur2__prenom', flat=True).get(pk=id_match),Match.objects.values_list('joueur2__nom', flat=True).get(pk=id_match)),
			"nom_joueur2":fr.match.joueur2.fullname_score_board(),
			"vainqueurm":fr.match.vainqueurm(),
			},
		#"next_frame_id":33
		"numf":fr.num,
		"h_debut":fr.heure_debut(),
		#"scoref_j1":FrameEvent.objects.filter(frame=frame_id,crediteur=1,event_type__nom='score').values('points').aggregate(Sum('points'))['points__sum'],
		"scoref_j1":fr.scoref_j1(),
		#"scoref_j2":FrameEvent.objects.filter(frame=frame_id,crediteur=2,event_type__nom='score').values('points').aggregate(Sum('points'))['points__sum'],
		"scoref_j2":fr.scoref_j2(),
		"reprise":fr.reprise(),
		"joueur_actif":fr.joueur_actif(),
		"break":fr.break_en_cours(),
		"joueur_commence":fr.debutant(),
		"reprise_egalisatrice":fr.reprise_egalisatrice_now(),
		"vainqueurf":fr.vainqueurf(),
		
		}
	return(etat_json)

