from gestionnaire.models import *
from django.db.models import F, Func
from django.db.models import Avg, Count, Min, Sum

def frame_states(frame_id):
	fr=Frame.objects.get(pk=frame_id)

	etat_json = {
		"match":{
			"dureeM":fr.match.dureem_reelle(),
			"vainqueurm":fr.match.vainqueurm(),
			# "nb_frames":fr.match.nb_frames, Désormais affiché directement par framelive.html
			# "scorem_j1":fr.match.scorem_j1(), Désormais affiché directement par framelive.html
			# "scorem_j2":fr.match.scorem_j2(), Désormais affiché directement par framelive.html
			# "distanceFR_j1":fr.match.fr_distance_j1, Désormais affiché directement par framelive.html
			# "distanceFR_j2":fr.match.fr_distance_j2, Désormais affiché directement par framelive.html
			# "nom_joueur1":fr.match.joueur1.fullname_score_board(), Désormais affiché directement par framelive.html
			# "nom_joueur2":fr.match.joueur2.fullname_score_board(), Désormais affiché directement par framelive.html
			},
		"numf":fr.num,
		"nextf":fr.next_frame_existe(),
		"dureef":fr.dureef(),
		"scoref_j1":fr.scoref_j1(),
		"moyenne_j1":fr.moyennef_j1(),
		"scoref_j2":fr.scoref_j2(),
		"moyenne_j2":fr.moyennef_j2(),		
		"reprise":fr.reprise(),
		"joueur_actif":fr.joueur_actif(),
		"break":fr.break_en_cours(),
		"joueur_commence":fr.debutant(),
		# "reprise_egalisatrice":fr.reprise_egalisatrice_now(),
		"reprise_egalisatrice":fr.reprise_egalisatrice(),
		"vainqueurf":fr.vainqueurf(),		
		}
	return(etat_json)

