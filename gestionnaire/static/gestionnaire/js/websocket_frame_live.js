//PARAMETRES
var TTS_OK=false // pour saisir la valeur patrr défaut du TTS (activé ou desactivé

//DECLARATION des CONSTANTES et VARIABLES
const frameId = JSON.parse(document.getElementById('frame-id').textContent);
const FrameSocket = new WebSocket(
	'ws://'
	+ window.location.host
	+ '/ws/frame/'
	+ frameId
	+ '/'
);
var debut_frame2=new Date();
var end = 0
var diff = 0
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

if (arbitre){//affichage des outils dans le menu
	document.querySelector('.green').classList.remove('invisible')
	document.querySelector('.yellow').classList.remove('invisible')
}

//Gestion du TTS (forcer la valeur par défaut ci-dessous)
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

FrameSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);	
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
		
		if (joueur_actif != "0"){force_joueur_actif(joueur_actif,break_j);}
		
		//Gestion du chrono de frame : TODO optimisable? en ne relançant pas le chronoo à cchaque arrivée de ws ?
		const hui=new Date();
		var debut_frame=(data.message.dureef);
		const h = debut_frame.split(':');	
		debut_frame2=new Date(hui.getFullYear(),hui.getMonth(),hui.getDate(),hui.getHours()-h[0],hui.getMinutes()-h[1],hui.getSeconds()-h[2]);	
		chrono_frame();
		if (data.message.vainqueurf == -1){chrono_frame();}
		
		document.querySelector('#match_timer').textContent = data.message.match.dureeM;
		
		//On gère ensuite le cas où le match vient de commencer (i.e. : joueur_commence=-1)
		var joueur_actif = (data.message.joueur_actif);
		if (data.message.dureef !="00:00:00") {
		}
		else{
			if (data.message.numf == 1){
				if (arbitre){
					modal_ouverte = true;
					toss_modal.showModal();
					if (TTS_OK) {speak("Quel joueur engage ?");}}
				else{affiche_message_live("En attente de l'identification du joueur qui commence")}
				
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
	}
});
function action_annuler(){
	if (arbitre) {
		FrameSocket.send(JSON.stringify({
		'action': 'annuler_action',
		}));
	}
}
function action_point(zone = 0){
	if (arbitre &&  frame_terminee == false) {
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
	if (arbitre && frame_terminee == false){
		JouerSon("son-reprise");
		// const score_reprise_DOM = document.querySelector('#frame_reprise'); 
		FrameSocket.send(JSON.stringify({
			'action': 'pass',
			'joueur': get_joueur_actif(),
		}));
	}
};
	
function chrono_frame(){
	end = new Date()
    diff = end - debut_frame2
	diff = new Date(diff)
	var sec = diff.getSeconds()
	var min = diff.getMinutes()
	var hr = diff.getHours()-1
	if (min < 10){
		min = "0" + min
	}
	if (sec < 10){
		sec = "0" + sec
	}
	if (hr < 10){
		hr = "0" + hr
	}
	document.querySelector('#frame_timer').textContent = hr + ":" + min //+ ":" + sec
	timerID = setTimeout("chrono_frame()", 60000)
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