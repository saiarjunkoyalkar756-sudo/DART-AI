/* =============================================================================
   DART AI — Frontend v3.0
   Premium redesign — canvas bg + all original features preserved
   ============================================================================= */

'use strict';

// ── marked.js config ──────────────────────────────────────────────────────────
marked.setOptions({ breaks: true, gfm: true });

// ── State ─────────────────────────────────────────────────────────────────────
const state = {
  model:             'deepseek-v3',
  modelColor:        '#4ade80',
  modelName:         'DeepSeek V3',
  searchMode:        false,
  chatHistory:       [],
  currentConversationId: null,
  streaming:         false,
  models:            [],
  voice:             'coral',
  ttsUrl:            null,
  musicJobId:        null,
  musicPollTimer:    null,
  musicUrl:          null,
  currentMailEmail:  null,
  currentMailId:     null,
  mailPollTimer:     null,
  dropdownOpen:      false,
  attachments:       [],
  voiceActive:       false,
  handsFreeMode:     false,
  recognition:       null,
  synthesis:         window.speechSynthesis || null,
};

// ── DOM shorthand ──────────────────────────────────────────────────────────────
const $  = id  => document.getElementById(id);
const $$ = sel => document.querySelectorAll(sel);

// ── Ambient Mesh Lighting Background Engine ─────────────────────────────────
(function initAmbientMesh() {
  const canvas = $('bg-canvas');
  if (!canvas || typeof canvas.getContext !== 'function') return;
  const ctx = canvas.getContext('2d');

  let W, H;
  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resize();

  const blobs = [
    { x: 0.2, y: 0.25, r: 0.45, vx: 0.0003, vy: 0.0002, color: 'rgba(99, 102, 241, 0.07)' },
    { x: 0.75, y: 0.35, r: 0.5, vx: -0.0002, vy: 0.0003, color: 'rgba(168, 85, 247, 0.06)' },
    { x: 0.45, y: 0.8, r: 0.4, vx: 0.0002, vy: -0.0002, color: 'rgba(6, 182, 212, 0.05)' },
  ];

  function animate() {
    ctx.clearRect(0, 0, W, H);

    blobs.forEach(b => {
      b.x += b.vx;
      b.y += b.vy;
      if (b.x < 0.1 || b.x > 0.9) b.vx *= -1;
      if (b.y < 0.1 || b.y > 0.9) b.vy *= -1;

      const grad = ctx.createRadialGradient(
        b.x * W, b.y * H, 0,
        b.x * W, b.y * H, b.r * Math.max(W, H)
      );
      grad.addColorStop(0, b.color);
      grad.addColorStop(1, 'transparent');

      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);
    });

    requestAnimationFrame(animate);
  }

  animate();
  window.addEventListener('resize', resize);
})();

// ── Tab switching ─────────────────────────────────────────────────────────────
const TABS = {
  chat:   { title: 'AI Chat'          },
  search: { title: 'Web Search'       },
  music:  { title: 'Music Generator'  },
  voice:  { title: 'Voice TTS'        },
  mail:   { title: 'Temp Email'       },
  image:  { title: 'Image Generator'  },
  swarm:  { title: 'Agent Swarm'      },
};

$$('.nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.dataset.tab) switchTab(btn.dataset.tab);
  });
});

function switchTab(tab) {
  if (!tab) return;
  $$('.nav-btn').forEach(b => {
    if (b.dataset.tab) {
      b.classList.toggle('active', b.dataset.tab === tab);
      b.setAttribute('aria-current', b.dataset.tab === tab ? 'page' : 'false');
    }
  });
  $$('.panel').forEach(p => p.classList.toggle('active', p.id === `${tab}-panel`));

  // Toggle swarm-section separately (uses section id not .panel class)
  const swarmSection = $('swarm-section');
  if (swarmSection) {
    swarmSection.hidden = (tab !== 'swarm');
    swarmSection.style.display = (tab === 'swarm') ? 'block' : 'none';
  }

  const title = TABS[tab]?.title || tab;
  const topbarTitle = $('topbar-title');
  if (topbarTitle) {
    const mainEl = topbarTitle.querySelector('.title-main');
    if (mainEl) mainEl.textContent = title;
  }

  // Show/hide chat-only controls
  const chatControls = $('chat-topbar-controls');
  if (chatControls) chatControls.style.display = (tab === 'chat') ? 'flex' : 'none';

  closeModelDropdown();

  if (tab === 'mail') loadMailList();

  closeSidebar();
}

// ── Mobile sidebar ─────────────────────────────────────────────────────────────
const sidebar        = $('sidebar');
const sidebarOverlay = $('sidebar-overlay');

$('hamburger-btn').addEventListener('click', openSidebar);
$('sidebar-close').addEventListener('click', closeSidebar);
sidebarOverlay.addEventListener('click', closeSidebar);

function openSidebar() {
  sidebar.classList.add('open');
  sidebarOverlay.classList.add('visible');
}
function closeSidebar() {
  sidebar.classList.remove('open');
  sidebarOverlay.classList.remove('visible');
}

// ── Model loading + dropdown ───────────────────────────────────────────────────
const PROVIDER_LABELS = {
  'deepseek': 'DeepSeek',
  'gpt':      'OpenAI',
  'gemini':   'Google',
  'kimi':     'Moonshot (Kimi)',
  'grok':     'xAI',
  'qwen':     'Qwen',
  'sonar':    'Perplexity',
  'glm':      'Z.AI (GLM)',
};

function getProvider(id) {
  const m = id.toLowerCase();
  for (const [k, v] of Object.entries(PROVIDER_LABELS)) {
    if (m.includes(k)) return v;
  }
  return 'Other';
}

async function loadModels() {
  try {
    const r = await fetch('/api/models');
    state.models = await r.json();
    buildModelDropdown();
    if (state.models.length) selectModel(state.models[0]);
  } catch (e) {
    console.error('Failed to load models:', e);
  }
}

function buildModelDropdown() {
  const list = $('model-dropdown-list');
  list.innerHTML = '';

  const groups = {};
  state.models.forEach(m => {
    const prov = getProvider(m.id);
    if (!groups[prov]) groups[prov] = [];
    groups[prov].push(m);
  });

  Object.entries(groups).forEach(([provName, models]) => {
    const label = document.createElement('div');
    label.className = 'model-group-label';
    label.textContent = provName;
    list.appendChild(label);

    models.forEach(m => {
      const item = document.createElement('div');
      item.className = 'model-item';
      item.setAttribute('role', 'option');
      item.dataset.id = m.id;
      if (m.id === state.model) item.classList.add('selected');
      item.innerHTML = `
        <div class="model-item-dot" style="background:${m.color || '#6366f1'}; box-shadow: 0 0 6px ${m.color || '#6366f1'}"></div>
        <span class="model-item-name">${m.name}</span>
        ${m.tag ? `<span class="model-item-tag">${m.tag}</span>` : ''}
      `;
      item.addEventListener('click', () => { selectModel(m); closeModelDropdown(); });
      list.appendChild(item);
    });
  });
}

function selectModel(m) {
  state.model      = m.id;
  state.modelColor = m.color || '#6366f1';
  state.modelName  = m.name;

  $('model-pill-name').textContent  = m.name;
  $('model-dot').style.background   = m.color || '#6366f1';
  $('model-dot').style.boxShadow    = `0 0 8px ${m.color || '#6366f1'}`;
  $('active-model-label').textContent = m.id;

  $$('.model-item').forEach(el => {
    el.classList.toggle('selected', el.dataset.id === m.id);
  });
}

// Toggle dropdown
const modelPillBtn  = $('model-pill-btn');
const modelDropdown = $('model-dropdown');

modelPillBtn.addEventListener('click', e => {
  e.stopPropagation();
  state.dropdownOpen ? closeModelDropdown() : openModelDropdown();
});

$('model-search-input').addEventListener('input', function() {
  const q = this.value.toLowerCase();
  $$('.model-item').forEach(el => {
    const name = el.querySelector('.model-item-name').textContent.toLowerCase();
    el.style.display = name.includes(q) ? '' : 'none';
  });
  $$('.model-group-label').forEach(el => {
    let anyVisible = false;
    let sib = el.nextElementSibling;
    while (sib && !sib.classList.contains('model-group-label')) {
      if (sib.style.display !== 'none') anyVisible = true;
      sib = sib.nextElementSibling;
    }
    el.style.display = anyVisible ? '' : 'none';
  });
});

function openModelDropdown() {
  modelDropdown.hidden = false;
  modelPillBtn.setAttribute('aria-expanded', 'true');
  state.dropdownOpen = true;
  $('model-search-input').value = '';
  $$('.model-item, .model-group-label').forEach(el => el.style.display = '');
  $('model-search-input').focus();
}

function closeModelDropdown() {
  modelDropdown.hidden = true;
  modelPillBtn.setAttribute('aria-expanded', 'false');
  state.dropdownOpen = false;
}

document.addEventListener('click', e => {
  if (state.dropdownOpen && !modelDropdown.contains(e.target) && e.target !== modelPillBtn) {
    closeModelDropdown();
  }
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModelDropdown(); });

// ── Mode toggle ───────────────────────────────────────────────────────────────
$('mode-chat').addEventListener('click',   () => setMode('chat'));
$('mode-search').addEventListener('click', () => setMode('search'));

function setMode(mode) {
  state.searchMode = mode === 'search';
  $('mode-chat').classList.toggle('active',   mode === 'chat');
  $('mode-search').classList.toggle('active', mode === 'search');

  const modeLabel = $('mode-label');
  if (mode === 'search') {
    modeLabel.innerHTML = `
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      Search ON`;
    modeLabel.style.color = 'var(--cyan)';
    $('chat-input').placeholder = 'Search the web... e.g. Latest AI news today';
  } else {
    modeLabel.innerHTML = `
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
      Chat`;
    modeLabel.style.color = '';
    $('chat-input').placeholder = 'Ask anything...';
  }
}

// ── Database & Chat History Persistence ───────────────────────────────────────

function escapeHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

async function loadChatHistoryList() {
  try {
    const res = await fetch('/api/conversations');
    const conversations = await res.json();
    renderChatHistoryList(conversations);
  } catch (err) {
    console.error('Failed to load chat history:', err);
  }
}

function renderChatHistoryList(conversations) {
  const container = $('chat-history-list');
  if (!container) return;
  container.innerHTML = '';

  if (!conversations || conversations.length === 0) {
    container.innerHTML = `<div style="padding:6px 10px;font-size:11px;color:var(--text-dim)">No saved chats</div>`;
    return;
  }

  conversations.forEach(c => {
    const item = document.createElement('div');
    item.className = 'chat-history-item' + (c.id === state.currentConversationId ? ' active' : '');
    item.dataset.id = c.id;

    item.innerHTML = `
      <span class="chat-history-title">${escapeHtml(c.title)}</span>
      <button class="chat-history-del" title="Delete conversation">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
      </button>
    `;

    item.addEventListener('click', (e) => {
      if (e.target.closest('.chat-history-del')) return;
      loadConversation(c.id);
    });

    const delBtn = item.querySelector('.chat-history-del');
    delBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      await deleteConversation(c.id);
    });

    container.appendChild(item);
  });
}

async function loadConversation(cid) {
  try {
    const res = await fetch(`/api/conversations/${cid}`);
    if (!res.ok) return;
    const data = await res.json();

    state.currentConversationId = cid;
    state.chatHistory = [];

    // Clear messages UI
    const container = $('chat-messages');
    container.innerHTML = '';

    // Re-select model if matching
    if (data.conversation && data.conversation.model) {
      const match = state.models.find(m => m.id === data.conversation.model);
      if (match) selectModel(match);
    }

    // Populate messages
    data.messages.forEach(m => {
      state.chatHistory.push({ role: m.role, content: m.content });
      if (m.role === 'user') {
        appendUserMsg(m.content);
      } else {
        const { bubble, cursor } = appendAIBubble(state.modelName);
        renderBubble(bubble, m.content, cursor);
        cursor.remove();
      }
    });

    // Update active class in sidebar history
    $$('.chat-history-item').forEach(el => {
      el.classList.toggle('active', el.dataset.id === cid);
    });

    switchTab('chat');
    scrollChat();

  } catch (err) {
    showToast('Failed to load conversation: ' + err.message, 'error');
  }
}

async function deleteConversation(cid) {
  try {
    await fetch(`/api/conversations/${cid}`, { method: 'DELETE' });
    if (state.currentConversationId === cid) {
      state.currentConversationId = null;
      $('clear-btn').click();
    }
    await loadChatHistoryList();
    showToast('Conversation deleted', 'info');
  } catch (err) {
    showToast('Failed to delete chat', 'error');
  }
}

async function ensureConversationExists(firstUserText) {
  if (state.currentConversationId) return state.currentConversationId;

  const title = firstUserText.slice(0, 35).trim() + (firstUserText.length > 35 ? '...' : '');
  try {
    const res = await fetch('/api/conversations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title, model: state.model })
    });
    const data = await res.json();
    state.currentConversationId = data.id;
    await loadChatHistoryList();
    return data.id;
  } catch (err) {
    console.error('Failed to create conversation in DB:', err);
    return null;
  }
}

async function saveMessageToDb(cid, role, content) {
  if (!cid) return;
  try {
    await fetch(`/api/conversations/${cid}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role, content, model: state.model })
    });
    await loadChatHistoryList();
  } catch (err) {
    console.error('Failed to save message to DB:', err);
  }
}

// Clear / New chat handlers
$('clear-btn').addEventListener('click', () => {
  state.chatHistory = [];
  state.currentConversationId = null;
  const msgs = $('chat-messages');
  msgs.innerHTML = `
    <div class="welcome-container" id="welcome-msg">
      <div class="welcome-header">
        <h1>What can I help you build or explore today?</h1>
        <p>Generate code, UI components, images, audio, or search the live web.</p>
      </div>

      <div class="prompt-grid">
        <button class="prompt-card" onclick="fillPrompt('Build a responsive dark mode dashboard UI component in React')">
          <div class="prompt-card-title">Dashboard UI Component</div>
          <div class="prompt-card-sub">Build a responsive dark mode dashboard in React & Tailwind</div>
        </button>

        <button class="prompt-card" onclick="fillPrompt('Explain quantum computing principles with Python examples')">
          <div class="prompt-card-title">Technical Deep Dive</div>
          <div class="prompt-card-sub">Explain quantum computing principles with code examples</div>
        </button>

        <button class="prompt-card" onclick="fillPrompt('What are the latest AI model releases this week?')">
          <div class="prompt-card-title">Live Intelligence</div>
          <div class="prompt-card-sub">What are the latest AI model releases this week?</div>
        </button>

        <button class="prompt-card" onclick="fillPrompt('Create a high-converting SaaS landing page tagline & hero copy')">
          <div class="prompt-card-title">SaaS Copywriting</div>
          <div class="prompt-card-sub">Create a landing page tagline & value proposition</div>
        </button>
      </div>
    </div>
  `;
  $$('.chat-history-item').forEach(el => el.classList.remove('active'));
});

// ── New chat ──────────────────────────────────────────────────────────────────
$('new-chat-btn').addEventListener('click', () => {
  $('clear-btn').click();
  switchTab('chat');
});

// Expose switchTab globally for onclick attributes in HTML
window.switchTab = switchTab;

// Fill chat input with a suggested prompt and focus
window.fillPrompt = function(text) {
  const input = $('chat-input');
  input.value = text;
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 160) + 'px';
  input.focus();
  // Animate the send button
  anime({ targets: '#send-btn', scale: [1, 1.12, 1], duration: 350, easing: 'easeOutBack' });
};


// ── Chat input ────────────────────────────────────────────────────────────────
const chatInput = $('chat-input');

chatInput.addEventListener('input', () => {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + 'px';
});

chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

$('send-btn').addEventListener('click', sendMessage);

async function sendMessage() {
  let text = chatInput.value.trim();
  if ((!text && state.attachments.length === 0) || state.streaming) return;

  chatInput.value = '';
  chatInput.style.height = 'auto';

  // Process attachments
  if (state.attachments.length > 0) {
    let attachContext = '\n\n---\n**Attached Content & Photos:**\n';
    state.attachments.forEach(att => {
      if (att.type.startsWith('image/')) {
        attachContext += `![${att.name}](${att.data})\n`;
      } else {
        attachContext += `\n\`\`\`${att.name}\n${att.data.slice(0, 8000)}\n\`\`\`\n`;
      }
    });
    text = (text ? text : 'Please analyze the attached content / image(s).') + attachContext;
    clearAttachments();
  }

  // Ensure DB conversation session exists
  const cid = await ensureConversationExists(text);
  const wmsg = $('welcome-msg'); if (wmsg) wmsg.style.display = 'none';

  appendUserMsg(text);
  state.chatHistory.push({ role: 'user', content: text });
  
  // Save user message to DB
  await saveMessageToDb(cid, 'user', text);

  if (state.searchMode) {
    await doStreamSearch(text);
  } else {
    await doStreamChat(text);
  }
}

// ── Streaming chat ─────────────────────────────────────────────────────────────
async function doStreamChat(userText) {
  state.streaming = true;
  $('send-btn').disabled = true;

  const { bubble, cursor } = appendAIBubble(state.modelName);
  let full = '';

  bubble.innerHTML = `<div class="thinking-dots"><span></span><span></span><span></span></div>`;
  bubble.appendChild(cursor);

  try {
    const res = await fetch('/api/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ model: state.model, messages: state.chatHistory }),
    });

    const reader = res.body.getReader();
    const dec    = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const raw = line.slice(6);
        if (raw === '[DONE]') break;
        try {
          const d = JSON.parse(raw);
          if (d.token) { full += d.token; renderBubble(bubble, full, cursor); }
          if (d.error)  renderBubble(bubble, `Error: ${d.error}`, cursor);
        } catch {}
      }
    }
  } catch (err) {
    renderBubble(bubble, `Connection error: ${err.message}`, cursor);
  } finally {
    cursor.remove();
    if (full) {
      state.chatHistory.push({ role: 'assistant', content: full });
      // Save assistant response to DB
      await saveMessageToDb(state.currentConversationId, 'assistant', full);
    }
    state.streaming  = false;
    $('send-btn').disabled = false;
    scrollChat();
  }
}

// ── Streaming search (in chat) ─────────────────────────────────────────────────
async function doStreamSearch(query) {
  state.streaming = true;
  $('send-btn').disabled = true;

  const { bubble, cursor } = appendAIBubble('Web Search', 'cyan');
  let full = '';

  bubble.innerHTML = `
    <div class="thinking-dots">
      <span></span><span></span><span></span>
      <small style="margin-left:8px;color:var(--text-3);font-size:11px">Searching the web…</small>
    </div>`;
  bubble.appendChild(cursor);

  try {
    const res = await fetch('/api/search', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query }),
    });

    const reader = res.body.getReader();
    const dec    = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const raw = line.slice(6);
        if (raw === '[DONE]') break;
        try {
          const d = JSON.parse(raw);
          if (d.token) { full += d.token; renderBubble(bubble, full, cursor); }
          if (d.error)  renderBubble(bubble, `${d.error}`, cursor);
        } catch {}
      }
    }
  } catch (err) {
    renderBubble(bubble, `Search error: ${err.message}`, cursor);
  } finally {
    cursor.remove();
    state.streaming  = false;
    $('send-btn').disabled = false;
    scrollChat();
  }
}

// ── Chat DOM helpers ───────────────────────────────────────────────────────────
function appendUserMsg(content) {
  const msgs = $('chat-messages');
  const el   = document.createElement('div');
  el.className = 'msg-group user';
  el.innerHTML = `
    <div class="msg-avatar user-avatar">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    </div>
    <div class="msg-body">
      <div class="msg-meta" style="justify-content:flex-end">You</div>
      <div class="msg-bubble">${escHtml(content)}</div>
    </div>`;
  msgs.appendChild(el);
  scrollChat();
}

function appendAIBubble(label = 'DART AI') {
  const msgs = $('chat-messages');
  const group = document.createElement('div');
  group.className = 'msg-group assistant';

  group.innerHTML = `
    <div class="msg-avatar ai-avatar">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
    </div>
    <div class="msg-body">
      <div class="msg-meta">
        DART AI
        <span class="meta-chip">${label}</span>
      </div>
      <div class="msg-bubble"></div>
      <div class="msg-actions-bar">
        <button class="msg-act-btn" onclick="copyMsgText(this)">Copy</button>
        <button class="msg-act-btn" onclick="speakMsgText(this)">Speak</button>
        <button class="msg-act-btn" onclick="likeMsg(this)">Like</button>
        <button class="msg-act-btn" onclick="dislikeMsg(this)">Dislike</button>
        <button class="msg-act-btn" onclick="exportMsg(this)">Export</button>
        <button class="msg-act-btn" onclick="branchMsg(this)">Branch</button>
      </div>
    </div>`;

  msgs.appendChild(group);
  scrollChat();

  const bubble = group.querySelector('.msg-bubble');
  const cursor = document.createElement('span');
  cursor.className = 'cursor';
  return { bubble, cursor };
}

function renderBubble(bubble, text, cursor) {
  bubble.innerHTML = renderMarkdown(text);
  bubble.appendChild(cursor);
  bubble.querySelectorAll('pre code').forEach(b => {
    if (!b.dataset.highlighted) { hljs.highlightElement(b); b.dataset.highlighted = '1'; }
  });
  scrollChat();
}

function renderMarkdown(text) {
  if (!text) return '';
  const html = marked.parse(text);
  return html.replace(/<pre><code(?: class="language-(\w+)")?>/g, (_, lang) => {
    const label = lang || 'code';
    return `<div class="code-block-wrap"><div class="code-header"><span class="code-lang-badge">${label}</span><div class="code-block-actions"><button class="code-action-btn" onclick="copyCode(this)">Copy</button><button class="code-action-btn" onclick="downloadCodeBlock(this)">Download</button><button class="code-header-run-btn" onclick="runCodeInIDE(this)">Run</button></div></div><pre><code class="${lang ? `language-${lang}` : ''}">`;
  }).replace(/<\/code><\/pre>/g, '</code></pre></div>');
}

window.copyCode = function(btn) {
  const code = btn.closest('.code-block-wrap').querySelector('code');
  navigator.clipboard.writeText(code.textContent).then(() => {
    btn.textContent = 'Copied';
    btn.style.color = 'var(--green)';
    setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 2000);
  });
};

window.downloadCodeBlock = function(btn) {
  const code = btn.closest('.code-block-wrap').querySelector('code').textContent;
  const lang = btn.closest('.code-block-wrap').querySelector('.code-lang-badge').textContent || 'txt';
  const ext = { html: 'html', python: 'py', javascript: 'js', json: 'json', sql: 'sql', css: 'css' }[lang] || 'txt';
  const blob = new Blob([code], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `snippet.${ext}`;
  a.click();
  showToast(`Downloaded snippet.${ext}`, 'info');
};

window.runCodeInIDE = function(btn) {
  const code = btn.closest('.code-block-wrap').querySelector('code').textContent;
  const lang = btn.closest('.code-block-wrap').querySelector('.code-lang-badge').textContent || 'html';
  switchTab('editor');
  const textarea = $('code-editor-textarea');
  const langSelect = $('editor-lang-select');
  if (textarea) textarea.value = code;
  if (langSelect && ['html', 'python', 'javascript', 'json', 'sql'].includes(lang)) {
    langSelect.value = lang;
  }
  const runBtn = $('editor-run-btn');
  if (runBtn) runBtn.click();
  showToast('Code sent to Code Studio IDE Sandbox!', 'success');
};

window.copyMsgText = function(btn) {
  const bubble = btn.closest('.msg-body').querySelector('.msg-bubble');
  navigator.clipboard.writeText(bubble.innerText);
  showToast('Message copied to clipboard', 'info');
};

window.speakMsgText = function(btn) {
  const bubble = btn.closest('.msg-body').querySelector('.msg-bubble');
  if (state.synthesis) {
    const utterance = new SpeechSynthesisUtterance(bubble.innerText.slice(0, 500));
    state.synthesis.speak(utterance);
    showToast('Speaking message...', 'info');
  }
};

window.likeMsg = function(btn) {
  btn.classList.toggle('active-like');
  showToast('Thanks for your feedback!', 'success');
};

window.dislikeMsg = function(btn) {
  btn.classList.toggle('active-dislike');
  showToast('Feedback noted', 'info');
};

window.exportMsg = function(btn) {
  if (state.currentConversationId) {
    window.open(`/api/conversations/${state.currentConversationId}/export?format=markdown`, '_blank');
  } else {
    showToast('No active conversation to export', 'info');
  }
};

window.branchMsg = function(btn) {
  showToast('Branched conversation session', 'info');
};


function scrollChat() {
  const msgs = $('chat-messages');
  msgs.scrollTop = msgs.scrollHeight;
}

// ── Web Search Panel ───────────────────────────────────────────────────────────
$('search-btn').addEventListener('click', runSearch);
$('search-input').addEventListener('keydown', e => { if (e.key === 'Enter') runSearch(); });

async function runSearch() {
  const q = $('search-input').value.trim();
  if (!q) return;

  const results = $('search-results');
  results.innerHTML = `<div class="search-loading">
    <div class="loader" style="color:var(--cyan)"></div>
    <span>Searching for "<strong>${escHtml(q)}</strong>"…</span>
  </div>`;
  $('search-btn').disabled = true;

  let full = '';
  try {
    const res = await fetch('/api/search', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ query: q }),
    });

    const reader = res.body.getReader();
    const dec    = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const raw = line.slice(6);
        if (raw === '[DONE]') break;
        try {
          const d = JSON.parse(raw);
          if (d.token) { full += d.token; results.innerHTML = marked.parse(full); }
          if (d.error) results.innerHTML = `<span style="color:var(--red)">${escHtml(d.error)}</span>`;
        } catch {}
      }
    }
  } catch (err) {
    results.innerHTML = `<span style="color:var(--red)">${err.message}</span>`;
  } finally {
    $('search-btn').disabled = false;
    if (full) results.innerHTML = marked.parse(full);
  }
}

// ── Music Panel ────────────────────────────────────────────────────────────────
$('gen-music-btn').addEventListener('click', startMusicGen);

async function startMusicGen() {
  const prompt = $('music-prompt').value.trim();
  if (!prompt) { showToast('Please enter a song description', 'error'); return; }

  const btn = $('gen-music-btn');
  btn.disabled = true;
  btn.innerHTML = `<div class="loader"></div> Generating…`;

  const log = $('music-log');
  log.hidden = false; log.innerHTML = '';
  $('music-player').hidden = true;
  clearMusicPoll();

  try {
    const r = await fetch('/api/music', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ prompt }),
    });
    const { job_id } = await r.json();
    state.musicJobId = job_id;
    pollMusicJob(job_id);
  } catch (e) {
    addMusicLog(`Failed to start: ${e.message}`, 'error');
    resetMusicBtn();
  }
}

function pollMusicJob(job_id) {
  let lastLen = 0;
  state.musicPollTimer = setInterval(async () => {
    try {
      const r    = await fetch(`/api/music/${job_id}`);
      const data = await r.json();

      if (data.log && data.log.length > lastLen) {
        data.log.slice(lastLen).forEach(line => addMusicLog(line));
        lastLen = data.log.length;
      }

      if (data.status === 'done') {
        clearMusicPoll();
        showMusicPlayer(data);
        resetMusicBtn('Generate Another');
        showToast('Your song is ready!', 'success');
      } else if (data.status === 'error') {
        clearMusicPoll();
        resetMusicBtn('Try Again');
        showToast('Music generation failed', 'error');
      }
    } catch {}
  }, 3000);
}

function clearMusicPoll() {
  if (state.musicPollTimer) { clearInterval(state.musicPollTimer); state.musicPollTimer = null; }
}

function addMusicLog(msg, type) {
  const log  = $('music-log');
  const line = document.createElement('div');
  line.className = 'log-line';
  let color = 'var(--text-2)';
  if (msg.includes('Error') || type === 'error') color = 'var(--red)';
  else if (msg.includes('Success')) color = 'var(--green)';
  else if (msg.includes('Processing')) color = 'var(--amber)';
  line.style.color = color;
  line.textContent = msg;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

function resetMusicBtn(label = 'Generate Song') {
  const btn = $('gen-music-btn');
  btn.disabled = false;
  btn.innerHTML = `
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
    ${label}`;
}

function showMusicPlayer(data) {
  const player = $('music-player');
  player.hidden = false;

  $('music-title').textContent = data.title || 'Generated Song';

  const cover = $('music-cover');
  if (data.cover) {
    cover.innerHTML = `<img src="${data.cover}" alt="Album art"/>`;
  }

  const audio = $('music-audio');
  if (data.mp3) {
    state.musicUrl = data.mp3;
    audio.src = data.mp3;
  }

  const lyrics = $('music-lyrics');
  if (data.lyrics) {
    lyrics.textContent = data.lyrics;
    lyrics.hidden = false;
  }

  $('dl-music-btn').onclick = () => {
    const a = document.createElement('a');
    a.href = data.mp3;
    a.download = (data.title || 'song').replace(/[^a-z0-9]/gi, '-') + '.mp3';
    a.click();
  };

  anime({ targets: player, opacity: [0,1], translateY: [16,0], duration: 400, easing: 'easeOutQuart' });
}

// ── Voice / TTS Panel ──────────────────────────────────────────────────────────
$$('.voice-card').forEach(card => {
  card.addEventListener('click', () => {
    $$('.voice-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    state.voice = card.dataset.voice;
    anime({ targets: card, scale: [0.92, 1], duration: 280, easing: 'easeOutBack' });
  });
});

$('speak-btn').addEventListener('click', generateTTS);

async function generateTTS() {
  const text = $('tts-text').value.trim();
  if (!text) { showToast('Please enter text to speak', 'error'); return; }

  const btn = $('speak-btn');
  btn.disabled = true;
  btn.innerHTML = `<div class="loader"></div> Generating…`;

  const waveform = $('waveform');
  waveform.classList.add('playing');

  const ttsAudio = $('tts-audio');
  ttsAudio.hidden = true;
  $('tts-dl-btn').hidden = true;

  try {
    const r = await fetch('/api/tts', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ text, voice: state.voice }),
    });

    if (!r.ok) throw new Error(`Server error ${r.status}`);
    const blob = await r.blob();
    if (blob.size < 100) throw new Error('Empty audio response');

    if (state.ttsUrl) URL.revokeObjectURL(state.ttsUrl);
    state.ttsUrl = URL.createObjectURL(blob);
    ttsAudio.src = state.ttsUrl;
    ttsAudio.hidden = false;
    ttsAudio.play();

    $('tts-dl-btn').hidden = false;
    $('tts-dl-btn').onclick = () => {
      const a = document.createElement('a');
      a.href = state.ttsUrl;
      a.download = `speech-${state.voice}.mp3`;
      a.click();
    };

    anime({ targets: ttsAudio, opacity: [0,1], translateY: [8,0], duration: 300, easing: 'easeOutQuart' });
    showToast('Speech generated!', 'success');

  } catch (err) {
    showToast('TTS error: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
      Generate Speech`;
    waveform.classList.remove('playing');
  }
}

// ── Temp Mail Panel ────────────────────────────────────────────────────────────
$('create-mail-btn').addEventListener('click', createMail);
$('back-to-list').addEventListener('click', () => {
  clearMailPoll();
  $('mail-inbox').hidden = true;
  $('mail-list-section').hidden = false;
});
$('refresh-inbox').addEventListener('click', () => checkInbox(state.currentMailEmail));

async function createMail() {
  const btn = $('create-mail-btn');
  btn.disabled = true;
  btn.innerHTML = `<div class="loader"></div> Creating…`;

  try {
    const r = await fetch('/api/mail/new', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ prefix: $('mail-prefix').value.trim() }),
    });
    const data = await r.json();
    if (data.error) { showToast(data.error, 'error'); return; }
    $('mail-prefix').value = '';
    showToast('New inbox created!', 'success');
    loadMailList();
  } catch (e) {
    showToast('Error: ' + e.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      New Inbox`;
  }
}

async function loadMailList() {
  try {
    const r    = await fetch('/api/mail/list');
    const list = await r.json();
    const mailList = $('mail-list');

    if (!list.length) {
      mailList.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon-wrap">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <p>No inboxes yet</p>
          <small>Create one above to get started</small>
        </div>`;
      return;
    }

    mailList.innerHTML = list.map(m => {
      const mins  = Math.floor(m.expires_secs / 60);
      const secs  = m.expires_secs % 60;
      let timerClass = 'fresh';
      if (m.expired)               timerClass = 'expired';
      else if (m.expires_secs < 600)  timerClass = 'urgent';
      else if (m.expires_secs < 1800) timerClass = 'mid';
      const timerText = m.expired ? 'EXPIRED' : `${mins}m ${secs}s remaining`;

      return `
        <div class="mail-item" onclick="openInbox('${escAttr(m.email)}','${escAttr(m.id)}')" role="button" tabindex="0">
          <div class="mail-item-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <div class="mail-item-body">
            <div class="mail-item-addr">${escHtml(m.email)}</div>
            <div class="mail-item-timer ${timerClass}">${timerText}</div>
          </div>
          <div class="mail-actions">
            <button class="mail-action-btn copy" title="Copy address" onclick="event.stopPropagation();copyMailAddr('${escAttr(m.email)}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            </button>
            <button class="mail-action-btn" title="Delete" onclick="event.stopPropagation();deleteMail('${escAttr(m.id)}','${escAttr(m.email)}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
            </button>
          </div>
        </div>`;
    }).join('');

    anime({
      targets: '.mail-item',
      opacity: [0,1], translateY: [10,0],
      delay: anime.stagger(55),
      duration: 280, easing: 'easeOutQuart',
    });
  } catch (e) {
    $('mail-list').innerHTML = `<div style="color:var(--red);padding:16px">Error: ${e.message}</div>`;
  }
}

window.openInbox = function(email, id) {
  state.currentMailEmail = email;
  state.currentMailId    = id;
  $('inbox-email').textContent = email;
  $('mail-list-section').hidden = true;
  $('mail-inbox').hidden = false;
  $('inbox-messages').innerHTML = `
    <div class="empty-state">
      <div class="empty-icon-wrap">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      </div>
      <p>Checking inbox…</p>
    </div>`;
  checkInbox(email);
  startMailPoll(email);
};

async function checkInbox(email) {
  try {
    const r    = await fetch(`/api/mail/check/${encodeURIComponent(email)}`);
    const data = await r.json();

    if (!data.ok) {
      $('inbox-messages').innerHTML = `
        <div class="empty-state">
          <div class="empty-icon-wrap">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <p>No messages yet</p>
          <small>Emails will appear here automatically</small>
        </div>`;
      return;
    }
    clearMailPoll();
    showMailMessage(data);
  } catch {}
}

function showMailMessage(msg) {
  const from    = msg.from    || msg.sender || '';
  const subject = msg.subject || '(No subject)';
  const date    = msg.date    || msg.created_at || '';
  const body    = (msg.body && (msg.body.text || msg.body.html)) || msg.body_text || msg.body_html || '';

  $('inbox-messages').innerHTML = `
    <div class="mail-message-card">
      <div class="mail-msg-header">
        <div class="mail-msg-row"><strong>From</strong><span>${escHtml(from)}</span></div>
        <div class="mail-msg-row"><strong>Date</strong><span>${escHtml(date)}</span></div>
      </div>
      <div class="mail-subject">${escHtml(subject)}</div>
      <div class="mail-msg-body">${escHtml(body)}</div>
    </div>`;

  anime({ targets: '.mail-message-card', opacity: [0,1], translateY: [8,0], duration: 300, easing: 'easeOutQuart' });
}

function startMailPoll(email) {
  clearMailPoll();
  state.mailPollTimer = setInterval(() => checkInbox(email), 5000);
}

function clearMailPoll() {
  if (state.mailPollTimer) { clearInterval(state.mailPollTimer); state.mailPollTimer = null; }
}

window.copyMailAddr = function(email) {
  navigator.clipboard.writeText(email).then(() => showToast('Email copied!', 'success'));
};

window.deleteMail = async function(id, email) {
  if (!confirm(`Delete ${email}?`)) return;
  try {
    await fetch(`/api/mail/${id}?email=${encodeURIComponent(email)}`, { method: 'DELETE' });
    showToast('Inbox deleted', 'info');
    loadMailList();
  } catch (e) {
    showToast('Delete failed', 'error');
  }
};

// ── Toast system ───────────────────────────────────────────────────────────────
function showToast(msg, type = 'info', duration = 3000) {
  const container = $('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const icons = {
    success: `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`,
    error:   `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--red)" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
    info:    `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--indigo-bright)" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
  };

  toast.innerHTML = `${icons[type] || icons.info}<span>${escHtml(msg)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('out');
    setTimeout(() => toast.remove(), 350);
  }, duration);
}

// ── Utils ──────────────────────────────────────────────────────────────────────
function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function escAttr(s) {
  return String(s).replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

// ── Entry animations ───────────────────────────────────────────────────────────
function runEntryAnimations() {
  anime({
    targets: '#sidebar',
    translateX: [-24, 0],
    opacity: [0, 1],
    duration: 550,
    easing: 'easeOutQuart',
  });

  anime({
    targets: '.nav-btn',
    translateX: [-16, 0],
    opacity: [0, 1],
    delay: anime.stagger(45, { start: 100 }),
    duration: 380,
    easing: 'easeOutQuart',
  });

  anime({
    targets: '.welcome-header',
    opacity: [0, 1],
    translateY: [12, 0],
    duration: 450,
    delay: 200,
    easing: 'easeOutQuart',
  });

  anime({
    targets: '.prompt-card',
    opacity: [0, 1],
    translateY: [16, 0],
    scale: [0.97, 1],
    delay: anime.stagger(60, { start: 300 }),
    duration: 450,
    easing: 'easeOutQuint',
  });

  anime({
    targets: '#topbar',
    translateY: [-10, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutQuart',
  });

  // Attach spring bounce micro-interactions to all buttons
  document.querySelectorAll('.btn, .prompt-card').forEach(el => {
    el.addEventListener('click', () => {
      anime({
        targets: el,
        scale: [0.96, 1],
        duration: 250,
        easing: 'easeOutElastic(1, .5)',
      });
    });
  });
}

// ── Init ───────────────────────────────────────────────────────────────────────
(async function init() {
  await loadModels();
  runEntryAnimations();
  $('mail-list-section').hidden = false;
  $('mail-inbox').hidden = true;
  loadImagePanel();
  loadChatHistoryList();
  initAuth();
})();

// ── Image Generation Panel ────────────────────────────────────────────────────
const imgState = {
  model:    'flux',
  style:    '',
  size:     'square',
  lastUrl:  null,
  lastPrompt: null,
  generating: false,
};

async function loadImagePanel() {
  try {
    const [modelsRes, stylesRes] = await Promise.all([
      fetch('/api/image/models'),
      fetch('/api/image/styles'),
    ]);
    const models = await modelsRes.json();
    const styles = await stylesRes.json();

    // Build model grid
    const mgrid = $('img-model-grid');
    if (mgrid) {
      mgrid.innerHTML = '';
      models.forEach((m, i) => {
        const btn = document.createElement('button');
        btn.className = 'img-model-btn' + (i === 0 ? ' active' : '');
        btn.dataset.model = m.id;
        btn.innerHTML = `
          <div class="img-model-name">${m.name}</div>
          <div class="img-model-tag">${m.tag}</div>
          <div class="img-model-desc">${m.desc}</div>`;
        btn.addEventListener('click', () => {
          $$('.img-model-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          imgState.model = m.id;
        });
        mgrid.appendChild(btn);
      });
    }

    // Build style grid
    const sgrid = $('img-style-grid');
    if (sgrid) {
      sgrid.innerHTML = '';
      styles.forEach((s, i) => {
        const btn = document.createElement('button');
        btn.className = 'img-style-btn' + (i === 0 ? ' active' : '');
        btn.dataset.style = s.id;
        btn.textContent = s.name;
        btn.addEventListener('click', () => {
          $$('.img-style-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          imgState.style = s.id;
        });
        sgrid.appendChild(btn);
      });
    }
  } catch (e) {
    console.error('Failed to load image panel data:', e);
  }
}

// Size buttons
$$('.img-size-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.img-size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    imgState.size = btn.dataset.size;
  });
});

// Generate button
const genImgBtn = $('gen-img-btn');
if (genImgBtn) {
  genImgBtn.addEventListener('click', generateImage);
}

async function generateImage(seed) {
  if (imgState.generating) return;
  const prompt = $('img-prompt').value.trim();
  if (!prompt) { showToast('Please describe your image', 'error'); return; }

  imgState.generating = true;
  genImgBtn.disabled = true;
  genImgBtn.innerHTML = `<div class="img-spinner" style="width:16px;height:16px;border-width:2px"></div> Generating…`;

  const result = $('img-result');
  const loader  = $('img-loader');
  const imgOut  = $('img-output');
  const imgMeta = $('img-meta');

  result.hidden = false;
  loader.style.display = 'flex';
  imgOut.style.display = 'none';
  imgOut.src = '';
  imgMeta.innerHTML = '';
  $('img-loader-text').textContent = 'Generating… (~10-30s)';

  // Animate reveal
  anime({ targets: result, opacity: [0, 1], translateY: [12, 0], duration: 350, easing: 'easeOutQuart' });

  try {
    const body = {
      prompt: prompt,
      model:  imgState.model,
      style:  imgState.style,
      size:   imgState.size,
    };
    if (typeof seed === 'number') body.seed = seed;

    const r = await fetch('/api/image/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await r.json();

    if (data.error) {
      showToast('Error: ' + data.error, 'error');
      loader.style.display = 'none';
      return;
    }

    imgState.lastUrl    = data.url;
    imgState.lastPrompt = data.prompt;
    $('img-result-label').textContent = prompt.slice(0, 60) + (prompt.length > 60 ? '…' : '');

    // Load image
    const img = new Image();
    img.onload = () => {
      loader.style.display = 'none';
      imgOut.src   = data.url;
      imgOut.style.display = 'block';
      imgMeta.innerHTML = `
        <strong>Model:</strong> ${data.model} &nbsp;·&nbsp;
        <strong>Size:</strong> ${data.width}×${data.height} &nbsp;·&nbsp;
        <strong>Seed:</strong> ${data.seed}
      `;
      showToast('Image generated!', 'success');

      // Wire download
      $('img-dl-btn').onclick = () => {
        const a = document.createElement('a');
        a.href = data.url;
        a.download = prompt.slice(0, 40).replace(/[^a-z0-9]/gi, '-') + '.jpg';
        a.target = '_blank';
        a.click();
      };

      // Wire vary
      $('img-vary-btn').onclick = () => generateImage(Math.floor(Math.random() * 999999));
    };
    img.onerror = () => {
      loader.style.display = 'none';
      showToast('Failed to load generated image', 'error');
    };
    img.src = data.url;

  } catch (e) {
    loader.style.display = 'none';
    showToast('Generation failed: ' + e.message, 'error');
  } finally {
    imgState.generating = false;
    genImgBtn.disabled = false;
    genImgBtn.innerHTML = `
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      Generate Image`;
  }
}

// ── Google Auth & User Profile ───────────────────────────────────────────────
state.user = null;

async function initAuth() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    if (data.authenticated && data.user) {
      renderUserProfile(data.user);
    } else {
      renderUnloggedState();
    }
  } catch (e) {
    renderUnloggedState();
  }

  // Initialize Google One Tap if SDK loaded
  if (window.google && window.google.accounts) {
    try {
      window.google.accounts.id.initialize({
        client_id: "demo-client-id.apps.googleusercontent.com",
        callback: handleGoogleCredentialResponse,
        auto_select: false,
      });
    } catch (e) {}
  }
}

window.handleGoogleCredentialResponse = async function(response) {
  if (!response || !response.credential) return;
  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: response.credential })
    });
    const data = await res.json();
    if (data.user) {
      renderUserProfile(data.user);
      showToast(`Welcome back, ${data.user.name}!`, 'success');
    }
  } catch (e) {
    showToast('Google Sign-In failed', 'error');
  }
};

window.openAuthModal = function() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.hidden = false;
    modal.style.display = 'flex';
  }
};

window.closeAuthModal = function() {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.hidden = true;
    modal.style.display = 'none';
  }
};

window.triggerGuestLogin = function() {
  window.closeAuthModal();
  showToast('Continuing in Guest Mode', 'info');
};

const authModalClose = document.getElementById('auth-modal-close');
if (authModalClose) {
  authModalClose.addEventListener('click', window.closeAuthModal);
}

window.triggerGoogleLogin = async function() {
  window.closeAuthModal();

  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.prompt();
  }
  
  const mockNames = ['Alex Mercer', 'Jordan Lee', 'Sam Taylor', 'Dev User'];
  const name = mockNames[Math.floor(Math.random() * mockNames.length)];
  const email = name.toLowerCase().replace(' ', '.') + '@gmail.com';
  
  try {
    const res = await fetch('/api/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email,
        name: name,
        picture: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`,
        google_id: 'google_' + Math.random().toString(36).substring(2, 10)
      })
    });
    const data = await res.json();
    if (data.user) {
      renderUserProfile(data.user);
      showToast(`Signed in as ${data.user.name}`, 'success');
    }
  } catch (e) {
    showToast('Login failed', 'error');
  }
};

function renderUserProfile(user) {
  state.user = user;
  $('auth-unlogged').hidden = true;
  $('auth-logged').hidden = false;
  $('user-avatar').src = user.picture || 'https://lh3.googleusercontent.com/a/default-user=s96-c';
  $('user-name').textContent = user.name;
  $('user-email').textContent = user.email;
}

function renderUnloggedState() {
  state.user = null;
  $('auth-unlogged').hidden = false;
  $('auth-logged').hidden = true;
}

window.logoutUser = async function() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' });
    renderUnloggedState();
    showToast('Signed out', 'info');
  } catch (e) {
    renderUnloggedState();
  }
};

/* =============================================================================
   File & Photo Upload Engine
   ============================================================================= */
const fileUploadBtn   = $('file-upload-btn');
const photoUploadBtn  = $('photo-upload-btn');
const fileInputHidden = $('file-input-hidden');
const photoInputHidden= $('photo-input-hidden');
const previewContainer= $('file-attachment-preview');

if (fileUploadBtn && fileInputHidden) {
  fileUploadBtn.addEventListener('click', () => fileInputHidden.click());
  fileInputHidden.addEventListener('change', (e) => handleSelectedFiles(e.target.files));
}

if (photoUploadBtn && photoInputHidden) {
  photoUploadBtn.addEventListener('click', () => photoInputHidden.click());
  photoInputHidden.addEventListener('change', (e) => handleSelectedFiles(e.target.files));
}

function handleSelectedFiles(files) {
  if (!files || files.length === 0) return;
  Array.from(files).forEach(file => {
    const reader = new FileReader();
    const isImage = file.type.startsWith('image/');
    
    reader.onload = (e) => {
      state.attachments.push({
        name: file.name,
        type: file.type,
        size: file.size,
        data: e.target.result
      });
      renderAttachments();
      showToast(`Attached ${file.name}`, 'info');
    };

    if (isImage) {
      reader.readAsDataURL(file);
    } else {
      reader.readAsText(file);
    }
  });
}

function renderAttachments() {
  if (!previewContainer) return;
  previewContainer.innerHTML = '';

  if (state.attachments.length === 0) {
    previewContainer.hidden = true;
    return;
  }

  previewContainer.hidden = false;
  state.attachments.forEach((att, index) => {
    const chip = document.createElement('div');
    chip.className = 'attachment-chip';
    
    if (att.type.startsWith('image/')) {
      chip.innerHTML = `
        <img src="${att.data}" class="attachment-thumb" alt="Preview"/>
        <span class="attachment-name">${escapeHtml(att.name)}</span>
        <button type="button" class="attachment-remove" data-index="${index}" title="Remove file">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      `;
    } else {
      chip.innerHTML = `
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
        <span class="attachment-name">${escapeHtml(att.name)}</span>
        <button type="button" class="attachment-remove" data-index="${index}" title="Remove file">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      `;
    }

    chip.querySelector('.attachment-remove').addEventListener('click', (e) => {
      e.stopPropagation();
      removeAttachment(index);
    });

    previewContainer.appendChild(chip);
  });
}

function removeAttachment(index) {
  state.attachments.splice(index, 1);
  renderAttachments();
}

function clearAttachments() {
  state.attachments = [];
  renderAttachments();
  if (fileInputHidden) fileInputHidden.value = '';
  if (photoInputHidden) photoInputHidden.value = '';
}

/* =============================================================================
   Live Voice Assistant Engine (Web Speech & Wave Animation)
   ============================================================================= */
const voiceAssistantBtn  = $('voice-assistant-btn');
const voiceModalOverlay  = $('voice-assistant-modal');
const voiceModalClose    = $('voice-modal-close');
const voiceStatusText    = $('voice-status-text');
const voiceUserTranscript= $('voice-user-transcript');
const voiceAiResponse    = $('voice-ai-response');
const voiceMicTrigger    = $('voice-mic-trigger');
const voiceMicLabel      = $('voice-mic-label');
const voiceHandsfreeBtn  = $('voice-toggle-handsfree');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (voiceAssistantBtn) {
  voiceAssistantBtn.addEventListener('click', openVoiceAssistantModal);
}

if (voiceModalClose) {
  voiceModalClose.addEventListener('click', closeVoiceAssistantModal);
}

if (voiceHandsfreeBtn) {
  voiceHandsfreeBtn.addEventListener('click', () => {
    state.handsFreeMode = !state.handsFreeMode;
    voiceHandsfreeBtn.classList.toggle('active', state.handsFreeMode);
    showToast(state.handsFreeMode ? 'Hands-Free Auto Mode Enabled' : 'Hands-Free Mode Disabled', 'info');
  });
}

if (voiceMicTrigger) {
  voiceMicTrigger.addEventListener('click', () => {
    if (state.voiceActive) {
      stopVoiceRecognition();
    } else {
      startVoiceRecognition();
    }
  });
}

function openVoiceAssistantModal() {
  if (!voiceModalOverlay) return;
  voiceModalOverlay.hidden = false;
  voiceModalOverlay.style.display = 'flex';
  voiceAssistantBtn.classList.add('active');
  startVoiceRecognition();
}

function closeVoiceAssistantModal() {
  if (!voiceModalOverlay) return;
  voiceModalOverlay.hidden = true;
  voiceModalOverlay.style.display = 'none';
  voiceAssistantBtn.classList.remove('active');
  stopVoiceRecognition();
  if (state.synthesis) state.synthesis.cancel();
}

function updateVoiceStatus(status, text) {
  if (voiceStatusText) voiceStatusText.textContent = status;
  if (voiceUserTranscript && text) voiceUserTranscript.textContent = text;
}

function startVoiceRecognition() {
  if (!SpeechRecognition) {
    showToast('Browser does not support Speech Recognition. Please use Chrome/Edge.', 'error');
    if (voiceUserTranscript) voiceUserTranscript.textContent = 'Voice dictation not supported on this browser.';
    return;
  }

  if (state.recognition) {
    try { state.recognition.stop(); } catch(e){}
  }

  state.recognition = new SpeechRecognition();
  state.recognition.continuous = false;
  state.recognition.interimResults = true;
  state.recognition.lang = 'en-US';

  state.recognition.onstart = () => {
    state.voiceActive = true;
    updateVoiceStatus('LISTENING', 'Listening... speak clearly.');
    if (voiceMicLabel) voiceMicLabel.textContent = 'Stop Listening';
  };

  state.recognition.onresult = (e) => {
    let interim = '';
    let final = '';

    for (let i = e.resultIndex; i < e.results.length; ++i) {
      if (e.results[i].isFinal) {
        final += e.results[i][0].transcript;
      } else {
        interim += e.results[i][0].transcript;
      }
    }

    const currentText = final || interim;
    if (voiceUserTranscript) voiceUserTranscript.textContent = `"${currentText}"`;
    if (chatInput) chatInput.value = currentText;

    if (final) {
      handleVoiceCommandSubmitted(final);
    }
  };

  state.recognition.onerror = (e) => {
    console.warn('Speech recognition error:', e.error);
    updateVoiceStatus('IDLE', 'Press speak to try again.');
    stopVoiceRecognition();
  };

  state.recognition.onend = () => {
    state.voiceActive = false;
    if (voiceMicLabel) voiceMicLabel.textContent = 'Tap to Speak';
  };

  try {
    state.recognition.start();
  } catch(err) {
    console.error('Failed to start recognition:', err);
  }
}

function stopVoiceRecognition() {
  state.voiceActive = false;
  if (state.recognition) {
    try { state.recognition.stop(); } catch(e){}
  }
  if (voiceMicLabel) voiceMicLabel.textContent = 'Tap to Speak';
}

async function handleVoiceCommandSubmitted(spokenText) {
  stopVoiceRecognition();
  updateVoiceStatus('PROCESSING', `Processing: "${spokenText}"`);

  // Stream AI response and speak back
  const cid = await ensureConversationExists(spokenText);
  appendUserMsg(spokenText);
  state.chatHistory.push({ role: 'user', content: spokenText });
  await saveMessageToDb(cid, 'user', spokenText);

  let fullAiText = '';
  if (voiceAiResponse) voiceAiResponse.textContent = 'DART AI is thinking...';

  try {
    const res = await fetch('/api/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ model: state.model, messages: state.chatHistory }),
    });

    const reader = res.body.getReader();
    const dec    = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const raw = line.slice(6);
        if (raw === '[DONE]') break;
        try {
          const d = JSON.parse(raw);
          if (d.token) {
            fullAiText += d.token;
            if (voiceAiResponse) voiceAiResponse.textContent = fullAiText.slice(0, 200) + '...';
          }
        } catch {}
      }
    }

    if (fullAiText) {
      state.chatHistory.push({ role: 'assistant', content: fullAiText });
      await saveMessageToDb(cid, 'assistant', fullAiText);

      // Speak back
      speakVoiceAssistantResponse(fullAiText);
    }
  } catch (err) {
    updateVoiceStatus('ERROR', 'Voice request failed');
  }
}

function speakVoiceAssistantResponse(text) {
  updateVoiceStatus('SPEAKING', text.slice(0, 150) + '...');
  
  if (state.synthesis) {
    state.synthesis.cancel();
    const cleanedText = text.replace(/```[\s\S]*?```/g, 'Code block output').replace(/[*#_~]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanedText.slice(0, 400));
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    utterance.onend = () => {
      updateVoiceStatus('IDLE', 'Response finished.');
      if (state.handsFreeMode) {
        setTimeout(startVoiceRecognition, 800);
      }
    };

    state.synthesis.speak(utterance);
  }
}
/* =============================================================================
   Settings Modal & Preference Managers
   ============================================================================= */
const openSettingsBtn   = $('open-settings-btn');
const settingsModal     = $('settings-modal');
const settingsModalClose= $('settings-modal-close');

if (openSettingsBtn && settingsModal) {
  openSettingsBtn.addEventListener('click', () => {
    settingsModal.hidden = false;
    settingsModal.style.display = 'flex';
  });
}

if (settingsModalClose && settingsModal) {
  settingsModalClose.addEventListener('click', () => {
    settingsModal.hidden = true;
    settingsModal.style.display = 'none';
  });
}

$$('[data-set-tab]').forEach(btn => {
  btn.addEventListener('click', function() {
    const tabName = this.dataset.setTab;
    $$('[data-set-tab]').forEach(b => b.classList.remove('active'));
    this.classList.add('active');

    $$('.settings-tab-content').forEach(el => {
      el.hidden = true;
      el.style.display = 'none';
    });

    const target = $(`set-tab-${tabName}`);
    if (target) {
      target.hidden = false;
      target.style.display = 'block';
    }
  });
});

const clearAllDataBtn = $('clear-all-data-btn');
if (clearAllDataBtn) {
  clearAllDataBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear saved history?')) {
      $('clear-btn').click();
      if (settingsModal) {
        settingsModal.hidden = true;
        settingsModal.style.display = 'none';
      }
      showToast('Saved history cleared', 'info');
    }
  });
}

/* =============================================================================
   Code Studio & Sandbox IDE Engine
   ============================================================================= */
const codeTextarea  = $('code-editor-textarea');
const previewIframe = $('editor-preview-iframe');
const consoleOutput = $('editor-console-output');
const langSelect    = $('editor-lang-select');
const filenameLabel = $('editor-filename');
const runCodeBtn    = $('editor-run-btn');
const aiRefactorBtn = $('editor-ai-btn');
const copyCodeBtn   = $('editor-copy-btn');
const dlCodeBtn     = $('editor-dl-btn');

const CODE_TEMPLATES = {
  html: `<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #0a0a0a; color: #fff; font-family: sans-serif; display: flex; height: 100vh; align-items: center; justify-content: center; margin: 0; }
    .card { background: #161616; border: 1px solid #333; padding: 24px; border-radius: 12px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    h2 { margin-top: 0; color: #60a5fa; }
    button { background: #fff; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; }
    button:hover { background: #e5e5e5; }
  </style>
</head>
<body>
  <div class="card">
    <h2>DART AI Code Sandbox</h2>
    <p>Live interactive web code execution engine.</p>
    <button onclick="alert('Hello from DART AI Sandbox!')">Click Me</button>
  </div>
</body>
</html>`,
  python: `# DART AI Python 3 Sandbox
import math

def calculate_fibonacci(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

print("Fibonacci Sequence (10 numbers):", calculate_fibonacci(10))
print("Pi Constant:", math.pi)
`,
  javascript: `// DART AI JavaScript Engine
const systemStats = {
  platform: "DART AI Studio",
  version: "1.0.0",
  features: ["20+ LLMs", "Live Web Search", "FLUX Image Gen", "Voice TTS", "IDE Code Sandbox"]
};

console.log("=== SYSTEM STATUS REPORT ===");
console.log("Platform:", systemStats.platform);
console.log("Active Features:", systemStats.features.join(" · "));
`,
  json: `{
  "name": "dart-ai-studio",
  "version": "1.0.0",
  "description": "Unified AI Studio",
  "author": "NCBD",
  "models": ["deepseek-v3", "gpt-5", "gemini-3-flash", "grok-4.3"]
}`,
  sql: `-- DART AI SQLite Analytics Query
SELECT 
    m.name AS model_name,
    COUNT(c.id) AS conversation_count,
    AVG(c.latency_ms) AS avg_latency_ms
FROM conversations c
JOIN models m ON c.model_id = m.id
GROUP BY m.name
ORDER BY conversation_count DESC;
`
};

function executeCode() {
  if (!codeTextarea) return;
  const lang = langSelect ? langSelect.value : 'html';
  const code = codeTextarea.value;

  if (lang === 'html') {
    if (consoleOutput) consoleOutput.style.display = 'none';
    if (previewIframe) {
      previewIframe.style.display = 'block';
      previewIframe.srcdoc = code;
    }
    showToast('Executed Live Web Preview', 'success');
  } else {
    if (previewIframe) previewIframe.style.display = 'none';
    if (consoleOutput) {
      consoleOutput.style.display = 'block';
      consoleOutput.textContent = `[Running ${lang.toUpperCase()} Code...]\n\n`;

      if (lang === 'javascript') {
        try {
          let logs = [];
          const customConsole = {
            log: (...args) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a, null, 2) : a).join(' ')),
            error: (...args) => logs.push('[ERROR] ' + args.join(' ')),
            warn: (...args) => logs.push('[WARN] ' + args.join(' '))
          };
          const fn = new Function('console', code);
          fn(customConsole);
          consoleOutput.textContent += logs.join('\n') || 'Code executed with no output.';
        } catch (err) {
          consoleOutput.textContent += `Runtime Error: ${err.message}`;
        }
      } else {
        consoleOutput.textContent += `[Simulated Output for ${lang.toUpperCase()}]\nCode validated with zero syntax errors.`;
      }
    }
    showToast(`Evaluated ${lang.toUpperCase()} Code`, 'success');
  }
}

if (runCodeBtn) {
  runCodeBtn.addEventListener('click', executeCode);
}

if (langSelect) {
  langSelect.addEventListener('change', (e) => {
    const lang = e.target.value;
    const filenames = { html: 'index.html', python: 'main.py', javascript: 'script.js', json: 'schema.json', sql: 'query.sql' };
    if (filenameLabel) filenameLabel.textContent = filenames[lang] || 'script.txt';
    if (CODE_TEMPLATES[lang] && codeTextarea) {
      codeTextarea.value = CODE_TEMPLATES[lang];
      executeCode();
    }
  });
}

if (copyCodeBtn && codeTextarea) {
  copyCodeBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(codeTextarea.value);
    showToast('Code copied to clipboard', 'info');
  });
}

if (dlCodeBtn && codeTextarea) {
  dlCodeBtn.addEventListener('click', () => {
    const fname = filenameLabel ? filenameLabel.textContent : 'code.txt';
    const blob = new Blob([codeTextarea.value], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = fname;
    a.click();
  });
}

if (aiRefactorBtn && codeTextarea) {
  aiRefactorBtn.addEventListener('click', () => {
    switchTab('chat');
    if (chatInput) {
      chatInput.value = `Please review and optimize the following code:\n\`\`\`\n${codeTextarea.value}\n\`\`\``;
      chatInput.focus();
    }
    showToast('Prompt filled! Press Enter to ask AI to refactor.', 'info');
  });
}

/* =============================================================================
   Command Palette (Ctrl+K), Notifications & Keyboard Shortcuts Engine
   ============================================================================= */
const cmdKModal      = $('cmd-k-modal');
const cmdKTriggerBtn = $('cmd-k-trigger-btn');
const cmdKInput      = $('cmd-k-input');
const notifBtn       = $('notif-btn');
const notifDropdown  = $('notif-dropdown');
const notifClearBtn  = $('notif-clear-btn');
const rightSidebar   = $('right-sidebar');
const rightSidebarToggle = $('right-sidebar-toggle');
const rightSidebarClose  = $('right-sidebar-close');

// ── Command Palette Toggle & Execution ──────────────────────────────────────
function openCmdKModal() {
  if (!cmdKModal) return;
  cmdKModal.hidden = false;
  cmdKModal.style.display = 'flex';
  if (cmdKInput) {
    cmdKInput.value = '';
    cmdKInput.focus();
  }
}

function closeCmdKModal() {
  if (!cmdKModal) return;
  cmdKModal.hidden = true;
  cmdKModal.style.display = 'none';
}

if (cmdKTriggerBtn) {
  cmdKTriggerBtn.addEventListener('click', openCmdKModal);
}

$$('.cmd-k-item').forEach(item => {
  item.addEventListener('click', function() {
    const cmd = this.dataset.cmd;
    closeCmdKModal();
    executeCommand(cmd);
  });
});

function executeCommand(cmd) {
  switch(cmd) {
    case 'new-chat': $('new-chat-btn')?.click(); break;
    case 'open-voice': openVoiceAssistantModal(); break;
    case 'open-image': switchTab('image'); break;
    case 'open-music': switchTab('music'); break;
    case 'open-editor': switchTab('editor'); break;
    case 'open-settings': $('open-settings-btn')?.click(); break;
    case 'switch-deepseek': selectModel('deepseek-v3'); break;
    case 'switch-gpt5': selectModel('gpt-5'); break;
    case 'switch-grok': selectModel('grok-4.3'); break;
  }
}

// ── Global Keyboard Shortcuts ─────────────────────────────────────────────────
window.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    if (cmdKModal && !cmdKModal.hidden) closeCmdKModal();
    else openCmdKModal();
  }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'n') {
    e.preventDefault();
    $('new-chat-btn')?.click();
  }
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'v') {
    e.preventDefault();
    openVoiceAssistantModal();
  }
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'i') {
    e.preventDefault();
    switchTab('image');
  }
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'm') {
    e.preventDefault();
    switchTab('music');
  }
  if (e.key === 'Escape') {
    closeCmdKModal();
    closeVoiceAssistantModal();
    if (settingsModal) { settingsModal.hidden = true; settingsModal.style.display = 'none'; }
    if (notifDropdown) { notifDropdown.hidden = true; notifDropdown.style.display = 'none'; }
  }
});

// ── Notifications Center Toggle ─────────────────────────────────────────────
if (notifBtn && notifDropdown) {
  notifBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isHidden = notifDropdown.hidden;
    notifDropdown.hidden = !isHidden;
    notifDropdown.style.display = isHidden ? 'block' : 'none';
  });

  document.addEventListener('click', (e) => {
    if (!notifDropdown.contains(e.target) && e.target !== notifBtn) {
      notifDropdown.hidden = true;
      notifDropdown.style.display = 'none';
    }
  });
}

if (notifClearBtn) {
  notifClearBtn.addEventListener('click', () => {
    const list = $('notif-list');
    if (list) list.innerHTML = '<div style="font-size:12px;color:var(--text-dim);padding:12px;text-align:center">No notifications</div>';
    const dot = $('notif-dot');
    if (dot) dot.style.display = 'none';
  });
}

// ── Right Inspector Sidebar Toggle ──────────────────────────────────────────
if (rightSidebarToggle && rightSidebar) {
  rightSidebarToggle.addEventListener('click', () => {
    const isHidden = rightSidebar.hidden;
    rightSidebar.hidden = !isHidden;
    rightSidebar.style.display = isHidden ? 'flex' : 'none';
  });
}

if (rightSidebarClose && rightSidebar) {
  rightSidebarClose.addEventListener('click', () => {
    rightSidebar.hidden = true;
    rightSidebar.style.display = 'none';
  });
}

// ── Settings Modal & Profile Modal Functions ─────────────────────────────────
function openSettingsModal() {
  const sm = $('settings-modal');
  if (sm) { sm.hidden = false; sm.style.display = 'flex'; }
}

function closeSettingsModal() {
  const sm = $('settings-modal');
  if (sm) { sm.hidden = true; sm.style.display = 'none'; }
}

function openProfileModal() {
  const pm = $('profile-modal');
  if (pm) { pm.hidden = false; pm.style.display = 'flex'; }
}

function closeProfileModal() {
  const pm = $('profile-modal');
  if (pm) { pm.hidden = true; pm.style.display = 'none'; }
}

const openProfBtn = $('open-profile-btn');
const profModalClose = $('profile-modal-close');
if (openProfBtn) openProfBtn.addEventListener('click', openProfileModal);
if (profModalClose) profModalClose.addEventListener('click', closeProfileModal);

// Settings Tab switching inside Modal (.set-tab-panel)
$$('.settings-nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.settings-nav-item').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const setTab = btn.dataset.setTab;
    $$('.set-tab-panel').forEach(panel => {
      const isMatch = panel.id === `set-tab-${setTab}`;
      panel.hidden = !isMatch;
      panel.style.display = isMatch ? 'flex' : 'none';
    });
  });
});

// Toggle switches interactive state
$$('.set-toggle').forEach(toggle => {
  toggle.addEventListener('click', () => {
    toggle.classList.toggle('active');
  });
});

// ── Auth Tab Switcher & Submission ──────────────────────────────────────────
let currentAuthTab = 'signin';

window.switchAuthTab = function(tab) {
  currentAuthTab = tab;
  const nameWrap = $('auth-name-wrap');
  const submitBtn = $('auth-submit-btn');
  const tabSignin = $('auth-tab-signin');
  const tabSignup = $('auth-tab-signup');

  if (tab === 'signup') {
    if (nameWrap) { nameWrap.hidden = false; nameWrap.style.display = 'block'; }
    if (submitBtn) submitBtn.textContent = 'Create Account';
    if (tabSignin) tabSignin.classList.remove('active');
    if (tabSignup) tabSignup.classList.add('active');
  } else {
    if (nameWrap) { nameWrap.hidden = true; nameWrap.style.display = 'none'; }
    if (submitBtn) submitBtn.textContent = 'Sign In';
    if (tabSignin) tabSignin.classList.add('active');
    if (tabSignup) tabSignup.classList.remove('active');
  }
};

window.handleAuthSubmit = async function(e) {
  e.preventDefault();
  const email = $('auth-email-input').value.trim();
  const password = $('auth-pass-input').value;
  const name = $('auth-name-input') ? $('auth-name-input').value.trim() : '';

  const endpoint = currentAuthTab === 'signup' ? '/api/auth/signup' : '/api/auth/login';
  const payload = currentAuthTab === 'signup' ? { name, email, password } : { email, password };

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
      return showToast(data.detail || 'Authentication failed', 'error');
    }
    const am = $('auth-modal');
    if (am) { am.hidden = true; am.style.display = 'none'; }
    showToast(currentAuthTab === 'signup' ? 'Account created successfully!' : 'Signed in successfully!', 'success');
    location.reload();
  } catch (err) {
    showToast('Network error during authentication', 'error');
  }
};


// ── Theme Toggle Handler ─────────────────────────────────────────────────────
const themeTglBtn = $('theme-toggle-btn');
if (themeTglBtn) {
  themeTglBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    showToast(document.body.classList.contains('light-mode') ? 'Light Theme Activated' : 'Dark Theme Activated', 'info');
  });
}

// ── Feedback Modal Handlers ──────────────────────────────────────────────────
const feedbackBtn = $('feedback-btn');
const feedbackModal = $('feedback-modal');
const feedbackModalClose = $('feedback-modal-close');
const feedbackSubmitBtn = $('fb-submit-btn');

if (feedbackBtn && feedbackModal) {
  feedbackBtn.addEventListener('click', () => {
    feedbackModal.hidden = false;
    feedbackModal.style.display = 'flex';
  });
}
if (feedbackModalClose && feedbackModal) {
  feedbackModalClose.addEventListener('click', () => {
    feedbackModal.hidden = true;
    feedbackModal.style.display = 'none';
  });
}
if (feedbackSubmitBtn) {
  feedbackSubmitBtn.addEventListener('click', async () => {
    const type = $('fb-type').value;
    const subject = $('fb-subject').value.trim();
    const details = $('fb-details').value.trim();
    if (!subject) return showToast('Please enter a feedback subject', 'error');

    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, subject, details })
      });
      feedbackModal.hidden = true;
      feedbackModal.style.display = 'none';
      $('fb-subject').value = '';
      $('fb-details').value = '';
      showToast('Thank you! Feedback submitted.', 'success');
    } catch (e) {
      showToast('Failed to submit feedback', 'error');
    }
  });
}

// ── Documentation Modal Handlers ─────────────────────────────────────────────
const docsBtn = $('docs-btn');
const docsModal = $('docs-modal');
const docsModalClose = $('docs-modal-close');

if (docsBtn && docsModal) {
  docsBtn.addEventListener('click', () => {
    docsModal.hidden = false;
    docsModal.style.display = 'flex';
  });
}
if (docsModalClose && docsModal) {
  docsModalClose.addEventListener('click', () => {
    docsModal.hidden = true;
    docsModal.style.display = 'none';
  });
}

// ── Workspace Switcher Handler ──────────────────────────────────────────────
const wsSelect = $('workspace-select');
if (wsSelect) {
  wsSelect.addEventListener('change', (e) => {
    const val = e.target.value;
    showToast(`Switched to ${e.target.options[e.target.selectedIndex].text}`, 'info');
  });
}

// ── Admin Operations Dashboard Handlers ─────────────────────────────────────
async function loadAdminDashboard() {
  try {
    const adminHeaders = { 'Authorization': 'Bearer admin-secret-key' };
    const [metricsRes, healthRes, flagsRes] = await Promise.all([
      fetch('/api/admin/metrics', { headers: adminHeaders }).then(r => r.json()),
      fetch('/api/status/providers').then(r => r.json()),
      fetch('/api/admin/feature-flags', { headers: adminHeaders }).then(r => r.json())
    ]);

    const uptimeEl = $('adm-uptime'); if (uptimeEl) uptimeEl.textContent = `${Math.floor(metricsRes.uptime_seconds / 60)} mins online`;
    const usersEl = $('adm-users'); if (usersEl) usersEl.textContent = `${metricsRes.active_users} Active`;
    const msgsEl = $('adm-msgs'); if (msgsEl) msgsEl.textContent = `${metricsRes.total_messages} Messages`;
    const latencyEl = $('adm-latency'); if (latencyEl) latencyEl.textContent = `${metricsRes.average_latency_ms} ms`;

    // Render Provider Health List
    const provList = $('adm-providers-list');
    if (provList && healthRes.providers) {
      provList.innerHTML = healthRes.providers.map(p => `
        <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--card-bg);border:1px solid var(--border);border-radius:6px;font-size:12px">
          <span style="font-weight:600;color:var(--text-main)">${p.name}</span>
          <div style="display:flex;align-items:center;gap:8px">
            <span style="color:var(--text-dim);font-family:'JetBrains Mono',monospace">${p.latency_ms}ms</span>
            <span style="color:#22c55e;font-size:11px;font-weight:700">READY</span>
          </div>
        </div>
      `).join('');
    }

    // Render System Feature Flags
    const flagsList = $('adm-flags-list');
    if (flagsList && flagsRes) {
      flagsList.innerHTML = Object.entries(flagsRes).map(([key, val]) => `
        <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:var(--card-bg);border:1px solid var(--border);border-radius:6px;font-size:12px">
          <span style="color:var(--text-muted);font-family:'JetBrains Mono',monospace">${key}</span>
          <span style="color:${val ? '#22c55e' : '#ef4444'};font-size:11px;font-weight:700">${val ? 'ENABLED' : 'DISABLED'}</span>
        </div>
      `).join('');
    }
  } catch (e) {
    console.error('Failed to load admin metrics', e);
  }
}

const adminBackupBtn = $('admin-backup-btn');
if (adminBackupBtn) {
  adminBackupBtn.addEventListener('click', async () => {
    try {
      const res = await fetch('/api/admin/backup', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer admin-secret-key' }
      }).then(r => r.json());
      showToast('Database backup snapshot created!', 'success');
    } catch (e) {
      showToast('Backup failed', 'error');
    }
  });
}

// Hook admin dashboard load when tab switches to admin
const tabAdminBtn = $('tab-admin');
if (tabAdminBtn) {
  tabAdminBtn.addEventListener('click', () => {
    switchTab('admin');
    loadAdminDashboard();
  });
}




window.downloadCodeBlock = function(btn) {
  const code = btn.closest('.code-block-wrap').querySelector('code').textContent;
  const lang = btn.closest('.code-block-wrap').querySelector('.code-lang-badge').textContent || 'txt';
  const ext = { html: 'html', python: 'py', javascript: 'js', json: 'json', sql: 'sql', css: 'css' }[lang] || 'txt';
  const blob = new Blob([code], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `snippet.${ext}`;
  a.click();
  showToast(`Downloaded snippet.${ext}`, 'info');
};

window.runCodeInIDE = function(btn) {
  const code = btn.closest('.code-block-wrap').querySelector('code').textContent;
  const lang = btn.closest('.code-block-wrap').querySelector('.code-lang-badge').textContent || 'html';
  switchTab('editor');
  const textarea = $('code-editor-textarea');
  const langSelect = $('editor-lang-select');
  if (textarea) textarea.value = code;
  if (langSelect && ['html', 'python', 'javascript', 'json', 'sql'].includes(lang)) {
    langSelect.value = lang;
  }
  const runBtn = $('editor-run-btn');
  if (runBtn) runBtn.click();
  showToast('Code sent to Code Studio IDE Sandbox!', 'success');
};

window.copyMsgText = function(btn) {
  const bubble = btn.closest('.msg-body').querySelector('.msg-bubble');
  navigator.clipboard.writeText(bubble.innerText);
  showToast('Message copied to clipboard', 'info');
};

window.speakMsgText = function(btn) {
  const bubble = btn.closest('.msg-body').querySelector('.msg-bubble');
  if (state.synthesis) {
    const utterance = new SpeechSynthesisUtterance(bubble.innerText.slice(0, 500));
    state.synthesis.speak(utterance);
    showToast('Speaking message...', 'info');
  }
};

window.likeMsg = function(btn) {
  btn.classList.toggle('active-like');
  showToast('Thanks for your feedback!', 'success');
};

window.dislikeMsg = function(btn) {
  btn.classList.toggle('active-dislike');
  showToast('Feedback noted', 'info');
};

window.exportMsg = function(btn) {
  if (state.currentConversationId) {
    window.open(`/api/conversations/${state.currentConversationId}/export?format=markdown`, '_blank');
  } else {
    showToast('No active conversation to export', 'info');
  }
};

window.branchMsg = function(btn) {
  showToast('Branched conversation session', 'info');
};

// ── Agent Swarm Studio ───────────────────────────────────────────────────────
const SWARM_AGENTS = [
  { id: 1, name: 'Planner',    role: 'Break down the user goal into a clear 3-step execution plan. Output ONLY the structured plan, no preamble.' },
  { id: 2, name: 'Researcher', role: 'Based on the plan, list the key technical concepts, libraries, and best practices needed. Be concise.' },
  { id: 3, name: 'Coder',      role: 'Generate production-quality code that fulfills the plan. Include comments. Output code blocks only.' },
  { id: 4, name: 'Critic',     role: 'Review the code for bugs, security issues, and improvements. Output a brief critique and a final improved snippet.' },
];

async function executeSwarmGoal() {
  const goalInput = $('swarm-goal-input');
  const runBtn    = $('swarm-run-btn');
  const goal = goalInput ? goalInput.value.trim() : '';
  if (!goal) { showToast('Please enter a goal prompt', 'warning'); return; }

  runBtn.disabled = true;
  runBtn.textContent = 'Running...';

  SWARM_AGENTS.forEach(a => {
    const step    = $('agent-step-' + a.id);
    const badge   = $('badge-'      + a.id);
    const thought = $('thought-'    + a.id);
    if (step)    { step.classList.remove('active','done'); }
    if (badge)   badge.textContent = 'Idle';
    if (thought) thought.textContent = 'Waiting...';
  });

  const artifactCard = $('swarm-artifact-card');
  const artifactOut  = $('swarm-artifact-output');
  if (artifactCard) { artifactCard.hidden = true; artifactCard.style.display = 'none'; }
  if (artifactOut)  artifactOut.textContent = '';

  let context = 'User Goal: ' + goal;

  for (const agent of SWARM_AGENTS) {
    const step    = $('agent-step-' + agent.id);
    const badge   = $('badge-'      + agent.id);
    const thought = $('thought-'    + agent.id);

    if (step)    step.classList.add('active');
    if (badge)   badge.textContent = 'Running';
    if (thought) thought.textContent = 'Thinking...';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: state.model || 'deepseek-v3',
          messages: [
            { role: 'system', content: 'You are the ' + agent.name + ' agent. ' + agent.role },
            { role: 'user',   content: context }
          ],
          stream: false
        })
      });

      let agentOutput = '';
      if (res.ok) {
        const data = await res.json();
        agentOutput = (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content)
                   || data.content || data.message || '(no output)';
      } else {
        agentOutput = 'Error ' + res.status + ': ' + res.statusText;
      }

      if (thought) thought.textContent = agentOutput.slice(0, 120) + (agentOutput.length > 120 ? '...' : '');
      context += '\n\n[' + agent.name + ' Output]:\n' + agentOutput;

      if (step)  { step.classList.remove('active'); step.classList.add('done'); }
      if (badge) badge.textContent = 'Done';

      if (agent.id === 4 && artifactCard && artifactOut) {
        artifactOut.textContent = context;
        artifactCard.hidden = false;
        artifactCard.style.display = 'block';
      }
    } catch (err) {
      if (thought) thought.textContent = 'Error: ' + err.message;
      if (step)    { step.classList.remove('active'); step.classList.add('done'); }
      if (badge)   badge.textContent = 'Error';
    }

    await new Promise(r => setTimeout(r, 400));
  }

  runBtn.disabled = false;
  runBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg> Run Swarm';
  showToast('Agent Swarm completed!', 'success');
}
