// Seleciona elementos do HTML
const sendButton = document.getElementById('send-button');
const messageInput = document.getElementById('message-input');
const previousChatsList = document.getElementById('previous-chats');
const chatMessages = document.getElementById('chat-messages');

// Função para pegar o token CSRF do cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Carregar mensagens do chat selecionado
function loadMessages(chatId) {
    fetch(`/chat/api/messages/${chatId}/`)
        .then(response => response.json())
        .then(data => {
            chatMessages.innerHTML = '';
            data.messages.forEach(msg => {
                const p = document.createElement('p');
                p.textContent = `${msg.sender}: ${msg.text}`;
                chatMessages.appendChild(p);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar mensagens:', error);
        });
}

// Enviar uma nova mensagem
async function sendMessage() {
    const message = document.getElementById('message-input').value;
    const chatId = 1; // Exemplo: ID do chat

    // Enviar mensagem para o servidor
    const response = await fetch('/chat/api/send/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Adicionar o CSRF se necessário
        },
        body: JSON.stringify({ message: message, chat_id: chatId }),
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Mensagem enviada:', data);

        // Exibir mensagem do usuário
        displayMessage({
            content: data.user_message.text,
            sender: 'Você',
        });

        // Exibir resposta do bot
        displayMessage({
            content: data.bot_message.text,
            sender: 'Bot',
        });
    } else {
        console.error('Erro ao enviar mensagem');
    }
}

function displayMessage(messageData) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = `${messageData.sender}: ${messageData.content}`;
    chatBox.appendChild(messageDiv);
}


// Quando clica em uma conversa da sidebar
if (previousChatsList) {
    previousChatsList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const chatId = event.target.dataset.chatId;
            if (chatId) {
                // Remove 'active' de todos
                previousChatsList.querySelectorAll('li').forEach(li => {
                    li.classList.remove('active');
                });

                // Adiciona 'active' no clicado
                event.target.classList.add('active');

                // Carrega as mensagens do chat clicado
                loadMessages(chatId);
            }
        }
    });
}

// Quando clica no botão de enviar
if (sendButton) {
    sendButton.addEventListener('click', function() {
        const messageText = messageInput.value.trim();
        const activeChat = previousChatsList.querySelector('.active');
        const chatId = activeChat ? activeChat.dataset.chatId : null;

        console.log('Tentando enviar:', { messageText, chatId });

        if (messageText && chatId) {
            sendMessage();
        } else if (!chatId) {
            alert('Selecione uma conversa antes de enviar a mensagem.');
        }
    });
}
