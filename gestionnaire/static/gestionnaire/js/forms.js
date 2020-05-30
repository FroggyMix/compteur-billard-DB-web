//VARIABLES
const masque_champ_grisé = true //Permet de régler le fonctionnement : si true alors les champs grisé (non saisissables mais quand même pertinents 1/1 type de jeu) sont cachés

function check_JeuType(){	// LORS des changemenst dans la combo TYPE de JEU
	var url = $("#matchForm").attr("data-jv-url");  // get the url of the `load_cities` view
	//var jeu_type = $(this).val();  // get the selected type de jeu ID from the HTML input
	var jeu_type = document.querySelector("#id_jeu_type").value // get the selected type de jeu ID from the HTML input
	// VARIANTES DE JEU en fonction du type de jeu
	$.ajax({                       // initialize an AJAX request
		url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
		data: {
			'jeu_type': jeu_type       // add the country id to the GET parameters
		},
		success: function (data) {   // `data` is the return of the `load_cities` view function
			$("#id_jeu_variante").html(data);  // replace the contents of the city input with the data that came from the server
		}
	});	
	// MASQUAGE/AFFIHAGE des champs specifiques au TYPE de JEU
	var form_items = document.querySelectorAll("#matchForm > p");
	type_jeu_arr=["_fr_","_sn_","_am_","_po_"]	
	form_items.forEach(function(champs) {
		champs.childNodes.forEach(function(item) {
			if (item.id){
				for (let i = 0, l = type_jeu_arr.length; i < l; i += 1) {
					if (item.id.search(type_jeu_arr[i]) >= 0){
							champs.classList.add('invisible');
					}
					if (item.id.search("_"+jeu_type+"_") >= 0){
							champs.classList.remove('invisible');
					}
				}
			}
		});
	});	
}
function check_REG(){		// GRISAGE/COCHAGE/MASQUAGE de la checkbox REG
	//var limite_reprise = $(this).val();
	var limite_reprise = document.querySelector("#id_fr_limite_nb_reprises").value
	var chkbx_REG = document.querySelector("#id_fr_reprise_egalisatrice")
	if (!limite_reprise || limite_reprise == 0){		
		if (masque_champ_grisé) {document.querySelector("label[for="+chkbx_REG.id+"]").parentElement.classList.remove('invisible');}
		else {chkbx_REG.disabled = false;}
	}
	else{
		chkbx_REG.checked = true; // si une distance de reprise existe, alors on cohche REG obligatoirement
		if (masque_champ_grisé) {document.querySelector("label[for="+chkbx_REG.id+"]").parentElement.classList.add('invisible');}
		else {
			chkbx_REG.disabled= true;
			document.querySelector("label[for="+chkbx_REG.id+"]").disabled= 'disabled';//classList.add('griser');
		}
	}
}

window.onload = function () {
	check_JeuType();
	check_REG()
}
$("#id_jeu_type").change(function () {
	check_JeuType();
	check_REG();
});
$("#id_fr_limite_nb_reprises").change(function () {
	check_REG();
});
