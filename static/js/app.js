const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const isTouch = window.matchMedia("(hover:none), (pointer:coarse)").matches;

/* ---------------------------------------------------------
   Mobile Menu
--------------------------------------------------------- */
const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");

if (menuBtn && navLinks) {
    menuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("active");
        menuBtn.classList.toggle("open");
    });

    navLinks.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("active");
            menuBtn.classList.remove("open");
        });
    });
}

/* ---------------------------------------------------------
   Scroll Reveal — IntersectionObserver with stagger
--------------------------------------------------------- */
const reveals = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });

    reveals.forEach(el => io.observe(el));

    // Stagger children inside grid sections
    document.querySelectorAll(".services-grid, .why-grid, .projects-grid, .testimonial-grid").forEach(grid => {
        [...grid.children].forEach((child, i) => {
            child.classList.add("reveal");
            child.style.setProperty("--d", (i * 0.08) + "s");
            io.observe(child);
        });
    });
} else {
    reveals.forEach(el => el.classList.add("active"));
}

/* ---------------------------------------------------------
   Scroll Progress Bar
--------------------------------------------------------- */
const progressBar = document.getElementById("progress-bar");

function updateProgress() {
    const scrollTop = document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = progress + "%";
}

/* ---------------------------------------------------------
   Animated Counter (triggers once, on view)
--------------------------------------------------------- */
const counters = document.querySelectorAll(".counter");

function animateCounter(counter) {
    const target = +counter.dataset.target;
    let count = 0;
    const duration = 1400;
    const start = performance.now();

    function update(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        count = Math.floor(eased * target);
        counter.innerText = progress < 1 ? count : target + "+";
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

if ("IntersectionObserver" in window && counters.length) {
    const counterIO = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterIO.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    counters.forEach(c => counterIO.observe(c));
} else {
    counters.forEach(animateCounter);
}

/* ---------------------------------------------------------
   Back To Top (declared early — referenced by scroll handler below)
--------------------------------------------------------- */
const topBtn = document.getElementById("topBtn");
if (topBtn) {
    topBtn.style.alignItems = "center";
    topBtn.style.justifyContent = "center";
    topBtn.onclick = () => window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ---------------------------------------------------------
   Navbar scroll state + active section link + progress bar
   (single rAF-throttled scroll handler)
--------------------------------------------------------- */
const navbar = document.querySelector(".navbar");
const sections = document.querySelectorAll("section[id]");
const navItems = document.querySelectorAll(".nav-links a");
let ticking = false;

function onScrollFrame() {
    updateProgress();

    if (navbar) {
        navbar.classList.toggle("scrolled", window.scrollY > 30);
    }

    let current = "";
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 130;
        if (window.scrollY >= sectionTop) current = section.getAttribute("id");
    });
    navItems.forEach(link => {
        link.classList.toggle("active", link.getAttribute("href") === "#" + current);
    });

    if (topBtn) topBtn.style.display = window.scrollY > 500 ? "flex" : "none";

    ticking = false;
}

window.addEventListener("scroll", () => {
    if (!ticking) {
        requestAnimationFrame(onScrollFrame);
        ticking = true;
    }
});
onScrollFrame();

/* ---------------------------------------------------------
   Loader — terminal boot sequence
--------------------------------------------------------- */
window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    if (!loader) return;
    const delay = prefersReducedMotion ? 150 : 1300;
    setTimeout(() => {
        loader.style.opacity = "0";
        loader.style.visibility = "hidden";
        setTimeout(() => { loader.style.display = "none"; }, 650);
    }, delay);
});

/* ---------------------------------------------------------
   Contact form
--------------------------------------------------------- */
const contactForm = document.getElementById("contactForm");
const successMessage = document.getElementById("successMessage");
const submitBtn = document.getElementById("submitBtn");

if (contactForm) {
    contactForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        submitBtn.disabled = true;
        submitBtn.textContent = "⏳ Sending...";

        const formData = new FormData(contactForm);

        try {
            const response = await fetch("/contact", { method: "POST", body: formData });
            const data = await response.json();

            successMessage.textContent = data.message;
            successMessage.style.display = "block";

            if (data.success) {
                contactForm.reset();
                submitBtn.textContent = "✅ Request Sent";
            } else {
                submitBtn.disabled = false;
                submitBtn.textContent = "🚀 Send Project Request";
            }
        } catch (error) {
            console.error("Contact error:", error);
            successMessage.textContent = "❌ Something went wrong. Please try again.";
            successMessage.style.display = "block";
            submitBtn.disabled = false;
            submitBtn.textContent = "🚀 Send Project Request";
        }
    });
}

/* ---------------------------------------------------------
   Project modal (BrightHeaven)
--------------------------------------------------------- */
function openBrightheaven() {
    document.getElementById("brightheavenModal").classList.add("active");
}
function closeBrightheaven() {
    document.getElementById("brightheavenModal").classList.remove("active");
}
window.openBrightheaven = openBrightheaven;
window.closeBrightheaven = closeBrightheaven;

/* ---------------------------------------------------------
   Offer Popup
--------------------------------------------------------- */
const offerPopup = document.getElementById("offerPopup");
const offerClose = document.getElementById("offerClose");

if (offerPopup && offerClose) {
    setTimeout(() => offerPopup.classList.add("show"), 10000);

    offerClose.addEventListener("click", () => offerPopup.classList.remove("show"));
    offerPopup.addEventListener("click", (e) => {
        if (e.target === offerPopup) offerPopup.classList.remove("show");
    });
}

/* ---------------------------------------------------------
   Custom cursor (desktop only)
--------------------------------------------------------- */
if (!isTouch && !prefersReducedMotion) {
    const dot = document.createElement("div");
    dot.className = "cursor-dot";
    const ring = document.createElement("div");
    ring.className = "cursor-ring";
    document.body.append(dot, ring);

    let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;

    window.addEventListener("mousemove", (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%,-50%)`;
    });

    function loopCursor() {
        ringX += (mouseX - ringX) * 0.18;
        ringY += (mouseY - ringY) * 0.18;
        ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%,-50%)`;
        requestAnimationFrame(loopCursor);
    }
    loopCursor();

    document.querySelectorAll("a, button, .service-card, .project-card, .why-card, .testimonial-card, input, textarea")
        .forEach(el => {
            el.addEventListener("mouseenter", () => ring.classList.add("hovering"));
            el.addEventListener("mouseleave", () => ring.classList.remove("hovering"));
        });
}

/* ---------------------------------------------------------
   Magnetic buttons
--------------------------------------------------------- */
if (!isTouch && !prefersReducedMotion) {
    document.querySelectorAll(".btn-primary, .btn-secondary, .nav-btn").forEach(btn => {
        btn.classList.add("magnetic");
        btn.addEventListener("mousemove", (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.18}px, ${y * 0.35}px)`;
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "translate(0,0)";
        });
    });
}

/* ---------------------------------------------------------
   Tilt on hero browser mockup + service/why/testimonial cards
--------------------------------------------------------- */
if (!isTouch && !prefersReducedMotion) {
    function attachTilt(el, strength = 10) {
        el.addEventListener("mousemove", (e) => {
            const rect = el.getBoundingClientRect();
            const px = (e.clientX - rect.left) / rect.width;
            const py = (e.clientY - rect.top) / rect.height;
            const rx = (py - 0.5) * -strength;
            const ry = (px - 0.5) * strength;
            el.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;

            if (el.classList.contains("service-card")) {
                el.style.setProperty("--mx", (px * 100) + "%");
                el.style.setProperty("--my", (py * 100) + "%");
            }
        });
        el.addEventListener("mouseleave", () => {
            el.style.transform = "rotateX(0) rotateY(0)";
        });
    }

    const laptopCard = document.querySelector(".laptop-card");
    if (laptopCard) attachTilt(laptopCard, 8);

    document.querySelectorAll(".service-card").forEach(el => attachTilt(el, 6));
}

/* ---------------------------------------------------------
   Hero typewriter — cycles through what OKWebStudio builds
--------------------------------------------------------- */
(function typewriter() {
    const el = document.querySelector(".typed-wrap");
    if (!el) return;

    const words = ["businesses.", "schools.", "brands.", "stores."];

    if (prefersReducedMotion) {
        el.textContent = words[0];
        return;
    }

    let wordIndex = 0, charIndex = 0, deleting = false;

    function tick() {
        const word = words[wordIndex];

        if (!deleting) {
            charIndex++;
            el.textContent = word.slice(0, charIndex);
            if (charIndex === word.length) {
                deleting = true;
                setTimeout(tick, 1400);
                return;
            }
        } else {
            charIndex--;
            el.textContent = word.slice(0, charIndex);
            if (charIndex === 0) {
                deleting = false;
                wordIndex = (wordIndex + 1) % words.length;
            }
        }

        setTimeout(tick, deleting ? 45 : 85);
    }

    tick();
})();
