document.querySelector('#menu_general').onclick = function(e){
  var elems = document.querySelector(".current");

  if(elems !==null){
   elems.classList.remove("current");
  }
 e.target.className = "current";
}