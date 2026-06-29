/**
 * JARVIS AI Assistant — Chat Module
 * Handles AJAX-based chat interaction with the backend.
 */
document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingIndicator = document.getElementById('typingIndicator');

    if (!chatInput || !sendBtn) return;

    // Get CSRF token from meta tags
    const csrfToken = document.querySelector('meta[name="_csrf"]')?.getAttribute('content');
    const csrfHeader = document.querySelector('meta[name="_csrf_header"]')?.getAttribute('content');

    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);

    // Send message on Enter key
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize input
    chatInput.addEventListener('input', () => {
        sendBtn.disabled = chatInput.value.trim() === '';
    });

    // Initial scroll to bottom
    scrollToBottom();

    /**
     * Send a chat message to the server.
     */
    async function sendMessage() {
        const question = chatInput.value.trim();
        if (!question) return;

        // Add user message bubble
        appendMessage('user', question, formatTime(new Date()));
        chatInput.value = '';
        sendBtn.disabled = true;

        // Show typing indicator
        showTyping(true);

        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            if (csrfToken && csrfHeader) {
                headers[csrfHeader] = csrfToken;
            }

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            showTyping(false);

            // Add bot response bubble
            appendMessage('bot', data.response, formatTime(new Date(data.timestamp)));

        } catch (error) {
            showTyping(false);
            appendMessage('bot', '⚠️ Sorry, I encountered an error. Please try again.', formatTime(new Date()));
            console.error('Chat error:', error);
        }

        sendBtn.disabled = false;
        chatInput.focus();
    }

    /**
     * Append a message bubble to the chat area.
     */
    function appendMessage(type, text, time) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        const avatarText = type === 'bot' ? 'J' : 'U';

        // Convert newlines to <br> for display
        const formattedText = text.replace(/\n/g, '<br>');

        messageDiv.innerHTML = `
            <div class="msg-avatar">${avatarText}</div>
            <div>
                <div class="msg-bubble">${formattedText}</div>
                <div class="msg-time">${time}</div>
            </div>
        `;

        // Insert before typing indicator if it exists
        if (typingIndicator) {
            chatMessages.insertBefore(messageDiv, typingIndicator);
        } else {
            chatMessages.appendChild(messageDiv);
        }

        scrollToBottom();
    }

    /**
     * Toggle typing indicator visibility.
     */
    function showTyping(visible) {
        if (typingIndicator) {
            typingIndicator.classList.toggle('visible', visible);
            scrollToBottom();
        }
    }

    /**
     * Scroll chat to the bottom.
     */
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    /**
     * Format a Date object to a readable time string.
     */
    function formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
});
