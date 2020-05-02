
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


chatSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);
	document.querySelector('#scoref_j1').textContent = (data.message.scoref_j1);
	document.querySelector('#scoref_j2').textContent = (data.message.scoref_j2);
	document.querySelector('#moyennef_j1').textContent = Math.round(1000*parseInt(data.message.scoref_j1)/parseInt(data.message.reprise))/1000;
	document.querySelector('#moyennef_j2').textContent = Math.round(1000*parseInt(data.message.scoref_j2)/parseInt(data.message.reprise))/1000;
	document.querySelector('#frame_reprise').textContent = (data.message.reprise);
	document.querySelector('#identite_j1').textContent = (data.message.match.nom_joueur1);
	document.querySelector('#identite_j2').textContent = (data.message.match.nom_joueur2);
	//document.querySelector('#frame_shot_timer').textContent = (data.);
	m1=data.message.match.scorem_j1;
	m2=data.message.match.scorem_j2;
	nbf=data.message.match.nb_frames;
	document.querySelector('#match_score').textContent = m1+" ("+nbf+") "+m2
	var joueur_actif = (data.message.joueur_actif);
	var break_j = (data.message.break);
	document.querySelector('.joueur_actif').classList.remove('joueur_actif')
	//window.alert(joueur_actif)
	if (joueur_actif == '1'){
		document.querySelectorAll('.gauche')[0].classList.add('joueur_actif')
		document.querySelector('#break_j1').textContent=break_j;
	}
	else{
		document.querySelectorAll('.droite')[0].classList.add('joueur_actif')
		document.querySelector('#break_j2').textContent=break_j;
	}
	
	//Gestion du chrono de frame
	const hui=new Date();
	var debut_frame=(data.message.h_debut);
	const h = debut_frame.split(':');	
	debut_frame2=new Date(hui.getFullYear(),hui.getMonth(),hui.getDate(),h[0],h[1],h[2]);	
	chrono_frame();
};

chatSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};

document.querySelector('#maj_scores_submit').onclick = function(e) {
	//window.alert("clic sur btn");
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

document.querySelector('#scoref_j1').onclick = function(e) {
	//window.alert("clic sur score J1");
	if (joueur_actif() == 1) {
		const score_j1_DOM = document.querySelector('#scoref_j1');
		chatSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "1",
			'points': "1",
		}));
	}
	//score_j1_DOM.textContent=parseInt(score_j1_DOM.textContent, 10)+1;
};
document.querySelector('#scoref_j2').onclick = function(e) {
	//window.alert("clic sur score J2");	
	if (joueur_actif() == 2) {
		const score_j2_DOM = document.querySelector('#scoref_j2');
		chatSocket.send(JSON.stringify({
			'action': 'score',
			'joueur': "2",
			'points': "1",
		}));
	}
	//score_j2_DOM.textContent=parseInt(score_j2_DOM.textContent, 10)+1;
};
document.querySelector('#frame_reprise').onclick = function(e) {
	const score_reprise_DOM = document.querySelector('#frame_reprise');
	 
	chatSocket.send(JSON.stringify({
		'action': 'pass',
		'joueur': joueur_actif(),
	}));
	//score_reprise_DOM.textContent=parseInt(score_reprise_DOM.textContent, 10)+1;
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
	document.querySelector('#frame_timer').textContent = hr + ":" + min + ":" + sec
	timerID = setTimeout("chrono_frame()", 1000)
}

function joueur_actif(){
	const joueur1actif = $('section.joueur.gauche').hasClass('joueur_actif');
	var joueur_actif=2;
	if (joueur1actif) {
		joueur_actif=1;
	}
	return joueur_actif
}