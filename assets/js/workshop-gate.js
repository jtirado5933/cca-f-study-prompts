(function () {
  "use strict";

  // SHA-256 of the access code you give registrants (change before deploy).
  // Generate: echo -n 'YOUR-CODE' | sha256sum  (or PowerShell equivalent in README).
  var WORKSHOP_CODE_SHA256 =
    "276b5cd2cb57af8b75e832a9e0a707c1bdf82ce531043fe4675b9a799f92f4d0";
  var STORAGE_KEY = "ccar-f-workshop-unlocked";

  function normalizeCode(raw) {
    return String(raw || "").trim();
  }

  function sha256Hex(text) {
    if (!window.crypto || !window.crypto.subtle) {
      return Promise.reject(new Error("secure context required"));
    }
    var data = new TextEncoder().encode(text);
    return window.crypto.subtle.digest("SHA-256", data).then(function (buf) {
      return Array.from(new Uint8Array(buf))
        .map(function (b) {
          return b.toString(16).padStart(2, "0");
        })
        .join("");
    });
  }

  function unlock() {
    document.body.classList.remove("workshop-locked");
    try {
      localStorage.setItem(STORAGE_KEY, "1");
    } catch (e) {
      /* ignore */
    }
  }

  function isUnlocked() {
    try {
      return localStorage.getItem(STORAGE_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function init() {
    if (isUnlocked()) {
      unlock();
      return;
    }

    var form = document.getElementById("workshop-code-form");
    var input = document.getElementById("workshop-code-input");
    var errorEl = document.getElementById("workshop-gate-error");
    if (!form || !input) return;

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (errorEl) errorEl.hidden = true;

      var code = normalizeCode(input.value);
      sha256Hex(code)
        .then(function (hash) {
          if (hash === WORKSHOP_CODE_SHA256) {
            unlock();
            return;
          }
          if (errorEl) errorEl.hidden = false;
          input.focus();
          input.select();
        })
        .catch(function () {
          if (errorEl) {
            errorEl.textContent =
              "Unlock needs a secure connection (HTTPS). Open this page over HTTPS and try again.";
            errorEl.hidden = false;
          }
        });
    });

    if (window.location.hash === "#day-2" || window.location.hash === "#workshop") {
      var gate = document.getElementById("workshop-gate");
      if (gate) gate.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
