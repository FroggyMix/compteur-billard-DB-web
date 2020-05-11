
const frameId = JSON.parse(document.getElementById('frame-id').textContent);

const chatSocket = new WebSocket(
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


chatSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);	

	document.querySelector('#scoref_j1').textContent = (data.message.scoref_j1);
	document.querySelector('#scoref_j2').textContent = (data.message.scoref_j2);
	document.querySelector('#moyennef_j1').textContent = (data.message.moyenne_j1);//Math.round(1000*parseInt(data.message.scoref_j1)/parseInt(data.message.reprise))/1000;
	document.querySelector('#moyennef_j2').textContent = (data.message.moyenne_j2);//Math.round(1000*parseInt(data.message.scoref_j2)/parseInt(data.message.reprise))/1000;
	document.querySelector('#frame_reprise').textContent = (data.message.reprise);
	// document.querySelector('#identite_j1').textContent = (data.message.match.nom_joueur1);
	// document.querySelector('#identite_j2').textContent = (data.message.match.nom_joueur2);
	//document.querySelector('#frame_shot_timer').textContent = (data.);
	
	// m1=data.message.match.scorem_j1;
	// m2=data.message.match.scorem_j2;
	// nbf=data.message.match.nb_frames;
	// document.querySelector('#match_score').textContent = m1+" ("+nbf+") "+m2
	
	var joueur_actif = (data.message.joueur_actif);
	var break_j = (data.message.break);
	//window.alert(joueur_actif)
	
	if (joueur_actif != "0"){force_joueur_actif(joueur_actif,break_j);}
	
	//Gestion du chrono de frame : TODO optimisable? en ne relançant pas le chronoo à cchaque arrivée de ws ?
	const hui=new Date();
	var debut_frame=(data.message.dureef);
	const h = debut_frame.split(':');	
	debut_frame2=new Date(hui.getFullYear(),hui.getMonth(),hui.getDate(),hui.getHours()-h[0],hui.getMinutes()-h[1],hui.getSeconds()-h[2]);	
	chrono_frame();
	if (data.message.vainqueurf == -1){chrono_frame();}
	
	// Affichage de la durée du match : calcul désormais géré directement dans le template (ne change pas pdt la frame)
	// var hm=data.message.match.dureeM.split(':');
	// hmh=hm[0];
	// if (hmh<10){hmh="0"+hmh}
	// hmm=hm[1];
	// if (hmm.length<2){hmm="0"+hmm}
	document.querySelector('#match_timer').textContent = data.message.match.dureeM;
	
	if (demandeur == 'arbitre'){
		//window.alert(data.message.dureef)
		//On gère ensuite le cas où le match vient de commencer (i.e. : joueur_commence=-1)
		var joueur_actif = (data.message.joueur_actif);
		if (data.message.dureef !="00:00:00") {
				//window.alert("le jouer qui a engagé : "+data.message.joueur_commence)
		}
		else{
			if (data.message.numf == 1){
				toss_modal.showModal();
			}
			else{
				document.getElementById('message_start_modal').innerText ="Cliquer sur le bouton ci-dessous lorsque le joueur "+joueur_actif+" est prêt à engager"
				start_modal.showModal();
			}	
		}
		// Reprise égalisatrice
		if (data.message.reprise_egalisatrice == "maintenant"){
			//window.alert("reprise égalisatrice")
			document.getElementById('message_info_modal').innerText ="Reprise égalisatrice pour le joueur "+joueur_actif;
			info_modal.showModal();
		}
		if (data.message.reprise_egalisatrice == "prochain"){
			document.getElementById('message_info_modal').innerText ="Dernier coup pour le joueur "+joueur_actif;
			info_modal.showModal();
		}
		//Fin de frame
		if (data.message.vainqueurf >= 0){
			frame_terminee = true;
			// if (data.message.vainqueurf == 1) {window.alert("frame gagnée par joueur 1")}
			// if (data.message.vainqueurf == 2) {window.alert("frame gagnée par joueur 2")}
			// if (data.message.vainqueurf == 0) {window.alert("Egalité !! je ne sais pas quoi faire")}	
			var texte="Frame ";
			if (data.message.match.vainqueurm > 0){
				frame_terminee = true;
				texte="Frame et Match ";
			}
			if (data.message.vainqueurf == 1) {document.getElementById('message_info_modal').innerText =texte+"pour joueur 1"}
			if (data.message.vainqueurf == 2) {document.getElementById('message_info_modal').innerText =texte+"pour joueur 2"}
			if (data.message.vainqueurf == 0) {document.getElementById('message_info_modal').innerText ="Egalité !! je ne sais pas (encore) quoi faire"}
			info_modal.showModal();
		}
		//Fin de match
		// if (data.message.match.vainqueurm > 0){
			// frame_terminee = true;
			// if (data.message.match.vainqueurm == 1) {window.alert("Match gagnée par joueur 1")}
			// if (data.message.match.vainqueurm == 2) {window.alert("Match gagnée par joueur 2")}
		// }
	}
	if (data.message.nextf){window.location.replace("http://192.168.1.28:8000/frame/"+data.message.nextf+"/?ref="+urlParams.get('ref'));}
	// if (data.message.match.vainqueurm <= 0 && data.message.vainqueurf >= 0){
		// if (confirm('Voulez-vous lancer la frame suivante ?')) {
			// window.location.replace("http://192.168.1.28:8000/frame/"+data.message.numf+1+"/");
		// }
		// else{
			// window.location.replace("http://192.168.1.28:8000/frame_liste");
		// }
	// }
};

chatSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};
document.querySelector('#maj_scores_submit').onclick = function(e) {
	const modif_j1_DOM = document.querySelector('#maj_J1');
	const modif_j1=  modif_j1_DOM.value;
	const modif_j2_DOM = document.querySelector('#maj_J2');
	const modif_j2=  modif_j2_DOM.value;
	const modif_reprise_DOM = document.querySelector('#maj_reprise');
	const modif_reprise=  modif_reprise_DOM.value;
	
	chatSocket.send(JSON.stringify({
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
	if (get_joueur_actif() == 1 && frame_terminee == false) {
		JouerSon("son-point");
		const score_j1_DOM = document.querySelector('#scoref_j1');
		chatSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "1",
			'points': "1",
		}));
	}
};
document.querySelector('.droite').onclick = function(e) {
	if (get_joueur_actif() == 2 && frame_terminee == false) {
		JouerSon("son-point");
		const score_j2_DOM = document.querySelector('#scoref_j2');
		chatSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "2",
			'points': "1",
		}));
	}
};
// document.querySelector('#frame_reprise').onclick = function(e) {
document.querySelector('section.reprise').onclick = function(e) {
	if (frame_terminee == false){
		JouerSon("son-reprise");
		const score_reprise_DOM = document.querySelector('#frame_reprise'); 
		chatSocket.send(JSON.stringify({
			'action': 'pass',
			'joueur': get_joueur_actif(),
		}));
	}
};
document.querySelector('#annuler_action').onclick = function(e) {
	//window.alert('annulation')
	chatSocket.send(JSON.stringify({
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
	chatSocket.send(JSON.stringify({
		'action': 'toss',
		'joueur': numjoueur,
	}));
}
function ws_envoi_start(){	 
	chatSocket.send(JSON.stringify({
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
			// window.alert(sound.innerhtml)
    
            sound.play()
}