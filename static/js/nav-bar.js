const menuBtn = document.querySelector(".menu-btn-mobile");
const menuLinks = document.querySelector(".nav-links-mobile");
const menuIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", () => {

    menuLinks.classList.toggle("ativo");

    if (menuLinks.classList.contains("ativo")) {

        menuIcon.classList.remove("fa-bars");
        menuIcon.classList.add("fa-xmark");

    } else {

        menuIcon.classList.remove("fa-xmark");
        menuIcon.classList.add("fa-bars");

    }

});