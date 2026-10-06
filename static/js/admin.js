/* ---------------------------------------------------------
   Mobile sidebar toggle
--------------------------------------------------------- */
(function () {
    const sidebar = document.getElementById("adminSidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const openBtn = document.getElementById("sidebarToggleBtn");
    const closeBtn = document.getElementById("sidebarCloseBtn");

    function openSidebar() {
        if (sidebar) sidebar.classList.add("open");
        if (overlay) overlay.classList.add("show");
    }
    function closeSidebar() {
        if (sidebar) sidebar.classList.remove("open");
        if (overlay) overlay.classList.remove("show");
    }

    if (openBtn) openBtn.addEventListener("click", openSidebar);
    if (closeBtn) closeBtn.addEventListener("click", closeSidebar);
    if (overlay) overlay.addEventListener("click", closeSidebar);
})();

/* ---------------------------------------------------------
   Confirm before destructive actions (delete forms)
--------------------------------------------------------- */
document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (e) => {
        const message = form.getAttribute("data-confirm") || "Are you sure?";
        if (!window.confirm(message)) {
            e.preventDefault();
        }
    });
});

/* ---------------------------------------------------------
   Project form — link mode segmented control shows/hides
   the relevant URL fields
--------------------------------------------------------- */
(function () {
    const radios = document.querySelectorAll('input[name="link_mode"]');
    if (!radios.length) return;

    function sync() {
        const selected = document.querySelector('input[name="link_mode"]:checked');
        const value = selected ? selected.value : "none";

        document.querySelectorAll("[data-link-fields]").forEach((el) => {
            const forMode = el.getAttribute("data-link-fields");
            el.classList.toggle("is-hidden", forMode !== value);
        });
    }

    radios.forEach((radio) => radio.addEventListener("change", sync));
    sync();
})();

/* ---------------------------------------------------------
   Project form — image preview on file select, remove-image checkbox
--------------------------------------------------------- */
(function () {
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");
    const removeCheckbox = document.getElementById("removeImageCheckbox");

    if (input && preview) {
        input.addEventListener("change", () => {
            const file = input.files && input.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
            if (removeCheckbox) removeCheckbox.checked = false;
        });
    }

    if (removeCheckbox && preview) {
        removeCheckbox.addEventListener("change", () => {
            if (removeCheckbox.checked) {
                preview.innerHTML = `<span>🖼️</span>`;
                if (input) input.value = "";
            }
        });
    }
})();

/* ---------------------------------------------------------
   Testimonial form — clickable star rating picker
--------------------------------------------------------- */
(function () {
    const picker = document.getElementById("starPicker");
    const ratingInput = document.getElementById("ratingInput");
    if (!picker || !ratingInput) return;

    const stars = Array.from(picker.querySelectorAll(".star"));

    function paint(value) {
        stars.forEach((star) => {
            star.classList.toggle("is-filled", Number(star.dataset.value) <= value);
        });
    }

    stars.forEach((star) => {
        star.addEventListener("click", () => {
            const value = Number(star.dataset.value);
            ratingInput.value = value;
            paint(value);
        });
        star.addEventListener("mouseenter", () => paint(Number(star.dataset.value)));
    });

    picker.addEventListener("mouseleave", () => paint(Number(ratingInput.value)));

    paint(Number(ratingInput.value) || 5);
})();

/* ---------------------------------------------------------
   Enquiries — expand/collapse full message
--------------------------------------------------------- */
document.querySelectorAll("[data-toggle-message]").forEach((btn) => {
    btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-toggle-message");
        const target = document.getElementById(targetId);
        if (!target) return;
        const isOpen = target.style.display !== "none";
        target.style.display = isOpen ? "none" : "block";
        btn.textContent = isOpen ? "Read message ▾" : "Hide message ▴";
    });
});
