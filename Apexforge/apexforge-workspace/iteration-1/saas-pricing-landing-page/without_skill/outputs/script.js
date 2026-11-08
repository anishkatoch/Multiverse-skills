// Flowstack pricing page - small, self-contained interactions.
// 1) Monthly / Yearly billing toggle for the pricing cards
// 2) Accordion behaviour for the FAQ list

(function () {
  "use strict";

  /* ---------------- Billing toggle ---------------- */
  var toggleButtons = document.querySelectorAll(".toggle-btn");
  var priceAmounts = document.querySelectorAll(".price-amount");
  var billedAsLines = document.querySelectorAll(".plan-billed-as");

  function setPeriod(period) {
    toggleButtons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.dataset.period === period);
    });

    priceAmounts.forEach(function (el) {
      var value = el.dataset[period];
      if (value) el.textContent = value;
    });

    billedAsLines.forEach(function (el) {
      var text = el.dataset[period + "Text"];
      if (text) el.textContent = text;
    });
  }

  toggleButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setPeriod(btn.dataset.period);
    });
  });

  /* ---------------- FAQ accordion ---------------- */
  var faqItems = document.querySelectorAll(".faq-item");

  faqItems.forEach(function (item) {
    var question = item.querySelector(".faq-question");

    question.addEventListener("click", function () {
      var isOpen = item.classList.contains("is-open");

      // Close any other open item for a tidy single-open accordion.
      faqItems.forEach(function (other) {
        if (other !== item) {
          other.classList.remove("is-open");
          other.querySelector(".faq-question").setAttribute("aria-expanded", "false");
        }
      });

      item.classList.toggle("is-open", !isOpen);
      question.setAttribute("aria-expanded", String(!isOpen));
    });
  });
})();
