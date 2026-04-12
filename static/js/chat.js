// static/js/chat.js
const messagesContainer = document.getElementById('messages');
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

userInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = '';
    userInput.focus();

    const typingId = showTyping();

    sendBtn.disabled = true;
    userInput.disabled = true;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
        .then(response => response.json())
        .then(data => {
            removeTyping(typingId);
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            removeTyping(typingId);
            addMessage('<p>Sorry, something went wrong. Please try again. 😅</p>', 'bot');
            console.error('Error:', error);
        })
        .finally(() => {
            sendBtn.disabled = false;
            userInput.disabled = false;
            userInput.focus();
        });
}

function sendSuggestion(text) {
    userInput.value = text;
    sendMessage();
}

function clearChat() {
    fetch('/clear', { method: 'POST' })
        .then(() => {
            // Keep only the welcome message
            const messages = messagesContainer.children;
            while (messages.length > 1) {
                messages[messages.length - 1].remove();
            }
        });
}

function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (type === 'user') {
        contentDiv.textContent = content;
    } else {
        contentDiv.innerHTML = content;
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    scrollToBottom();
}

function showTyping() {
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = id;

    messageDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;

    messagesContainer.appendChild(messageDiv);
    scrollToBottom();
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}