$(window).scroll(function(){
    if ($(this).scrollTop() >=50) {
        $('.navi').addClass('nav-fixed');
    }
    else{
        $('.navi').removeClass('nav-fixed');
    }
});

let searchBtn = document.querySelector('#search-btn');
let searchBar = document.querySelector('.search-bar-container');
let formBtn = document.querySelector('#login-btn');
let loginForm = document.querySelector('.login-form-container');
let formClose = document.querySelector('#form-close');
let menu = document.querySelector('#menu-bar');
let navbar = document.querySelector('.navbar');
let videoBtn = document.querySelectorAll('.vid-btn');


window.onscroll = () =>{
    searchBtn.classList.remove('fa-times');
    searchBar.classList.remove('active');
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
    loginForm.classList.remove('active');
}

menu.addEventListener('click', () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
});

searchBtn.addEventListener('click', () =>{
    searchBtn.classList.toggle('fa-times');
    searchBar.classList.toggle('active');
});

formBtn.addEventListener('click', () =>{
    loginForm.classList.add('active');
});
 
formClose.addEventListener('click', () =>{
    loginForm.classList.remove('active');
});
/*
function submit(params){
    var tempParas ={
        user_name:document.getElementById("username").value,
        user_email:document.getElementById("useremail").value,
        message:document.getElementById("msg").value,
    };
    emailjs.send('service_264q319' 'template_l9bf6pj',tempParas )
    .then(function(res){
        console.log("sucess",res.status);
    })
}*/