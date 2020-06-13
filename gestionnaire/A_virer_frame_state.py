from gestionnaire.models import *
from django.db.models import F, Func
from django.db.models import Avg, Count, Min, Sum

def frame_states(frame_id):
	fr=Frame.objects.get(pk=frame_id)

	etat_json = {
		"match":{
			"dureeM":fr.match.dureem_reelle(),
			"vainqueurm":fr.match.vainqueurm(),
			"score_match":fr.match.score_match_dans_framelive(), #On envoie qd mm cette info car à la fin de la dernière frame il faut prendre en compte le changement de score
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
		"restart_shot_timer":fr.restart_shot_timer(),
		}
	return(etat_json)

