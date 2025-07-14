(function() {
    'use strict';

    // Configuration
    const API_URL = window.LENILANI_CHATBOT_URL || 'http://localhost:8000';
    
    // Create styles
    const styles = `
        .lenilani-chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        
        .lenilani-chat-bubble {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .lenilani-chat-bubble:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        }
        
        .lenilani-chat-bubble svg {
            width: 30px;
            height: 30px;
            fill: white;
        }
        
        .lenilani-chat-window {
            position: fixed;
            bottom: 100px;
            right: 20px;
            width: 380px;
            height: 600px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 10000;
        }
        
        .lenilani-chat-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            color: white;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .lenilani-chat-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        .lenilani-chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s ease;
        }
        
        .lenilani-chat-close:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .lenilani-chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .lenilani-message {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 16px;
            word-wrap: break-word;
        }
        
        .lenilani-message.user {
            background: #007AFF;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
        
        .lenilani-message.bot {
            background: #F0F0F0;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }
        
        .lenilani-chat-input-container {
            padding: 20px;
            border-top: 1px solid #E0E0E0;
            display: flex;
            gap: 10px;
        }
        
        .lenilani-chat-input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #E0E0E0;
            border-radius: 24px;
            outline: none;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .lenilani-chat-input:focus {
            border-color: #4ECDC4;
        }
        
        .lenilani-chat-send {
            background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s ease;
        }
        
        .lenilani-chat-send:hover {
            transform: scale(1.1);
        }
        
        .lenilani-chat-send svg {
            width: 20px;
            height: 20px;
            fill: white;
        }
        
        .lenilani-typing {
            display: flex;
            gap: 4px;
            padding: 12px 16px;
            background: #F0F0F0;
            border-radius: 16px;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }
        
        .lenilani-typing span {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: lenilani-bounce 1.4s infinite ease-in-out both;
        }
        
        .lenilani-typing span:nth-child(1) { animation-delay: -0.32s; }
        .lenilani-typing span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes lenilani-bounce {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        @media (max-width: 480px) {
            .lenilani-chat-window {
                width: 100%;
                height: 100%;
                right: 0;
                bottom: 0;
                border-radius: 0;
            }
            
            .lenilani-chat-bubble {
                bottom: 10px;
                right: 10px;
            }
        }
    `;
    
    // Create chat HTML
    const chatHTML = `
        <div class="lenilani-chat-widget">
            <div class="lenilani-chat-bubble" id="lenilani-bubble">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3 .97 4.29L1 23l6.71-1.97C9 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm0 18c-1.41 0-2.73-.36-3.88-.98l-.28-.14-2.92.77.79-2.89-.18-.29C4.91 14.73 4.55 13.38 4.55 12c0-4.41 3.59-8 8-8s8 3.59 8 8-3.59 8-8 8z"/>
                </svg>
            </div>
            
            <div class="lenilani-chat-window" id="lenilani-window">
                <div class="lenilani-chat-header">
                    <div class="lenilani-chat-title">🌺 Chat with Leni Begonia</div>
                    <button class="lenilani-chat-close" id="lenilani-close">×</button>
                </div>
                
                <div class="lenilani-chat-messages" id="lenilani-messages"></div>
                
                <div class="lenilani-chat-input-container">
                    <input 
                        type="text" 
                        class="lenilani-chat-input" 
                        id="lenilani-input" 
                        placeholder="Type your message..."
                    />
                    <button class="lenilani-chat-send" id="lenilani-send">
                        <svg viewBox="0 0 24 24">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Initialize widget
    function initWidget() {
        // Add styles
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        
        // Add HTML
        const container = document.createElement('div');
        container.innerHTML = chatHTML;
        document.body.appendChild(container);
        
        // Get elements
        const bubble = document.getElementById('lenilani-bubble');
        const window = document.getElementById('lenilani-window');
        const closeBtn = document.getElementById('lenilani-close');
        const input = document.getElementById('lenilani-input');
        const sendBtn = document.getElementById('lenilani-send');
        const messagesContainer = document.getElementById('lenilani-messages');
        
        let isOpen = false;
        let conversationId = null;
        
        // Toggle chat window
        function toggleChat() {
            isOpen = !isOpen;
            window.style.display = isOpen ? 'flex' : 'none';
            if (isOpen && !conversationId) {
                startConversation();
            }
        }
        
        // Start conversation
        async function startConversation() {
            try {
                conversationId = 'web-' + Date.now();
                
                console.log('Starting conversation with API:', API_URL);
                
                // Send initial message to start conversation
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    mode: 'cors',
                    body: JSON.stringify({ 
                        message: 'Aloha',
                        session_id: conversationId
                    })
                });
                
                console.log('Response status:', response.status);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                // Add bot's response
                addMessage(data.response, 'bot');
            } catch (error) {
                console.error('Failed to start conversation:', error);
                console.error('API URL:', API_URL);
                console.error('Full error:', error.message);
                addMessage('Sorry, I\'m having trouble connecting. Please try again later.', 'bot');
            }
        }
        
        // Add message to chat
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `lenilani-message ${sender}`;
            messageDiv.textContent = text;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Show typing indicator
        function showTyping() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'lenilani-typing';
            typingDiv.id = 'typing-indicator';
            typingDiv.innerHTML = '<span></span><span></span><span></span>';
            messagesContainer.appendChild(typingDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Hide typing indicator
        function hideTyping() {
            const typing = document.getElementById('typing-indicator');
            if (typing) typing.remove();
        }
        
        // Send message
        async function sendMessage() {
            const message = input.value.trim();
            if (!message || !conversationId) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show typing
            showTyping();
            
            try {
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        session_id: conversationId
                    })
                });
                
                hideTyping();
                
                const data = await response.json();
                addMessage(data.response, 'bot');
            } catch (error) {
                hideTyping();
                console.error('Failed to send message:', error);
                addMessage('Sorry, I couldn\'t send your message. Please try again.', 'bot');
            }
        }
        
        // Event listeners
        bubble.addEventListener('click', toggleChat);
        closeBtn.addEventListener('click', toggleChat);
        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
})();