/* ReviewBriefs — main.js */

(function () {
  'use strict';

  // ---- Current year in footer ----
  const yearEl = document.getElementById('current-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // ---- Mobile nav toggle ----
  const navToggle = document.querySelector('.nav-toggle');
  const mobileNav = document.querySelector('.site-nav__mobile');

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      navToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    // Close mobile nav when a link is clicked
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Open menu');
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!navToggle.contains(e.target) && !mobileNav.contains(e.target)) {
        mobileNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---- Print helper ----
  const printBtns = document.querySelectorAll('[data-action="print"]');
  printBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.print();
    });
  });

  // ---- Pricing billing toggle ----
  window.toggleBilling = function () {
    const toggle = document.getElementById('billing-toggle');
    if (!toggle) return;
    const isAnnual = toggle.getAttribute('aria-checked') === 'true';
    const nowAnnual = !isAnnual;

    toggle.setAttribute('aria-checked', String(nowAnnual));
    document.getElementById('toggle-thumb').style.left = nowAnnual ? '23px' : '3px';
    toggle.style.background = nowAnnual ? 'var(--rb-moss)' : 'var(--rb-stone)';
    document.getElementById('toggle-monthly').style.fontWeight = nowAnnual ? '400' : '600';
    document.getElementById('toggle-monthly').style.color = nowAnnual ? 'var(--rb-muted)' : 'var(--rb-ink)';
    document.getElementById('toggle-annual').style.color = nowAnnual ? 'var(--rb-ink)' : 'var(--rb-muted)';
    document.getElementById('toggle-annual').style.fontWeight = nowAnnual ? '600' : '400';

    document.querySelectorAll('.price-amount').forEach(function (el) {
      el.textContent = nowAnnual ? el.dataset.annual : el.dataset.monthly;
    });
    document.querySelectorAll('.price-annual-note').forEach(function (el) {
      el.style.display = nowAnnual ? 'block' : 'none';
    });
    document.querySelectorAll('.price-monthly-note').forEach(function (el) {
      el.style.display = nowAnnual ? 'none' : 'block';
    });
  };

  // ---- Active nav link ----
  const currentPath = window.location.pathname;
  document.querySelectorAll('.site-nav__link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && (currentPath === href || currentPath.startsWith(href.replace('index.html', '')))) {
      link.classList.add('active');
    }
  });

})();
