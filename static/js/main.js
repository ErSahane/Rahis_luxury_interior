window.addEventListener("load", () => {
  document.getElementById("loader")?.classList.add("hide");
});

AOS.init({ once: true, duration: 850, offset: 80 });

new Swiper(".hero-swiper", {
  loop: true,
  effect: "fade",
  autoplay: { delay: 4200, disableOnInteraction: false },
  speed: 1200,
});

new Swiper(".review-swiper", {
  loop: true,
  slidesPerView: 1,
  spaceBetween: 18,
  autoplay: { delay: 3200 },
  breakpoints: { 768: { slidesPerView: 2 }, 1100: { slidesPerView: 3 } },
});

GLightbox({ selector: ".glightbox", touchNavigation: true, loop: true });

document.querySelectorAll("[data-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const filter = button.dataset.filter;
    document.querySelectorAll(".portfolio-item").forEach((item) => {
      item.style.display = filter === "all" || item.dataset.category === filter ? "block" : "none";
    });
  });
});

const counters = document.querySelectorAll(".counter");
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const target = Number(entry.target.dataset.target || entry.target.textContent);
    let value = 0;
    const step = Math.max(1, Math.ceil(target / 70));
    const timer = setInterval(() => {
      value += step;
      entry.target.textContent = value >= target ? target : value;
      if (value >= target) clearInterval(timer);
    }, 22);
    countObserver.unobserve(entry.target);
  });
});
counters.forEach((counter) => countObserver.observe(counter));

const compareRange = document.getElementById("compareRange");
const compareAfter = document.getElementById("compareAfter");
compareRange?.addEventListener("input", (event) => {
  compareAfter.style.width = `${event.target.value}%`;
});

const themeToggle = document.getElementById("themeToggle");
const savedTheme = localStorage.getItem("rahis-theme");
if (savedTheme) document.documentElement.dataset.theme = savedTheme;
themeToggle?.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("rahis-theme", next);
  themeToggle.innerHTML = next === "dark" ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
});

document.getElementById("closePop")?.addEventListener("click", () => {
  document.getElementById("enquiryPop").style.display = "none";
});


window.addEventListener("load", function () {
    document.getElementById("loader").classList.add("hide");
});