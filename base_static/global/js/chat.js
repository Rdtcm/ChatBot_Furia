// chat.js

document.addEventListener('DOMContentLoaded', () => {
  // Elementos do DOM
  const sendButton        = document.getElementById('send-button');
  const messageInput      = document.getElementById('message-input');
  const previousChatsList = document.getElementById('previous-chats');
  const chatMessages      = document.getElementById('chat-messages');

  // Pega CSRF token do cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        }
      });
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  console.log('chat.js carregado. sendButton=', sendButton, 'messageInput=', messageInput);

  // Clique nas conversas anteriores
  if (previousChatsList) {
    previousChatsList.addEventListener('click', e => {
      if (e.target.tagName === 'LI') {
        previousChatsList.querySelectorAll('li').forEach(li => li.classList.remove('active'));
        e.target.classList.add('active');
        loadMessages(e.target.dataset.chatId);
      }
    });
  }

  // Carrega histórico de mensagens
  function loadMessages(chatId) {
    fetch(`/chat/api/messages/${chatId}/`)
      .then(res => res.json())
      .then(data => {
        chatMessages.innerHTML = '';
        data.messages.forEach(msg => {
          renderMessage(msg.is_bot ? 'Bot' : msg.sender, msg.text, msg.is_bot);
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
      })
      .catch(err => console.error('Erro ao carregar mensagens:', err));
  }

  // Normaliza conteúdo antigo (string que é repr. de lista) ou novo (string/array)
  function normalizeContent(content) {
    if (Array.isArray(content)) return content;
    const s = content.trim();
    if (s.startsWith('[') && s.endsWith(']')) {
      let inner = s.slice(1, -1);
      return inner.split(/',\s*'/).map(item => item.replace(/^'+|'+$/g, ''));
    }
    return content.split('\n');
  }

  // Função genérica para renderizar uma mensagem
  function renderMessage(sender, content, isBot) {
    const div = document.createElement('div');
    div.classList.add('message', isBot ? 'received' : 'sent');

    let html = `<strong>${sender}:</strong><br>`;
    const lines = normalizeContent(content);
    lines.forEach(line => {
      const safe = line.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      html += `${safe}<br>`;
    });

    div.innerHTML = html;
    chatMessages.appendChild(div);
  }

  // Exibe na tela mensagens novas (usuário e bot)
  function displayMessage({ sender, content }) {
    renderMessage(sender, content, sender !== 'Você');
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // Envia mensagem ao backend
  async function sendMessage(message, chatId) {
    console.log('→ sendMessage', { message, chatId });
    try {
      const res = await fetch('/chat/api/send/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ message, chat_id: chatId }),
      });
      console.log('→ fetch status=', res.status);

      const data = await res.json();
      displayMessage({ sender: 'Você', content: data.user_message.text });
      displayMessage({ sender: 'Bot', content: data.bot_message.text });
      messageInput.value = '';
    } catch (err) {
      console.error('Erro de rede ao enviar mensagem:', err);
    }
  }

  // Handler do botão Enviar
  if (sendButton) {
    sendButton.addEventListener('click', e => {
      e.preventDefault();
      const text = messageInput.value.trim();
      if (!text) return;
      const active = previousChatsList.querySelector('.active');
      const chatId = active ? active.dataset.chatId : null;
      sendMessage(text, chatId);
    });
  }

  // Mensagem de boas-vindas ao carregar
  const welcomeMessage = `
  🎮 FALA, FURIOSO! 🐍  
  Eu sou o bot oficial da FURIA, pronto pra te deixar por dentro de tudo!  
  Quer saber quando é o próximo jogo, estatísticas dos players, ou só trocar uma ideia sobre o time mais brabo do cenário?  
  Manda ver no chat e #DIADEFURIA começa agora!

  🔥 VAMOS PRA CIMA! 🔥
    `;
  renderMessage('Bot', welcomeMessage, true);
});


