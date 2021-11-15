function HidePassword() {
  var x = document.getElementById("myInput");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
var modal = document.querySelector(".modal");
var trigger = document.querySelector(".register-btn");
var closeButton = document.querySelector(".close-button");
var submitbutton = document.querySelector(".registration-submit")

function toggleModal() {
    modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal();
    }
}

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
//submitbutton.addEventListener("click", toggleModal);//
window.addEventListener("click", windowOnClick);
