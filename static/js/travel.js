$(window).scroll(function(){
    if ($(this).scrollTop() >=50) {
        $('.header').addClass('nav-fixed');
    }
    else{
        $('.header').removeClass('nav-fixed');
    }
});

let menu = document.querySelector('#menu-bar');
let navbar = document.querySelector('.navbar');
window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}
menu.addEventListener('click', () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
});