// Mobile Menu
const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");

if(menuBtn){
    menuBtn.onclick = () => {
        navLinks.classList.toggle("active");
    };
}

// Scroll Reveal
const reveals = document.querySelectorAll(".reveal");

function revealOnScroll(){

    reveals.forEach(section=>{

        const top = section.getBoundingClientRect().top;

        const visible = window.innerHeight - 120;

        if(top < visible){
            section.classList.add("active");
        }

    });

}

window.addEventListener("scroll",revealOnScroll);

revealOnScroll();

// Scroll Progress Bar

window.addEventListener("scroll",()=>{

const scrollTop=document.documentElement.scrollTop;

const scrollHeight=document.documentElement.scrollHeight-document.documentElement.clientHeight;

const progress=(scrollTop/scrollHeight)*100;

document.getElementById("progress-bar").style.width=progress+"%";

});