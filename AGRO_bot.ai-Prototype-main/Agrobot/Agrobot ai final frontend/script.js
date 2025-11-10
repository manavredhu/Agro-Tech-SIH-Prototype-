document.addEventListener('DOMContentLoaded', () => {
  /* ---------- Navbar dropdown ---------- */
  const dropdown = document.querySelector('.dropdown');
  if (dropdown) {
    const btn = dropdown.querySelector('.drop-btn');
    btn.addEventListener('click', () => {
      dropdown.classList.toggle('open');
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
    });
    document.addEventListener('click', (e) => {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Region → languages (India only) ---------- */
  const langsByRegion = {
    north: ["हिंदी", "अंग्रेज़ी", "भोजपुरी", "पंजाबी"],
    south: ["తెలుగు", "தமிழ்", "ಕನ್ನಡ", "മലയാളം", "English"],
    east:  ["বাংলা", "ଓଡ଼ିଆ", "অসমীয়া", "हिंदी"],
    west:  ["मराठी", "ગુજરાતી", "हिंदी", "English"]
  };

  const tabs = document.querySelectorAll('.tab');
  const grid = document.getElementById('langGrid');

  function renderLangs(regionKey) {
    const list = langsByRegion[regionKey] || [];
    grid.innerHTML = list
      .map(l => `<div class="lang-pill">${l} <span class="wa" title="Chat">💬</span></div>`)
      .join('');
  }

  tabs.forEach(t => t.addEventListener('click', () => {
    tabs.forEach(tb => tb.classList.remove('active'));
    t.classList.add('active');
    renderLangs(t.dataset.region);
  }));

  // initial render
  renderLangs('north');

  /* ---------- Chatbot functionality ---------- */
  const sendBtn = document.getElementById('send');
  const input = document.getElementById('msg');
  const chips = document.querySelectorAll('.chip');
  const chatMessages = document.getElementById('chatMessages') || createChatMessagesContainer();

  // Create chat messages container if it doesn't exist
  function createChatMessagesContainer() {
    const container = document.createElement('div');
    container.id = 'chatMessages';
    container.className = 'chat-messages';
    const widgetBody = document.querySelector('.widget-body');
    const title = widgetBody.querySelector('.widget-title');
    widgetBody.insertBefore(container, title.nextElementSibling);
    return container;
  }


  // Add initial bot message
  addBotMessage("Hello! I'm Farmer.CHAT. How can I help with your farming questions today?");

  chips.forEach(c => c.addEventListener('click', () => {
    input.value = c.textContent.trim();
    input.focus();
  }));

  if (sendBtn && input) {
    sendBtn.addEventListener('click', handleSendMessage);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleSendMessage();
    });
  }

  async function handleSendMessage() {
    const text = (input.value || '').trim();
    if (!text) return;
    
    // Add user message to chat
    addUserMessage(text);
    input.value = '';
    // mic button coustomization
    const micBtn = document.getElementById('micBtn');
const chatInput = document.getElementById('chatInput');

micBtn.addEventListener('click', () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-IN'; // Set language as needed
  recognition.start();

  recognition.onresult = (event) => {
    chatInput.value = event.results[0][0].transcript;
  };

  recognition.onerror = (event) => {
    alert('Voice recognition error: ' + event.error);
  };
});
    
    // Get bot response
    const botResponse = await getBotResponse(text);
    addBotMessage(botResponse);
  }

  function addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `<p>${text}</p>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function addBotMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `<p>${text}</p>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function getBotResponse(message) {
    // Simple farming knowledge base
    const knowledgeBase = {
      'chili': 'Plant chili in well-drained soil with good sunlight. Ideal temperature is 20-30°C. Water regularly but avoid waterlogging.',
      'ant': 'For black ants, use cinnamon powder, neem oil, or diatomaceous earth around the plants. Keep the area clean.',
      'rice': 'Rice yield improves with proper water management (2-3 inches of standing water), organic fertilizers, and timely weeding.',
      'maize': 'Sow maize 2-3 weeks before monsoon. Use well-drained soil and maintain 60-75 cm spacing between plants.',
      'coffee': 'Coffee plants need shade, well-drained acidic soil, and regular pruning. Protect from frost.',
      'yield': 'Improve yield by using quality seeds, proper irrigation, balanced fertilizers, and timely pest control.',
      'plant': 'Best planting time depends on the crop and region. Most crops do well at the beginning of rainy season.',
      'sow': 'Sowing time varies by crop. Generally, sow when soil is warm and there\'s adequate moisture.',
      'fertilizer': 'Use organic fertilizers like compost or vermicompost. Chemical fertilizers should be used based on soil testing.',
      'water': 'Water requirements vary by crop. Most crops need regular watering but avoid overwatering.',
      'pest': 'For pest control, use organic methods like neem oil, garlic spray, or introduce beneficial insects.',
      'soil': 'Good soil should be well-drained, rich in organic matter, and have proper pH balance for the specific crop.'
    };

    // Convert message to lowercase for matching
    const lowerMessage = message.toLowerCase();
    
    // Check for keywords and return appropriate response
    for (const [keyword, response] of Object.entries(knowledgeBase)) {
      if (lowerMessage.includes(keyword)) {
        return response;
      }
    }
    
    // Default response if no keywords matched
    return "I understand you're asking about farming. For more specific advice, please provide details about your crop, region, and the specific issue you're facing.";
  }

  /* ---------- Pricing plan toggle (visual only) ---------- */
  const planBtns = document.querySelectorAll('.plan-btn');
  planBtns.forEach(b => b.addEventListener('click', () => {
    planBtns.forEach(x => x.classList.remove('active'));
    b.classList.add('active');
  }));

  /* ---------- FAQ accordion ---------- */
  const accBtns = document.querySelectorAll('.acc-btn');
  accBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.item');
      const open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
});