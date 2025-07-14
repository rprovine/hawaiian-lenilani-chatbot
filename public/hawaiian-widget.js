(function() {
    'use strict';

    // Configuration
    const API_URL = window.LENILANI_CHATBOT_URL || 'http://localhost:8000';
    
    // Hawaiian Theme Colors
    const hawaiianColors = {
        oceanDeep: '#0081a7',
        oceanMid: '#00afb9',
        oceanLight: '#93e1d8',
        coral: '#ff6b6b',
        sunset: '#ff9a76',
        sand: '#ffd93d',
        lava: '#c1121f',
        palm: '#52b788',
        white: '#ffffff',
        dark: '#1a1a1a'
    };
    
    // Create styles with Hawaiian theme
    const styles = `
        @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600;700&display=swap');
        
        .lenilani-chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            font-family: 'Comfortaa', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .lenilani-chat-bubble {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0, 129, 167, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
        }
        
        .lenilani-chat-bubble:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(0, 129, 167, 0.4);
        }
        
        .lenilani-chat-bubble svg {
            width: 32px;
            height: 32px;
            fill: white;
        }
        
        .lenilani-chat-bubble .notification-dot {
            position: absolute;
            top: 5px;
            right: 5px;
            width: 12px;
            height: 12px;
            background: ${hawaiianColors.coral};
            border-radius: 50%;
            border: 2px solid white;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .lenilani-chat-window {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 400px;
            height: 600px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .lenilani-chat-header {
            background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
            color: white;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }
        
        .lenilani-chat-header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .lenilani-header-content {
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 1;
        }
        
        .lenilani-logo {
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 4px;
        }
        
        .lenilani-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        
        .lenilani-chat-title {
            display: flex;
            flex-direction: column;
        }
        
        .lenilani-chat-title .name {
            font-size: 18px;
            font-weight: 600;
        }
        
        .lenilani-chat-title .status {
            font-size: 12px;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .lenilani-status-dot {
            width: 6px;
            height: 6px;
            background: #4ade80;
            border-radius: 50%;
            display: inline-block;
        }
        
        .lenilani-chat-close {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 4px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s ease;
            z-index: 1;
        }
        
        .lenilani-chat-close:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .lenilani-welcome-screen {
            flex: 1;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
        }
        
        .lenilani-welcome-message {
            background: linear-gradient(135deg, ${hawaiianColors.oceanLight}20 0%, ${hawaiianColors.sand}20 100%);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
        }
        
        .lenilani-welcome-message h3 {
            margin: 0 0 8px 0;
            color: ${hawaiianColors.oceanDeep};
            font-size: 20px;
        }
        
        .lenilani-welcome-message p {
            margin: 0;
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .lenilani-quick-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .lenilani-action-card {
            background: white;
            border: 2px solid ${hawaiianColors.oceanLight};
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .lenilani-action-card:hover {
            border-color: ${hawaiianColors.oceanMid};
            background: ${hawaiianColors.oceanLight}10;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .lenilani-action-card .icon {
            font-size: 32px;
            margin-bottom: 8px;
        }
        
        .lenilani-action-card .title {
            font-weight: 600;
            color: ${hawaiianColors.oceanDeep};
            margin-bottom: 4px;
        }
        
        .lenilani-action-card .description {
            font-size: 12px;
            color: #666;
        }
        
        .lenilani-chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: none;
            flex-direction: column;
            gap: 12px;
            background: #f8f9fa;
        }
        
        .lenilani-message {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            position: relative;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .lenilani-message.user {
            background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
        
        .lenilani-message.bot {
            background: white;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .lenilani-message .time {
            font-size: 10px;
            opacity: 0.7;
            margin-top: 4px;
        }
        
        .lenilani-chat-input-container {
            padding: 16px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .lenilani-chat-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 24px;
            outline: none;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }
        
        .lenilani-chat-input:focus {
            border-color: ${hawaiianColors.oceanMid};
        }
        
        .lenilani-chat-send {
            background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
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
        
        .lenilani-chat-send:disabled {
            opacity: 0.5;
            cursor: not-allowed;
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
            background: white;
            border-radius: 18px;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .lenilani-typing span {
            width: 8px;
            height: 8px;
            background: ${hawaiianColors.oceanMid};
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
        
        .lenilani-quick-replies {
            padding: 12px 20px;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            background: #f8f9fa;
            border-top: 1px solid #e0e0e0;
        }
        
        .lenilani-quick-reply {
            padding: 8px 16px;
            background: white;
            border: 2px solid ${hawaiianColors.oceanLight};
            border-radius: 20px;
            color: ${hawaiianColors.oceanDeep};
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .lenilani-quick-reply:hover {
            background: ${hawaiianColors.oceanLight};
            border-color: ${hawaiianColors.oceanMid};
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
                bottom: 16px;
                right: 16px;
            }
        }
    `;
    
    // Create chat HTML with Hawaiian theme
    const chatHTML = `
        <div class="lenilani-chat-widget">
            <div class="lenilani-chat-bubble" id="lenilani-bubble">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3 .97 4.29L1 23l6.71-1.97C9 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm0 18c-1.41 0-2.73-.36-3.88-.98l-.28-.14-2.92.77.79-2.89-.18-.29C4.91 14.73 4.55 13.38 4.55 12c0-4.41 3.59-8 8-8s8 3.59 8 8-3.59 8-8 8z"/>
                </svg>
                <div class="notification-dot"></div>
            </div>
            
            <div class="lenilani-chat-window" id="lenilani-window">
                <div class="lenilani-chat-header">
                    <div class="lenilani-header-content">
                        <div class="lenilani-logo">
                            <img src="${API_URL}/logo" alt="LeniLani" />
                        </div>
                        <div class="lenilani-chat-title">
                            <div class="name">LeniLani Consulting</div>
                            <div class="status">
                                <span class="lenilani-status-dot"></span>
                                Leni Begonia • Online
                            </div>
                        </div>
                    </div>
                    <button class="lenilani-chat-close" id="lenilani-close">×</button>
                </div>
                
                <div class="lenilani-welcome-screen" id="lenilani-welcome">
                    <div class="lenilani-welcome-message">
                        <h3>Aloha! Welcome to LeniLani 🌴</h3>
                        <p>I'm Leni Begonia, your AI-powered Hawaiian business consultant. How can I help your business thrive in paradise?</p>
                    </div>
                    
                    <div class="lenilani-quick-actions">
                        <div class="lenilani-action-card" data-action="services">
                            <div class="icon">💼</div>
                            <div class="title">Our Services</div>
                            <div class="description">Explore AI & tech solutions</div>
                        </div>
                        <div class="lenilani-action-card" data-action="consultation">
                            <div class="icon">🤝</div>
                            <div class="title">Free Consultation</div>
                            <div class="description">Schedule a meeting</div>
                        </div>
                        <div class="lenilani-action-card" data-action="pricing">
                            <div class="icon">💰</div>
                            <div class="title">Pricing</div>
                            <div class="description">Competitive rates</div>
                        </div>
                        <div class="lenilani-action-card" data-action="chat">
                            <div class="icon">💬</div>
                            <div class="title">Start Chat</div>
                            <div class="description">Tell me about your business</div>
                        </div>
                    </div>
                </div>
                
                <div class="lenilani-chat-messages" id="lenilani-messages"></div>
                
                <div class="lenilani-quick-replies" id="lenilani-quick-replies" style="display: none;"></div>
                
                <div class="lenilani-chat-input-container">
                    <input 
                        type="text" 
                        class="lenilani-chat-input" 
                        id="lenilani-input" 
                        placeholder="Type your message..."
                        disabled
                    />
                    <button class="lenilani-chat-send" id="lenilani-send" disabled>
                        <svg viewBox="0 0 24 24">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    // Global flag to prevent any double initialization
    if (window.__LENILANI_WIDGET_INITIALIZED) {
        console.log('Widget already initialized globally');
        return;
    }
    window.__LENILANI_WIDGET_INITIALIZED = true;
    
    // Initialize widget
    function initWidget() {
        // Prevent double initialization
        if (document.querySelector('.lenilani-chat-widget')) {
            console.log('Hawaiian widget already initialized');
            return;
        }
        
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
        const welcomeScreen = document.getElementById('lenilani-welcome');
        const quickRepliesContainer = document.getElementById('lenilani-quick-replies');
        const notificationDot = bubble.querySelector('.notification-dot');
        
        let isOpen = false;
        let conversationId = null;
        let isFirstOpen = true;
        let chatStarted = false;
        
        // Toggle chat window
        function toggleChat() {
            isOpen = !isOpen;
            window.style.display = isOpen ? 'flex' : 'none';
            
            if (isOpen && isFirstOpen) {
                isFirstOpen = false;
                if (notificationDot) {
                    notificationDot.style.display = 'none';
                }
            }
        }
        
        // Start conversation
        function startChat() {
            if (chatStarted) {
                // Chat already started, just switch screens
                console.log('Chat already started, not sending another greeting');
                welcomeScreen.style.display = 'none';
                messagesContainer.style.display = 'flex';
                input.focus();
                return;
            }
            
            console.log('Starting new chat session');
            chatStarted = true;
            conversationId = 'web-' + Date.now();
            welcomeScreen.style.display = 'none';
            messagesContainer.style.display = 'flex';
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
            
            // Send initial greeting to get conversation started - but only once!
            setTimeout(() => {
                if (messagesContainer.children.length === 0) {
                    sendMessage('Start conversation', true);
                }
            }, 100);
        }
        
        // Format time
        function formatTime() {
            return new Date().toLocaleTimeString('en-US', { 
                hour: 'numeric', 
                minute: '2-digit',
                hour12: true 
            });
        }
        
        // Add message to chat
        function addMessage(text, sender, showTime = true) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `lenilani-message ${sender}`;
            
            const textDiv = document.createElement('div');
            textDiv.textContent = text;
            messageDiv.appendChild(textDiv);
            
            if (showTime) {
                const timeDiv = document.createElement('div');
                timeDiv.className = 'time';
                timeDiv.textContent = formatTime();
                messageDiv.appendChild(timeDiv);
            }
            
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
        
        // Show quick replies
        function showQuickReplies(replies) {
            quickRepliesContainer.innerHTML = '';
            if (replies && replies.length > 0) {
                replies.forEach(reply => {
                    const button = document.createElement('button');
                    button.className = 'lenilani-quick-reply';
                    button.textContent = reply;
                    button.onclick = () => {
                        sendMessage(reply);
                        quickRepliesContainer.style.display = 'none';
                    };
                    quickRepliesContainer.appendChild(button);
                });
                quickRepliesContainer.style.display = 'flex';
            } else {
                quickRepliesContainer.style.display = 'none';
            }
        }
        
        // Send message
        async function sendMessage(message, isInitial = false) {
            if (!message && !isInitial) {
                message = input.value.trim();
                if (!message) return;
            }
            
            // Add user message (unless it's the initial greeting)
            if (!isInitial) {
                addMessage(message, 'user');
                input.value = '';
            }
            
            // Show typing
            showTyping();
            input.disabled = true;
            sendBtn.disabled = true;
            
            const requestId = 'req-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
            console.log('Sending message to API:', message, 'Session:', conversationId, 'Request ID:', requestId);
            
            try {
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-Request-ID': requestId
                    },
                    mode: 'cors',
                    body: JSON.stringify({
                        message: message,
                        session_id: conversationId,
                        metadata: { request_id: requestId }
                    })
                });
                
                hideTyping();
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
                
                const data = await response.json();
                addMessage(data.response, 'bot');
                
                // Show quick replies if available
                if (data.suggestions && data.suggestions.length > 0) {
                    showQuickReplies(data.suggestions.slice(0, 3));
                }
            } catch (error) {
                hideTyping();
                input.disabled = false;
                sendBtn.disabled = false;
                console.error('Failed to send message:', error);
                addMessage('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
            }
        }
        
        // Handle action cards
        function handleAction(action) {
            // For specific actions, send the action message instead of generic greeting
            if (action !== 'chat') {
                // Don't call startChat for specific actions
                if (chatStarted) {
                    welcomeScreen.style.display = 'none';
                    messagesContainer.style.display = 'flex';
                    input.focus();
                } else {
                    chatStarted = true;
                    conversationId = 'web-' + Date.now();
                    welcomeScreen.style.display = 'none';
                    messagesContainer.style.display = 'flex';
                    input.disabled = false;
                    sendBtn.disabled = false;
                    input.focus();
                    
                    // Send the specific action message instead of generic greeting
                    switch(action) {
                        case 'services':
                            sendMessage('Tell me about your services', true);
                            break;
                        case 'consultation':
                            sendMessage('I\'d like to schedule a consultation', true);
                            break;
                        case 'pricing':
                            sendMessage('What are your prices?', true);
                            break;
                    }
                }
            } else {
                // For generic chat, use the normal startChat
                startChat();
            }
        }
        
        // Event listeners
        bubble.addEventListener('click', toggleChat);
        closeBtn.addEventListener('click', toggleChat);
        sendBtn.addEventListener('click', () => sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Action card listeners
        document.querySelectorAll('.lenilani-action-card').forEach(card => {
            card.addEventListener('click', () => {
                const action = card.getAttribute('data-action');
                handleAction(action);
            });
        });
        
        // Auto-open after 5 seconds on first visit
        setTimeout(() => {
            if (!isOpen && isFirstOpen) {
                const visited = localStorage.getItem('lenilani-visited');
                if (!visited) {
                    localStorage.setItem('lenilani-visited', 'true');
                    toggleChat();
                }
            }
        }, 5000);
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
})();