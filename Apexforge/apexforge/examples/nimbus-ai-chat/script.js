(() => {
  const messageList = document.getElementById("messageList");
  const emptyState = document.getElementById("emptyState");
  const composerForm = document.getElementById("composerForm");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const historyList = document.getElementById("historyList");
  const sidebar = document.getElementById("sidebar");
  const scrim = document.getElementById("scrim");
  const clearChatBtn = document.getElementById("clearChat");
  const themeToggle = document.getElementById("themeToggle");
  const scrollBottomBtn = document.getElementById("scrollBottomBtn");

  const HISTORY = [
    { id: "h1", title: "Quantum computing explained", active: true },
    { id: "h2", title: "Kyoto 3-day itinerary" },
    { id: "h3", title: "Debugging an infinite loop" },
    { id: "h4", title: "Email: deadline extension" },
    { id: "h5", title: "Weekly meal plan ideas" },
  ];

  const ICON_HISTORY = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M21 12a9 9 0 11-3-6.7M21 4v5h-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

  function renderHistory() {
    historyList.innerHTML = "";
    HISTORY.forEach((item) => {
      const btn = document.createElement("button");
      btn.className = "history-item" + (item.active ? " is-active" : "");
      btn.innerHTML = `${ICON_HISTORY}<span>${escapeHtml(item.title)}</span>`;
      btn.addEventListener("click", () => {
        HISTORY.forEach((h) => (h.active = h.id === item.id));
        renderHistory();
        closeSidebar();
      });
      historyList.appendChild(btn);
    });
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function formatTime() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function hideEmptyState() {
    if (emptyState.parentElement) emptyState.remove();
  }

  function renderInline(text) {
    // Minimal, safe markdown: escape first, then allow **bold** and `code`.
    return escapeHtml(text)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/`([^`]+?)`/g, "<code>$1</code>");
  }

  function appendMessage(role, text) {
    // A user's own outgoing message always snaps to bottom; an incoming
    // bot message only does if they hadn't scrolled away to read history.
    const wasNearBottom = role === "user" ? true : isNearBottom();
    hideEmptyState();
    const row = document.createElement("div");
    row.className = "message-row " + (role === "user" ? "is-user" : "is-bot");

    const avatar = document.createElement("span");
    avatar.className = "avatar " + (role === "user" ? "avatar--user" : "avatar--bot");
    avatar.innerHTML =
      role === "user"
        ? "JK"
        : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor"/></svg>`;

    const content = document.createElement("div");
    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = renderInline(text);

    const metaRow = document.createElement("div");
    metaRow.className = "message-meta-row";
    const meta = document.createElement("span");
    meta.className = "message-meta";
    meta.textContent = formatTime();
    metaRow.appendChild(meta);

    if (role === "bot") {
      const actions = document.createElement("div");
      actions.className = "message-actions";

      const copyBtn = document.createElement("button");
      copyBtn.type = "button";
      copyBtn.className = "msg-action-btn";
      copyBtn.setAttribute("aria-label", "Copy response");
      copyBtn.title = "Copy";
      const copyIcon = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none"><rect x="8" y="8" width="12" height="12" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M4 16V5a1 1 0 011-1h11" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>`;
      const checkIcon = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M5 12l5 5L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
      copyBtn.innerHTML = copyIcon;
      copyBtn.addEventListener("click", () => {
        navigator.clipboard?.writeText(text).catch(() => {});
        copyBtn.innerHTML = checkIcon;
        copyBtn.classList.add("is-copied");
        setTimeout(() => {
          copyBtn.innerHTML = copyIcon;
          copyBtn.classList.remove("is-copied");
        }, 1500);
      });

      const upBtn = document.createElement("button");
      upBtn.type = "button";
      upBtn.className = "msg-action-btn";
      upBtn.setAttribute("aria-label", "Good response");
      upBtn.title = "Good response";
      upBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M7 11v8H4v-8h3zm0 0l3.5-7a2 2 0 013.6 1.4L13 9h4.5a2 2 0 011.9 2.7l-2 6A2 2 0 0115.5 19H7" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>`;

      const downBtn = document.createElement("button");
      downBtn.type = "button";
      downBtn.className = "msg-action-btn";
      downBtn.setAttribute("aria-label", "Bad response");
      downBtn.title = "Bad response";
      downBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M17 13V5h3v8h-3zm0 0l-3.5 7a2 2 0 01-3.6-1.4L11 15H6.5a2 2 0 01-1.9-2.7l2-6A2 2 0 018.5 5H17" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>`;

      function toggleFeedback(btn, other) {
        btn.addEventListener("click", () => {
          const wasActive = btn.classList.contains("is-active");
          btn.classList.toggle("is-active", !wasActive);
          if (!wasActive) other.classList.remove("is-active");
        });
      }
      toggleFeedback(upBtn, downBtn);
      toggleFeedback(downBtn, upBtn);

      actions.appendChild(copyBtn);
      actions.appendChild(upBtn);
      actions.appendChild(downBtn);
      metaRow.appendChild(actions);
    }

    content.appendChild(bubble);
    content.appendChild(metaRow);

    row.appendChild(avatar);
    row.appendChild(content);
    messageList.appendChild(row);
    scrollToBottomIfNear(wasNearBottom);
  }

  function showTyping() {
    const wasNearBottom = isNearBottom();
    const row = document.createElement("div");
    row.className = "typing-row";
    row.id = "typingRow";
    row.innerHTML = `
      <span class="avatar avatar--bot"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5z" fill="currentColor"/></svg></span>
      <div class="typing-dots"><span></span><span></span><span></span></div>
    `;
    messageList.appendChild(row);
    scrollToBottomIfNear(wasNearBottom);
  }

  function hideTyping() {
    const row = document.getElementById("typingRow");
    if (row) row.remove();
  }

  function scrollToBottom() {
    messageList.scrollTop = messageList.scrollHeight;
    scrollBottomBtn.hidden = true;
  }

  // Auto-scroll only if the user was already near the bottom - otherwise
  // a new message would yank them away from history they're reading.
  function scrollToBottomIfNear(wasNearBottom) {
    if (wasNearBottom) {
      scrollToBottom();
    } else {
      scrollBottomBtn.hidden = false;
    }
  }

  const CANNED_REPLIES = [
    "That's a great question. In a real deployment this is where a model response would stream in - but for this demo, here's a simulated reply so you can see how the conversation flows.",
    "Here's a simulated response demonstrating multi-line formatting:\n\n1. This UI is fully static on the frontend\n2. Replies are mocked with a short delay\n3. Swap this logic for a real API call when you're ready",
    "I don't have a real backend wired up in this demo, but the interaction model - typing indicator, bubble layout, auto-scroll - works exactly as it would with a live model.",
    "Got it. This is a placeholder reply so the chat feels alive during the demo; wire up your model's API in script.js to replace it.",
  ];

  let replyIndex = 0;

  function respondTo(userText) {
    showTyping();
    const delay = 700 + Math.random() * 700;
    setTimeout(() => {
      hideTyping();
      const reply = CANNED_REPLIES[replyIndex % CANNED_REPLIES.length];
      replyIndex += 1;
      appendMessage("bot", reply);
    }, delay);
  }

  function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    appendMessage("user", text);
    messageInput.value = "";
    autoResize();
    updateSendState();
    respondTo(text);
  }

  composerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage();
  });

  messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function updateSendState() {
    sendBtn.disabled = messageInput.value.trim().length === 0;
  }

  function autoResize() {
    messageInput.style.height = "auto";
    messageInput.style.height = Math.min(messageInput.scrollHeight, 160) + "px";
  }

  messageInput.addEventListener("input", () => {
    updateSendState();
    autoResize();
  });

  document.querySelectorAll(".suggestion-card").forEach((card) => {
    card.addEventListener("click", () => {
      messageInput.value = card.dataset.prompt;
      updateSendState();
      autoResize();
      sendMessage();
    });
  });

  clearChatBtn.addEventListener("click", () => {
    messageList.innerHTML = "";
    messageList.appendChild(emptyState);
  });

  // ---------- Mobile sidebar ----------
  function openSidebar() {
    sidebar.classList.add("is-open");
    scrim.classList.add("is-visible");
  }
  function closeSidebar() {
    sidebar.classList.remove("is-open");
    scrim.classList.remove("is-visible");
  }
  document.getElementById("openSidebar").addEventListener("click", openSidebar);
  document.getElementById("closeSidebar").addEventListener("click", closeSidebar);
  scrim.addEventListener("click", closeSidebar);

  function startNewChat() {
    HISTORY.forEach((h) => (h.active = false));
    renderHistory();
    messageList.innerHTML = "";
    messageList.appendChild(emptyState);
    messageInput.value = "";
    updateSendState();
    closeSidebar();
  }
  document.getElementById("newChatBtn").addEventListener("click", startNewChat);
  document.getElementById("mobileNewChat").addEventListener("click", startNewChat);

  // ---------- Theme toggle ----------
  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    themeToggle.setAttribute("aria-pressed", String(theme === "light"));
    themeToggle.setAttribute(
      "aria-label",
      theme === "light" ? "Switch to dark theme" : "Switch to light theme"
    );
    try {
      localStorage.setItem("nimbus-theme", theme);
    } catch (e) {}
  }

  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    setTheme(current === "light" ? "dark" : "light");
  });

  setTheme(document.documentElement.getAttribute("data-theme") || "dark");

  // ---------- Scroll-to-bottom button ----------
  function isNearBottom() {
    return messageList.scrollHeight - messageList.scrollTop - messageList.clientHeight < 80;
  }

  messageList.addEventListener("scroll", () => {
    scrollBottomBtn.hidden = isNearBottom();
  });

  scrollBottomBtn.addEventListener("click", scrollToBottom);

  renderHistory();
  updateSendState();
})();
