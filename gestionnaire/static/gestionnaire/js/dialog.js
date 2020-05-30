//////// INFO_OK
const info_modal = document.getElementById('info_modal');
const info_close = document.getElementById('info_close');
const info_OK = document.getElementById('info_OK');

dialogPolyfill.registerDialog(info_modal);
info_OK.addEventListener('click', () => {
  if(modal_url_OK != ""){ws_redirect("OK")}
  info_modal.close('');
  modal_ouverte = false;
});
info_close.addEventListener('click', () => {// Click sur croix
  // Todo ? : revenir sur la frame-list
  info_modal.close('cancelled');
  modal_ouverte = false;
});
info_modal.addEventListener('cancel', () => {// appui sur echap
  // Todo ? : revenir sur la frame-list
  info_modal.close('cancelled');
  modal_ouverte = false;
});

//////// MODAL START
const start_modal = document.getElementById('start_modal');
const start_close = document.getElementById('start_close');
const start_OK = document.getElementById('start_OK');

dialogPolyfill.registerDialog(start_modal);
start_OK.addEventListener('click', () => {
  ws_envoi_start();
  start_modal.close('');
  modal_ouverte = false;
});
start_close.addEventListener('click', () => {// Click sur croix
  // Todo ? : revenir sur la frame-list
  window.location.replace(modal_url_Cancel); //ws_redirect("cancel")
  start_modal.close('cancelled');
  modal_ouverte = false;
});
start_modal.addEventListener('cancel', () => {// appui sur echap
  // Todo ? : revenir sur la frame-list
  window.location.replace(modal_url_Cancel); //ws_redirect("cancel")
  start_modal.close('cancelled');
  modal_ouverte = false;
});


//////// MODAL TOSS
const toss_modal = document.getElementById('toss_modal');
const toss_close = document.getElementById('toss_close');
const toss_BtnJoueur1 = document.getElementById('toss_BtnJoueur1');
const toss_BtnJoueur2 = document.getElementById('toss_BtnJoueur2')
//const returnSpan = document.getElementById('return-value');


dialogPolyfill.registerDialog(toss_modal);
toss_BtnJoueur1.addEventListener('click', () => {
  ws_envoi_toss(1);
  toss_modal.close('');
  modal_ouverte = false;
});
toss_BtnJoueur2.addEventListener('click', () => {
  ws_envoi_toss(2);
  toss_modal.close('');
  modal_ouverte = false;
});
toss_close.addEventListener('click', () => {// Click sur croix
  // Todo ? : revenir sur la frame-list
  window.location.replace(modal_url_Cancel); //ws_redirect("cancel")
  toss_modal.close('cancelled');
  modal_ouverte = false;
});
toss_modal.addEventListener('cancel', () => {// appui sur echap
  // Todo ? : revenir sur la frame-list
  window.location.replace(modal_url_Cancel); //ws_redirect("cancel")
  toss_modal.close('cancelled');
  modal_ouverte = false;
});

// //close when clicking on backdrop
// modal.addEventListener('click', (event) => {
  // if (event.target === modal) {
    // modal.close('cancelled');
  // }
// });

// //display returnValue
// modal.addEventListener('close', () => {
  // returnSpan.innerHTML = modal.returnValue;
// });