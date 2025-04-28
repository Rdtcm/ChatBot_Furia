// Seleção de elementos do DOM
const previousChatsList = document.getElementById('previous-chats');
const chatMessagesDiv = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Função para carregar mensagens da conversa selecionada
function loadMessages(chatId) {
    chatMessagesDiv.innerHTML = '<p class="loading-message">Carregando mensagens...</p>';
    fetch(`/chat/api/messages/${chatId}/`)
        .then(response => response.json())
        .then(data => {
            chatMessagesDiv.innerHTML = ''; // Limpa a mensagem de carregamento
            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(message.is_bot ? 'received' : 'sent');
                messageElement.textContent = message.text;
                chatMessagesDiv.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar mensagens:', error);
            chatMessagesDiv.innerHTML = '<p class="error-message">Erro ao carregar mensagens.</p>';
        });
}

// Evento para carregar a conversa ao clicar em uma conversa anterior
if (previousChatsList) {
    previousChatsList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const chatId = event.target.dataset.chatId;
            if (chatId) {
                loadMessages(chatId);
            }
        }
    });
}

// Função para enviar mensagens
function sendMessage(messageText, chatId) {
    fetch('/chat/api/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', // <<< Adicionei aqui também para consistência
        },
        body: JSON.stringify({
            message: messageText,
            chat_id: chatId,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const userMessageElement = document.createElement('div');
            userMessageElement.classList.add('message', 'sent');
            userMessageElement.textContent = data.user_message.text;
            chatMessagesDiv.appendChild(userMessageElement);

            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('message', 'received');
            botMessageElement.textContent = data.bot_message.text;
            chatMessagesDiv.appendChild(botMessageElement);

            messageInput.value = '';
        }
    })
    .catch(error => {
        console.error('Erro ao enviar mensagem:', error);
        alert('Erro ao enviar mensagem.');
    });
}

// Evento para envio da mensagem
if (sendButton && messageInput) {
    sendButton.addEventListener('click', function() {
        const messageText = messageInput.value.trim();
        const chatId = previousChatsList.querySelector('.active')?.dataset.chatId;
        if (messageText && chatId) {
            sendMessage(messageText, chatId);
        }
    });

    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });
}

// Função para atualizar a lista de conversas
function updatePreviousChats() {
    fetch('/chat/api/chats/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest' // <<< ESSA LINHA É A CORREÇÃO PRINCIPAL
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.previous_chat) {
            previousChatsList.innerHTML = '';
            data.previous_chat.forEach(chat => {
                const li = document.createElement('li');
                li.dataset.chatId = chat.id;
                li.textContent = chat.title || 'Chat com Bot';
                previousChatsList.appendChild(li);
            });
        }
    })
    .catch(error => console.error('Erro ao carregar conversas:', error));
}

// Inicializa a lista de conversas ao carregar a página
updatePreviousChats();