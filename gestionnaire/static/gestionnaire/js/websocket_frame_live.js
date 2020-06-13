// console.log( Date.now())
//PARAMETRES
var TTS_OK=false // pour saisir la valeur par défaut du TTS (activé ou desactivé
const CHRONO_AFFICHE_SECONDES = true //Pour chrono frame et match : Affiche et decompte les secondes si true, les minutes seulement si false

//DECLARATION des CONSTANTES et VARIABLES
const frameId = JSON.parse(document.getElementById('frame-id').textContent);
const shot_time_limit = JSON.parse(document.getElementById('shot_time_limit').textContent);

const FrameSocket = new WebSocket(
	'ws://'
	+ window.location.host
	+ '/ws/frame/'
	+ frameId
	+ '/'
);
// var debut_frame2=new Date();
// var end = 0
// var diff = 0
var timerID = 0
var frame_terminee = false
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
var arbitre=true //='arbitre' 
if (urlParams.get('ref')=="false"){arbitre=false;}//temp='spectateur';}

var racine_site=window.location.protocol+'//'+window.location.hostname
if (window.location.port){racine_site=racine_site+":"+window.location.port}
var modal_url_OK=""
var modal_url_Cancel=racine_site //"http://192.168.1.28:8000/"
var modal_ouverte = false // permet de savoir is une modale est en cours 
var start; //utilisé pour l'heure de début du countdown
var JEU_EN_PAUSE = false; //utilisé pour les chronos 
var TIMER_LIBRE =true; // Utilisé pour éviter de lancer plusieurs timers (chrono et match)
var TIMERS_RUN = true; // Indique si les timers doivent tourner ou pas (pas avant debut match, pas en pause, pas après fin match...
var COUNTDOWN_DANGER = 10; //Temps à partir duquel le countdown devient rouge et fait du son
// var stop_countdown=false;
if (arbitre){//affichage des outils dans le menu
	document.querySelector('.green').classList.remove('invisible')
	document.querySelector('.yellow').classList.remove('invisible')
}

//Gestion du TTS (forcer la valeur par défaut ci-dessous). Ne concerne que l'arbitre
if (arbitre){
	btn_TTS=document.querySelector('#toggle-TTS')
	txt_TTS=document.querySelector('#label-TTS')
	btn_TTS.classList.remove('fa-toggle-on','fa-toggle-off');
	if (TTS_OK){
		btn_TTS.classList.add('fa-toggle-on');
		txt_TTS.textContent="Désactiver le TTS";
	}
	else{
		btn_TTS.classList.add('fa-toggle-off');
		txt_TTS.textContent="Activer le TTS";
	}
	btn_TTS.addEventListener('click', () => {
		if (btn_TTS.classList.contains('fa-toggle-on')){
			TTS_OK=false;
			txt_TTS.textContent="Activer le TTS";
		}
		else{
			TTS_OK=true;
			txt_TTS.textContent="Désactiver le TTS";		
		}
		btn_TTS.classList.toggle('fa-toggle-off');
		btn_TTS.classList.toggle('fa-toggle-on');
	});
}
//Gestion du bouton PAUSE
if (document.getElementById('btn-pause')){
	btn_PAUSE=document.getElementById('btn-pause')
	txt_PAUSE=document.getElementById('label-pause')
	btn_PAUSE.addEventListener('click', () => {
		btn_PAUSE.classList.toggle('fa-pause');
		btn_PAUSE.classList.toggle('fa-play');
		if (btn_PAUSE.classList.contains('fa-pause')){
			txt_PAUSE.textContent="Mettre le jeu en pause";
			chrono_play();
			document.getElementById('sombre').style.zIndex='-2';
		}
		else{
			txt_PAUSE.textContent="Relancer le jeu";
			chrono_pause();
			document.getElementById('sombre').style.zIndex='2';
		}
	});
}

FrameSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);	
	console.log(">>>>>>>>>>>>>>>>>RECEPTION MESSAGE ")
		
	if (data.message.url){ //c'est un ordre de redirection
		url = data.message.url
		if(arbitre){
			url=url+"/?ref=true"
		}
		else {url=url+"/?ref=false"
		}
		window.location.replace(url);	
	}
	else{		
		// La commande ci-dessous est pour l'instant enlevée car ca supprime certain message instantanément (2 trames de suite)
		//document.querySelector('#message_live').textContent =  ""	//on réinitialise la zone de message, et à la fin du traitement si elle est tjs vide on la masque
		document.querySelector('#scoref_j1').textContent = (data.message.scoref_j1);
		document.querySelector('#scoref_j2').textContent = (data.message.scoref_j2);
		document.querySelector('#moyennef_j1').textContent = (data.message.moyenne_j1);
		document.querySelector('#moyennef_j2').textContent = (data.message.moyenne_j2);
		document.querySelector('#frame_reprise').textContent = (data.message.reprise);
		document.querySelector('#match_score').textContent = (data.message.match.score_match);
		
		var joueur_actif = (data.message.joueur_actif);
		var break_j = (data.message.break);
		
		console.log("TIMERS_RUN1 = " + TIMERS_RUN)
		if(!TIMERS_RUN) TIMER_LIBRE = true;
		JEU_EN_PAUSE = (data.message.jeu_en_pause)
		TIMERS_RUN = (!JEU_EN_PAUSE && data.message.vainqueurf == -1 && data.message.dureef_en_sec != null)
		// console.log("JEU_EN_PAUSE = " + JEU_EN_PAUSE)
		// console.log("data.message.vainqueurf = " + data.message.vainqueurf)
		// console.log("data.message.dureef_en_sec = " + data.message.dureef_en_sec)
		// console.log("TIMERS_RUN2 = " + TIMERS_RUN)
		// console.log("TIMER_LIBRE = " + TIMER_LIBRE)
		
		
		if (joueur_actif != "0"){force_joueur_actif(joueur_actif,break_j);}
		// Mise à jour du bouton PAUSE
		if (document.getElementById('btn-pause')){
			btn_PAUSE=document.getElementById('btn-pause')
			txt_PAUSE=document.getElementById('label-pause')
			if (JEU_EN_PAUSE){
				txt_PAUSE.textContent="Relancer le jeu";
				btn_PAUSE.classList.add('fa-play');
				btn_PAUSE.classList.remove('fa-pause');	
				document.getElementById('sombre').style.zIndex='2';
			}
			else{
				txt_PAUSE.textContent="Mettre le jeu en pause";
				btn_PAUSE.classList.add('fa-pause');
				btn_PAUSE.classList.remove('fa-play');
				document.getElementById('sombre').style.zIndex='-2';
			}
		}
		//Gestion du compte à rebour de temps de jeu
		if (data.message.shot_timer_a_relancer_depuis !=0){
			start = Date.parse(data.message.shot_timer_a_relancer_depuis+ " GMT");
			countdown(shot_time_limit,document.querySelector('#shot_timer'));
		}
		else{
			document.querySelector('#shot_timer').textContent =(JEU_EN_PAUSE) ? "PAUSE" : "00:00"
			document.querySelector('#shot_timer').classList.remove('timeout')
		}		
		//Gestion du chrono de frame : TODO optimisable? en ne relançant pas le chronoo à cchaque arrivée de ws ?
		// console.log("data.message.dureef_en_sec = "+data.message.dureef_en_sec)
		chrono_sec(data.message.dureef_en_sec,data.message.match.dureem_en_sec)
		if (TIMERS_RUN){
		}	
		else{	
			}
		
		//On gère ensuite le cas où le match vient de commencer (i.e. : joueur_commence=-1)
		var joueur_actif = (data.message.joueur_actif);
		if (data.message.dureef_en_sec == null ) {			
			if (data.message.numf == 1){
				if (arbitre){
					modal_ouverte = true;
					toss_modal.showModal();
					if (TTS_OK) {speak("Quel joueur engage ?");}}
				else {affiche_message_live("En attente de l'identification du joueur qui commence")}
			}
			else{
				discours = "Cliquer lorsque le joueur "+joueur_actif+" est prêt à engager"
				if (arbitre){
					document.getElementById('message_start_modal').innerText = discours;
					modal_ouverte = true;
					start_modal.showModal();
					if (TTS_OK) {speak(discours);}
				}
				else{//spectateur
					affiche_message_live("En attente de l'engagement du joueur "+joueur_actif)
				}
			}	
		}
		// Reprise égalisatrice
		if (data.message.reprise_egalisatrice == "maintenant"){
			discours = "Reprise égalisatrice pour le joueur "+joueur_actif
			if (arbitre){
				if (TTS_OK) {speak(discours);}
				modal_url_OK="";
				document.getElementById('message_info_modal').innerText = discours;
				modal_ouverte = true;
				info_modal.showModal();
			}
			else{//Spectateur
				affiche_message_live("Reprise égalisatrice pour le joueur "+joueur_actif)
			}
		}
		if (data.message.reprise_egalisatrice == "prochain"){
			discours = "Dernière reprise pour le joueur "+joueur_actif
			if (arbitre){
				if (TTS_OK) {speak(discours);}				
				modal_url_OK="";
				document.getElementById('message_info_modal').innerText = discours;
				modal_ouverte = true;
				info_modal.showModal();
			}
			else{
				affiche_message_live(discours)
			}
		}
		//Fin de frame
		if (data.message.vainqueurf >= 0){
			frame_terminee = true;
			var discours="Frame ";
			//var texteS="freym"
			if (data.message.match.vainqueurm > 0){
				frame_terminee = true;
				discours="Frame et Match "
				//texteS="freym et match "
				modal_url_OK="";
			}
			else {
				if (data.message.nextf){modal_url_OK=racine_site+"/frame/"+data.message.nextf;}
			}
			if (data.message.vainqueurf == 1 || data.message.vainqueurf == 2) {
				discours = discours + "pour joueur " + data.message.vainqueurf;
				if (arbitre){
					if (TTS_OK) {speak(discours);}
					document.getElementById('message_info_modal').innerText = discours;
					modal_ouverte = true;
					info_modal.showModal();
				}
				else{affiche_message_live(discours)}
			}		
			// if (data.message.vainqueurf == 2) {
				// document.getElementById('message_info_modal').innerText =texte+"pour joueur 2";
				// if (TTS_OK) {speak(texteS+"pour le joueur 2");}
				// affiche_message_live(texteS+"pour joueur 2")
			// }
			if (data.message.vainqueurf == 0) {
				discours = "Egalité ! On rejoue la frame !"
				if (arbitre){
					if (TTS_OK) {speak(discours);}
					document.getElementById('message_info_modal').innerText =discours;
					modal_ouverte = true;
					info_modal.showModal();
				}
				else{affiche_message_live(discours)}
			}
		}
		if (document.querySelector('#message_live').textContent ==  ""){document.querySelector('#message_live').classList.add('retracte')}
	}
};
FrameSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};
document.querySelector('#maj_scores_submit').onclick = function(e) {
	const modif_j1_DOM = document.querySelector('#maj_J1');
	const modif_j1=  modif_j1_DOM.value;
	const modif_j2_DOM = document.querySelector('#maj_J2');
	const modif_j2=  modif_j2_DOM.value;
	const modif_reprise_DOM = document.querySelector('#maj_reprise');
	const modif_reprise=  modif_reprise_DOM.value;
	
	FrameSocket.send(JSON.stringify({
		'action': 'correction',
		'j1_add': modif_j1,
		'j2_add': modif_j2,
		'reprise_add': modif_reprise
	}));

	modif_j1_DOM.value = '';
	modif_j2_DOM.value = '';
	modif_reprise_DOM.value = '';
};
document.querySelector('.gauche').onclick = function(e) {action_point(1);};
document.querySelector('.droite').onclick = function(e) {action_point(2);};
document.querySelector('section.reprise').onclick = function(e) {action_pass();};
document.querySelector('#annuler_action').onclick = function(e) {action_annuler()};
document.querySelector('#echange_couleurs').onclick = function(e) {
	document.querySelector('.joueur.gauche').classList.toggle('couleur1');
	document.querySelector('.joueur.gauche').classList.toggle('couleur2');
	document.querySelector('.joueur.droite').classList.toggle('couleur1');
	document.querySelector('.joueur.droite').classList.toggle('couleur2');
}
document.querySelector('#conceder').onclick = function(e) {
	nom_joueur=document.querySelectorAll('.nom')[get_joueur_actif()-1].querySelector('span').innerText;
	
	if(confirm("Confirmez-vous que " + nom_joueur + " concède la frame ? Cette action est irrémédiable.")){
		if (arbitre) {
			// window.alert(nom_joueur);
			FrameSocket.send(JSON.stringify({
			'action': 'concede',
			'joueur': get_joueur_actif(),
			}));
		}
	}		
}
document.addEventListener('keyup',(e) =>{
	if ( !modal_ouverte ){
		if(e.key == " "){action_pass()}
		if(e.key == "Enter"){action_point()}
		if(e.key == "Delete"){action_annuler()}
		if(e.key == "P"){if (JEU_EN_PAUSE) chrono_play(); else chrono_pause()}
	}
});
function action_annuler(){
	if (arbitre) {
		FrameSocket.send(JSON.stringify({
		'action': 'annuler_action',
		}));
	}
}
function chrono_pause(){
	if (arbitre) {
		FrameSocket.send(JSON.stringify({
		'action': 'chrono-pause',
		}));
	}
}
function chrono_play(){
	if (arbitre) {
		FrameSocket.send(JSON.stringify({
		'action': 'chrono-play',
		}));
	}
}
function action_point(zone = 0){
	if (JEU_EN_PAUSE) window.alert("Le jeu est en pause");
	if (frame_terminee) window.alert("La frame est terminée");
	if (arbitre &&  frame_terminee == false && !JEU_EN_PAUSE) {
		var j=-1
		if (zone == 0){j = get_joueur_actif()}
		if (zone == 1 && get_joueur_actif() == 1){j=1}
		if (zone == 2 && get_joueur_actif() == 2){j=2}
		if (j >= 0){
			JouerSon("son-point");
			// const score_j2_DOM = document.querySelector('#scoref_j2');
			FrameSocket.send(JSON.stringify({
				'action': 'score',
				'joueur': j,
				'points': "1",
			}));
		}
	}
}
function action_pass(){	
	if (JEU_EN_PAUSE) window.alert("Le jeu est en pause");
	if (frame_terminee) window.alert("La frame est terminée");	
	if (arbitre && frame_terminee == false && !JEU_EN_PAUSE){
		JouerSon("son-reprise");
		// const score_reprise_DOM = document.querySelector('#frame_reprise'); 
		FrameSocket.send(JSON.stringify({
			'action': 'pass',
			'joueur': get_joueur_actif(),
		}));
	}
};	
function chrono_sec(secondesF,secondesM){
	var nb_sec =0;
	if (JEU_EN_PAUSE){
		console.log(">>[IF] Affichage du temps de frame : "+format_HMS(secondesF))
		document.querySelector('#frame_timer').textContent = format_HMS(secondesF);
		document.querySelector('#match_timer').textContent = format_HMS(secondesM);
		TIMER_LIBRE = true;
	}
	else{
		console.log("lancement timer")
		ref = Date.now();
		console.log("TIMER_LIBRE = " + TIMER_LIBRE)
		if (TIMER_LIBRE) timer_sec();
		TIMER_LIBRE = false;
		console.log("--->>>TIMER_LIBRE = " + TIMER_LIBRE)
	}
	function timer_sec(){
		console.log("--->>>TIMER_RUN = " + TIMERS_RUN)
		if(TIMERS_RUN) {
			// console.log(">>[FUNC] Affichage du temps de frame : "+format_HMS(secondesF + nb_sec)+"(secondesF = "+secondesF+" ; delta_sec ="+nb_sec+")")
			document.querySelector('#frame_timer').textContent = format_HMS(secondesF + nb_sec);
			document.querySelector('#match_timer').textContent = format_HMS(secondesM + nb_sec);
			nb_sec+=1;
			setTimeout(timer_sec,(CHRONO_AFFICHE_SECONDES) ? 1000 : 60000);
		}
		else{TIMER_LIBRE = true}
	}
}
function ws_envoi_toss(numjoueur){	 
	FrameSocket.send(JSON.stringify({
		'action': 'toss',
		'joueur': numjoueur,
	}));
}
function ws_envoi_start(){	 
	FrameSocket.send(JSON.stringify({
		'action': 'start',
		'joueur': get_joueur_actif(),
	}));
}	
function get_joueur_actif(){
	const joueur1actif = $('section.joueur.gauche').hasClass('joueur_actif');
	var joueur_actif=2;
	if (joueur1actif) {
		joueur_actif=1;
	}
	return joueur_actif
}
function force_joueur_actif(j,break_j){
	document.querySelector('.joueur_actif').classList.remove('joueur_actif')
	if (j == '1'){
		document.querySelectorAll('.gauche')[0].classList.add('joueur_actif')
		document.querySelector('#break_j1').textContent=break_j;
	}
	else{
		document.querySelectorAll('.droite')[0].classList.add('joueur_actif')
		document.querySelector('#break_j2').textContent=break_j;
	}
}
function JouerSon(nom_son) {
	        var sound = document.getElementById(nom_son);  
            sound.play()
}
function ws_redirect(action){		
	if(action=="OK"){urle=modal_url_OK}
	else {urle=modal_url_Cancel}
	FrameSocket.send(JSON.stringify({
		'action': 'redirect',
		'url': urle,
	}));
}	
function speak(text){
	var msg = new SpeechSynthesisUtterance();
	// var voices = window.speechSynthesis.getVoices();
	// msg.voice = voices[10]; // Note: some voices don't support altering params
		// speechSynthesis.getVoices().forEach(function(voice) {
			// window.alert(voice.name, voice.default ? voice.default :'');
		// });
	text = text.replace(/frame/gi, "freyme");
	msg.voiceURI = 'native';
	msg.volume = 1; // 0 to 1
	msg.rate = 1; // 0.1 to 10
	msg.pitch = 2; //0 to 2
	msg.text = text;
	msg.lang = 'fr-FR';
	speechSynthesis.speak(msg);
}
function affiche_message_live(text){
	document.querySelector('#message_live').textContent =  text	
	document.querySelector('#message_live').classList.remove('retracte')
	document.querySelector('#message_live').classList.add('deroule')
	setTimeout(function(){
		document.querySelector('#message_live').textContent ="";
		document.querySelector('#message_live').classList.remove('deroule')
		document.querySelector('#message_live').classList.add('retracte')
	},10000);
}
function format_HMS(secondes, H = true, M = true, S = (CHRONO_AFFICHE_SECONDES)){ //affiche un nombre de sec dans HH:MM:SS ou HH:MM ou MM:SS
	var hh='', mm='', ss=''
	if (H){hh=new Date(secondes * 1000).toISOString().substr(11, 2)}
	if (M){mm=new Date(secondes * 1000).toISOString().substr(14, 2)}
	if (S){ss=new Date(secondes * 1000).toISOString().substr(17, 2)}
	str = ''
	if(hh){
		str+=hh;
		if(mm || ss){str+=":";}
	}
	if(mm){
		str+=mm;
		if(ss){str+=":";}
	}
	if(mm){str+=ss;}
	return str
}
function countdown(duration, cible) {
	var diff,
	minutes,
	seconds;
	cible.classList.remove('timeout')
    timer();
    function timer() {
        // get the number of seconds that have elapsed since 
        // startTimer() was called
        diff = duration - (((Date.now() - start) / 1000) | 0);
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        cible.textContent = minutes + ":" + seconds; 
        if (diff <= COUNTDOWN_DANGER) {
			JouerSon("son-tictac");
        	cible.classList.add('timeout')
        }
		if (diff <= 0) {
			if (diff == 0) JouerSon("son-buzzer");
        	cible.classList.add('timeout');
			cible.textContent = "00:00";
        }
        else{
        	if(TIMERS_RUN) setTimeout(timer,1000);
			if(JEU_EN_PAUSE) {document.querySelector('#shot_timer').textContent = "PAUSE";}	
        }
    }
}
