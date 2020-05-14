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
var temp='arbitre' 
if (urlParams.get('ref')=="false"){temp='spectateur';}
const demandeur=temp

var racine_site=window.location.protocol+'//'+window.location.hostname
if (window.location.port){racine_site=racine_site+":"+window.location.port}
var modal_url_OK=""
var modal_url_Cancel=racine_site //"http://192.168.1.28:8000/"
const TTS_OK=true // pour activer/desactiver le TTS

FrameSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);	
	if (data.message.url){
		url = data.message.url
		
		if(demandeur == 'arbitre'){
			url=url+"/?ref=true"
		}
		else {url=url+"/?ref=false"
		}
		window.location.replace(url);	
	}
	else{
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
		
		if (demandeur == 'arbitre'){
			//On gère ensuite le cas où le match vient de commencer (i.e. : joueur_commence=-1)
			var joueur_actif = (data.message.joueur_actif);
			if (data.message.dureef !="00:00:00") {
			}
			else{
				if (data.message.numf == 1){
					if (TTS_OK) {speak("Quel joueur engage ?");}
					toss_modal.showModal();
				}
				else{
					if (TTS_OK) {speak("Cliquer lorsque le joueur "+joueur_actif+" est prêt à engager");}
					document.getElementById('message_start_modal').innerText ="Cliquer sur le bouton ci-dessous lorsque le joueur "+joueur_actif+" est prêt à engager"
					start_modal.showModal();
				}	
			}
			// Reprise égalisatrice
			if (data.message.reprise_egalisatrice == "maintenant"){
				if (TTS_OK) {speak("Reprise égalisatrice pour le joueur "+joueur_actif);}
				modal_url_OK="";
				document.getElementById('message_info_modal').innerText ="Reprise égalisatrice pour le joueur "+joueur_actif;
				info_modal.showModal();
			}
			if (data.message.reprise_egalisatrice == "prochain"){
				if (TTS_OK) {speak("Dernière reprise pour le joueur "+joueur_actif);}
				modal_url_OK="";
				document.getElementById('message_info_modal').innerText ="Dernière reprise pour le joueur "+joueur_actif;
				info_modal.showModal();
			}
			//Fin de frame
			if (data.message.vainqueurf >= 0){
				frame_terminee = true;
				var texte="Frame ";
				var texteS="freym"
				if (data.message.match.vainqueurm > 0){
					frame_terminee = true;
					texte="Frame et Match "
					texteS="freym et match "
					modal_url_OK="";
				}
				else {
					if (data.message.nextf){modal_url_OK=racine_site+"/frame/"+data.message.nextf;}
				}
				if (data.message.vainqueurf == 1) {document.getElementById('message_info_modal').innerText =texte+"pour joueur 1";if (TTS_OK) {speak(texteS+"pour Franck Rapold");}}
				if (data.message.vainqueurf == 2) {document.getElementById('message_info_modal').innerText =texte+"pour joueur 2";if (TTS_OK) {speak(texteS+"pour le joueur 2");}}
				if (data.message.vainqueurf == 0) {document.getElementById('message_info_modal').innerText ="Egalité ! On rejoue la frame !";if (TTS_OK) {speak("égalité, la freym est rejouée");}}
				info_modal.showModal();
			}
		}
		//if (data.message.nextf){window.location.replace("http://192.168.1.28:8000/frame/"+data.message.nextf+"/?ref="+urlParams.get('ref'));}
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
document.querySelector('.gauche').onclick = function(e) {
	if (demandeur == 'arbitre' && get_joueur_actif() == 1 && frame_terminee == false) {
		JouerSon("son-point");
		const score_j1_DOM = document.querySelector('#scoref_j1');
		FrameSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "1",
			'points': "1",
		}));
	}
};
document.querySelector('.droite').onclick = function(e) {
	if (demandeur == 'arbitre' && get_joueur_actif() == 2 && frame_terminee == false) {
		JouerSon("son-point");
		const score_j2_DOM = document.querySelector('#scoref_j2');
		FrameSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "2",
			'points': "1",
		}));
	}
};
document.querySelector('section.reprise').onclick = function(e) {
	if (demandeur == 'arbitre' && frame_terminee == false){
		JouerSon("son-reprise");
		const score_reprise_DOM = document.querySelector('#frame_reprise'); 
		FrameSocket.send(JSON.stringify({
			'action': 'pass',
			'joueur': get_joueur_actif(),
		}));
	}
};
document.querySelector('#annuler_action').onclick = function(e) {
	FrameSocket.send(JSON.stringify({
		'action': 'annuler_action',
	}));
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
	msg.voiceURI = 'native';
	msg.volume = 1; // 0 to 1
	msg.rate = 1; // 0.1 to 10
	msg.pitch = 2; //0 to 2
	msg.text = text;
	msg.lang = 'fr-FR';
	// msg.onend = function(e) {
	  // console.log('Finished in ' + event.elapsedTime + ' seconds.');
	// };
	speechSynthesis.speak(msg);
}