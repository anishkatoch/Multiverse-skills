(function () {
  'use strict';

  /* ---------------- Mobile nav toggle ---------------- */
  var navToggle = document.getElementById('navToggle');
  var mobileNav = document.getElementById('mobileNav');

  function closeMobileNav() {
    mobileNav.classList.remove('is-open');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Open menu');
  }

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = mobileNav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      navToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    // Close mobile nav when a link inside it is clicked
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMobileNav);
    });

    // Close on escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMobileNav();
    });

    // Close if viewport grows past the mobile breakpoint
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 900) closeMobileNav();
    });
  }

  /* ---------------- Billing toggle (monthly / annual) ---------------- */
  var btnAnnual = document.getElementById('btnAnnual');
  var btnMonthly = document.getElementById('btnMonthly');
  var priceAmounts = document.querySelectorAll('.price-amount');
  var priceNotes = document.querySelectorAll('.price-note');

  function setBillingPeriod(period) {
    var isAnnual = period === 'annual';

    btnAnnual.classList.toggle('is-active', isAnnual);
    btnMonthly.classList.toggle('is-active', !isAnnual);
    btnAnnual.setAttribute('aria-pressed', String(isAnnual));
    btnMonthly.setAttribute('aria-pressed', String(!isAnnual));

    priceAmounts.forEach(function (el) {
      var value = isAnnual ? el.getAttribute('data-annual') : el.getAttribute('data-monthly');
      el.textContent = value;
    });

    priceNotes.forEach(function (el) {
      el.textContent = isAnnual
        ? el.getAttribute('data-annual-note')
        : el.getAttribute('data-monthly-note');
    });
  }

  if (btnAnnual && btnMonthly) {
    btnAnnual.addEventListener('click', function () { setBillingPeriod('annual'); });
    btnMonthly.addEventListener('click', function () { setBillingPeriod('monthly'); });
  }

  /* ---------------- FAQ accordion ---------------- */
  var faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(function (item) {
    var question = item.querySelector('.faq-question');
    var answer = item.querySelector('.faq-answer');

    question.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');

      // Close all other items (single-open accordion)
      faqItems.forEach(function (other) {
        if (other !== item) {
          other.classList.remove('is-open');
          other.querySelector('.faq-question').setAttribute('aria-expanded', 'false');
          other.querySelector('.faq-answer').style.maxHeight = null;
        }
      });

      if (isOpen) {
        item.classList.remove('is-open');
        question.setAttribute('aria-expanded', 'false');
        answer.style.maxHeight = null;
      } else {
        item.classList.add('is-open');
        question.setAttribute('aria-expanded', 'true');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  /* ---------------- Demo button placeholder behavior ---------------- */
  var demoBtn = document.getElementById('demoBtn');
  if (demoBtn) {
    demoBtn.addEventListener('click', function (e) {
      e.preventDefault();
      // No real video to play in this standalone build - scroll to the
      // workflow illustration in the hero as a lightweight stand-in
      // instead of leaving the click dead.
      var visual = document.querySelector('.hero-visual');
      if (visual) visual.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
})();
