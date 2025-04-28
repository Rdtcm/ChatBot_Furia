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
  
    // Mostra debug no carregamento
    console.log('chat.js carregado. sendButton=', sendButton, 'messageInput=', messageInput);
  
    // Adiciona clique nas conversas anteriores
    if (previousChatsList) {
      previousChatsList.addEventListener('click', e => {
        if (e.target.tagName === 'LI') {
          previousChatsList.querySelectorAll('li').forEach(li => li.classList.remove('active'));
          e.target.classList.add('active');
          loadMessages(e.target.dataset.chatId);
        }
      });
    }
  
    // Carrega mensagens
    function loadMessages(chatId) {
      console.log('→ loadMessages(', chatId, ')');
      fetch(`/chat/api/messages/${chatId}/`)
        .then(res => res.json())
        .then(data => {
          chatMessages.innerHTML = '';
          data.messages.forEach(msg => {
            const p = document.createElement('p');
            p.textContent = `${msg.sender}: ${msg.text}`;
            chatMessages.appendChild(p);
          });
        })
        .catch(err => console.error('Erro ao carregar mensagens:', err));
    }
  
    // Exibe mensagem
    function displayMessage({ sender, content }) {
      const div = document.createElement('div');
      div.textContent = `${sender}: ${content}`;
      chatMessages.appendChild(div);
    }
  
    // Envia mensagem ao backend
    async function sendMessage(message, chatId) {
      console.log('→ sendMessage chamado', { message, chatId });
  
      try {
        const res = await fetch('/chat/api/send/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({ message, chat_id: chatId }),
        });
  
        console.log('→ fetch completo, status=', res.status);
  
        if (!res.ok) {
          const text = await res.text();
          console.error('Erro ao enviar mensagem:', res.status, text);
          return;
        }
  
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
        console.log('→ botão clicado');
        const messageText = messageInput.value.trim();
        if (!messageText) return;
  
        const active = previousChatsList.querySelector('.active');
        const chatId = active ? active.dataset.chatId : null;
        sendMessage(messageText, chatId);
      });
    }
  });
  