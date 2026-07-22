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

// Animated Counter

const counters = document.querySelectorAll(".counter");

const animateCounter = () => {

    counters.forEach(counter => {

        const target = +counter.dataset.target;

        let count = 0;

        const speed = target / 60;

        const update = () => {

            count += speed;

            if(count < target){

                counter.innerText = Math.floor(count);

                requestAnimationFrame(update);

            }else{

                counter.innerText = target + "+";

            }

        }

        update();

    });

}

animateCounter();

// Navbar Shadow

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll",()=>{

if(window.scrollY>30){

navbar.classList.add("scrolled");

}else{

navbar.classList.remove("scrolled");

}

});

// Back To Top

const topBtn = document.getElementById("topBtn");

window.addEventListener("scroll",()=>{

    if(window.scrollY > 500){

        topBtn.style.display="flex";

        topBtn.style.alignItems="center";

        topBtn.style.justifyContent="center";

    }else{

        topBtn.style.display="none";

    }

});

topBtn.onclick=()=>{

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

};

// Active Navigation

const sections = document.querySelectorAll("section");
const navItems = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 120;

        if(window.scrollY >= sectionTop){

            current = section.getAttribute("id");

        }

    });

    navItems.forEach(link => {

        link.classList.remove("active");

        if(link.getAttribute("href") === "#" + current){

            link.classList.add("active");

        }

    });

});

// Loader

window.addEventListener("load",()=>{

    const loader=document.getElementById("loader");

    loader.style.opacity="0";

    setTimeout(()=>{

    loader.style.display="none";

    },600);

});

const form = document.querySelector("form");

if(form){

form.addEventListener("submit", ()=>{

const btn = form.querySelector("button");

btn.innerHTML = "Sending...";

btn.disabled = true;

});

}