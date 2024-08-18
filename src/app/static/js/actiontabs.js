let menuToggle = document.querySelector('.toggle');
let tab = document.querySelector('.tab');
menuToggle.onclick = function(){
    tab.classList.toggle('active');
}