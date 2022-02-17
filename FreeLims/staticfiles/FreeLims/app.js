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
window.addEventListener("click", windowOnClick);//
//submitbutton.addEventListener("click", toggleModal);//



// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
$(window).on("load resize ", function() {
  var scrollWidth = $('.sample-tbl-content').width() - $('.sample-tbl-content table').width();
  $('.sample-tbl-header').css({'padding-right':scrollWidth});
}).resize();