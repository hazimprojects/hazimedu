const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const isOpen = siteNav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

/* =========================
   TOGGLE JAWAPAN
========================= */
document.querySelectorAll(".interactive-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const targetId = button.getAttribute("data-target");
    if (!targetId) return;

    const target = document.getElementById(targetId);
    if (!target) return;

    const isOpen = target.classList.toggle("show");
    button.textContent = isOpen ? "Sembunyikan jawapan" : "Tunjukkan jawapan";
  });
});

/* =========================
   PAPER TABS
========================= */
const paperTabs = document.querySelectorAll(".paper-tab");
const paperTabPanels = document.querySelectorAll(".paper-tab-panel");

paperTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const targetId = tab.getAttribute("data-tab");
    if (!targetId) return;

    paperTabs.forEach((item) => item.classList.remove("active"));
    paperTabPanels.forEach((panel) => panel.classList.remove("active"));

    tab.classList.add("active");

    const targetPanel = document.getElementById(targetId);
    if (targetPanel) {
      targetPanel.classList.add("active");
    }
  });
});

/* =========================
   PAPER TIMELINE
========================= */
const paperTimelineNodes = document.querySelectorAll(".paper-timeline-node");
const paperTimelinePanels = document.querySelectorAll(".paper-timeline-panel");

paperTimelineNodes.forEach((node) => {
  node.addEventListener("click", () => {
    const targetId = node.getAttribute("data-timeline");
    if (!targetId) return;

    paperTimelineNodes.forEach((item) => item.classList.remove("active"));
    paperTimelinePanels.forEach((panel) => panel.classList.remove("active"));

    node.classList.add("active");

    const targetPanel = document.getElementById(targetId);
    if (targetPanel) {
      targetPanel.classList.add("active");
    }
  });
});

/* =========================
   REVEAL ON SCROLL
========================= */
const revealElements = document.querySelectorAll(".reveal-on-scroll");

function revealOnScroll() {
  revealElements.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 70) {
      el.classList.add("visible");
    }
  });
}

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);
