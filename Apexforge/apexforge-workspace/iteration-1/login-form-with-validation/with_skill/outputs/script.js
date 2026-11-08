(function () {
  "use strict";

  var form = document.getElementById("loginForm");
  var emailInput = document.getElementById("email");
  var passwordInput = document.getElementById("password");
  var rememberInput = document.getElementById("rememberMe");
  var emailError = document.getElementById("emailError");
  var passwordError = document.getElementById("passwordError");
  var submitBtn = document.getElementById("submitBtn");
  var btnLabel = submitBtn.querySelector(".btn-label");
  var spinner = submitBtn.querySelector(".spinner");
  var togglePasswordBtn = document.getElementById("togglePassword");
  var eyeIcon = togglePasswordBtn.querySelector(".icon-eye");
  var eyeOffIcon = togglePasswordBtn.querySelector(".icon-eye-off");
  var banner = document.getElementById("formBanner");
  var forgotLink = document.getElementById("forgotLink");
  var signupLink = document.getElementById("signupLink");

  var STORAGE_KEY = "aurora_remembered_email";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Restore remembered email on load.
  try {
    var remembered = window.localStorage.getItem(STORAGE_KEY);
    if (remembered) {
      emailInput.value = remembered;
      rememberInput.checked = true;
    }
  } catch (err) {
    // localStorage unavailable (private mode, etc.) - fail silently, non-critical.
  }

  function showBanner(message, isError) {
    banner.textContent = message;
    banner.hidden = false;
    banner.style.background = isError ? "var(--color-error-soft)" : "var(--color-accent-soft)";
    banner.style.color = isError ? "var(--color-error)" : "var(--color-accent)";
    banner.style.borderColor = isError
      ? "color-mix(in srgb, var(--color-error) 25%, transparent)"
      : "color-mix(in srgb, var(--color-accent) 25%, transparent)";
  }

  function hideBanner() {
    banner.hidden = true;
    banner.textContent = "";
  }

  function setFieldError(inputEl, errorEl, message) {
    var field = inputEl.closest(".field");
    if (message) {
      field.classList.add("has-error");
      errorEl.textContent = message;
      inputEl.setAttribute("aria-invalid", "true");
    } else {
      field.classList.remove("has-error");
      errorEl.textContent = "";
      inputEl.removeAttribute("aria-invalid");
    }
  }

  function validateEmail() {
    var value = emailInput.value.trim();
    if (!value) {
      setFieldError(emailInput, emailError, "Email address is required.");
      return false;
    }
    if (!EMAIL_RE.test(value)) {
      setFieldError(emailInput, emailError, "Enter a valid email address.");
      return false;
    }
    setFieldError(emailInput, emailError, "");
    return true;
  }

  function validatePassword() {
    var value = passwordInput.value;
    if (!value) {
      setFieldError(passwordInput, passwordError, "Password is required.");
      return false;
    }
    if (value.length < 8) {
      setFieldError(passwordInput, passwordError, "Password must be at least 8 characters.");
      return false;
    }
    setFieldError(passwordInput, passwordError, "");
    return true;
  }

  emailInput.addEventListener("blur", validateEmail);
  passwordInput.addEventListener("blur", validatePassword);

  emailInput.addEventListener("input", function () {
    if (emailInput.closest(".field").classList.contains("has-error")) {
      validateEmail();
    }
  });

  passwordInput.addEventListener("input", function () {
    if (passwordInput.closest(".field").classList.contains("has-error")) {
      validatePassword();
    }
  });

  togglePasswordBtn.addEventListener("click", function () {
    var isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";
    // Use a class, not the `hidden` attribute/property: SVG elements don't
    // reliably support `hidden` across browsers (and the JS `.hidden`
    // property doesn't always sync back to the content attribute), so toggling
    // it silently left both icons visible at once in testing.
    eyeIcon.classList.toggle("icon-is-hidden", isPassword);
    eyeOffIcon.classList.toggle("icon-is-hidden", !isPassword);
    togglePasswordBtn.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
    togglePasswordBtn.setAttribute("aria-pressed", isPassword ? "true" : "false");
  });

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    spinner.hidden = !isLoading;
    btnLabel.textContent = isLoading ? "Signing in…" : "Sign in";
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    hideBanner();

    var emailOk = validateEmail();
    var passwordOk = validatePassword();

    if (!emailOk || !passwordOk) {
      var firstInvalid = !emailOk ? emailInput : passwordInput;
      firstInvalid.focus();
      return;
    }

    setLoading(true);

    // No backend is wired up here - this simulates a network round trip so the
    // loading and success states are real and visible, rather than instant/fake.
    window.setTimeout(function () {
      setLoading(false);

      try {
        if (rememberInput.checked) {
          window.localStorage.setItem(STORAGE_KEY, emailInput.value.trim());
        } else {
          window.localStorage.removeItem(STORAGE_KEY);
        }
      } catch (err) {
        // ignore storage failures
      }

      showBanner(
        "Signed in as " + emailInput.value.trim() + ". Connect this form to your auth API to finish the flow.",
        false
      );
    }, 1100);
  });

  forgotLink.addEventListener("click", function (event) {
    event.preventDefault();
    var value = emailInput.value.trim();
    if (value && EMAIL_RE.test(value)) {
      showBanner("If an account exists for " + value + ", password reset instructions have been sent.", false);
    } else {
      showBanner("Enter your email address above first, then click “Forgot password?” again.", true);
      emailInput.focus();
    }
  });

  signupLink.addEventListener("click", function (event) {
    event.preventDefault();
    showBanner("This would take you to the sign-up page - wire up a route to continue.", false);
  });
})();
