let menu = document.querySelector('.menu');
let userheader = document.querySelector('.userheader');
let userheader_container = document.querySelector('.userheader_container');

menu.onclick = function () {
    userheader.classList.toggle('active');
}
userheader.onclick = function () {
    userheader_container.classList.toggle('active');
}