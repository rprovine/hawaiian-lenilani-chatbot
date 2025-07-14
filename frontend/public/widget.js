/**
 * Hawaiian LeniLani Chatbot Widget Loader
 * Copyright 2024 LeniLani Consulting
 * Contact: reno@lenilani.com | 808-766-1164
 */
(function() {
  'use strict';
  
  // Prevent multiple loads
  if (window.LeniLaniChatbot) return;
  
  // Default configuration
  const config = window.LeniLaniConfig || {};
  const defaults = {
    position: 'bottom-right',
    primaryColor: '#F4A261',
    buttonSize: 60,
    greeting: 'Aloha! 🌺 Need help with your Hawaiian business?',
    apiUrl: window.location.origin,
    embedUrl: window.location.origin
  };
  
  // Merge configurations
  const settings = Object.assign({}, defaults, config);
  
  // Create chat button
  const chatButton = document.createElement('div');
  chatButton.id = 'lenilani-chat-button';
  chatButton.innerHTML = `
    <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
      <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 3 .97 4.29L1 23l6.71-1.97C9 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10s-4.48-10-10-10zm0 18c-1.41 0-2.73-.36-3.88-.99l-.28-.15-2.89.85.85-2.89-.15-.28C5.36 14.73 5 13.41 5 12c0-3.86 3.14-7 7-7s7 3.14 7 7-3.14 7-7 7z"/>
      <circle cx="8.5" cy="12" r="1.5"/>
      <circle cx="12" cy="12" r="1.5"/>
      <circle cx="15.5" cy="12" r="1.5"/>
    </svg>
  `;
  
  // Style the button
  const buttonStyles = `
    #lenilani-chat-button {
      position: fixed;
      ${settings.position === 'bottom-left' ? 'left: 20px;' : 'right: 20px;'}
      bottom: 20px;
      width: ${settings.buttonSize}px;
      height: ${settings.buttonSize}px;
      background-color: ${settings.primaryColor};
      border-radius: 50%;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
      z-index: 9998;
    }
    
    #lenilani-chat-button:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    #lenilani-chat-widget {
      position: fixed;
      ${settings.position === 'bottom-left' ? 'left: 20px;' : 'right: 20px;'}
      bottom: 90px;
      width: 380px;
      height: 600px;
      max-width: calc(100vw - 40px);
      max-height: calc(100vh - 110px);
      background: white;
      border-radius: 16px;
      box-shadow: 0 5px 40px rgba(0,0,0,0.16);
      display: none;
      flex-direction: column;
      z-index: 9999;
      overflow: hidden;
    }
    
    #lenilani-chat-widget.active {
      display: flex;
    }
    
    #lenilani-chat-header {
      background: linear-gradient(135deg, #F4A261 0%, #E76F51 100%);
      color: white;
      padding: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    #lenilani-chat-header h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
    }
    
    #lenilani-chat-close {
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
      transition: background 0.3s;
    }
    
    #lenilani-chat-close:hover {
      background: rgba(255,255,255,0.2);
    }
    
    #lenilani-chat-iframe {
      flex: 1;
      width: 100%;
      border: none;
    }
    
    @media (max-width: 768px) {
      #lenilani-chat-widget {
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height: 100%;
        max-width: 100%;
        max-height: 100%;
        border-radius: 0;
      }
      
      #lenilani-chat-button {
        bottom: 10px;
        ${settings.position === 'bottom-left' ? 'left: 10px;' : 'right: 10px;'}
      }
    }
  `;
  
  // Add styles to page
  const styleSheet = document.createElement('style');
  styleSheet.textContent = buttonStyles;
  document.head.appendChild(styleSheet);
  
  // Create widget container
  const widget = document.createElement('div');
  widget.id = 'lenilani-chat-widget';
  widget.innerHTML = `
    <div id="lenilani-chat-header">
      <div>
        <h3>LeniLani AI Assistant</h3>
        <p style="margin: 0; font-size: 14px; opacity: 0.9;">Hawaiian Business Consulting</p>
      </div>
      <button id="lenilani-chat-close" aria-label="Close chat">×</button>
    </div>
    <iframe 
      id="lenilani-chat-iframe"
      src="${settings.embedUrl}?embed=true&apiUrl=${encodeURIComponent(settings.apiUrl)}"
      title="LeniLani Hawaiian Business Chatbot"
      allow="microphone; camera">
    </iframe>
  `;
  
  // Add elements to page
  document.body.appendChild(chatButton);
  document.body.appendChild(widget);
  
  // Toggle widget
  let isOpen = false;
  
  function toggleWidget() {
    isOpen = !isOpen;
    widget.classList.toggle('active', isOpen);
    
    // Track event
    if (window.gtag) {
      window.gtag('event', isOpen ? 'chatbot_opened' : 'chatbot_closed', {
        'event_category': 'engagement',
        'event_label': 'Hawaiian LeniLani Chatbot'
      });
    }
  }
  
  // Event listeners
  chatButton.addEventListener('click', toggleWidget);
  document.getElementById('lenilani-chat-close').addEventListener('click', toggleWidget);
  
  // Listen for messages from iframe
  window.addEventListener('message', function(event) {
    if (event.origin !== settings.embedUrl) return;
    
    if (event.data.command === 'close') {
      isOpen = false;
      widget.classList.remove('active');
    }
  });
  
  // Show greeting on first visit
  if (!localStorage.getItem('lenilani_visited')) {
    localStorage.setItem('lenilani_visited', 'true');
    setTimeout(() => {
      const greeting = document.createElement('div');
      greeting.style.cssText = `
        position: fixed;
        ${settings.position === 'bottom-left' ? 'left: 90px;' : 'right: 90px;'}
        bottom: 30px;
        background: white;
        padding: 12px 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-size: 14px;
        color: #333;
        z-index: 9997;
        animation: slideIn 0.5s ease;
        max-width: 250px;
      `;
      greeting.textContent = settings.greeting;
      document.body.appendChild(greeting);
      
      setTimeout(() => {
        greeting.style.opacity = '0';
        greeting.style.transition = 'opacity 0.5s';
        setTimeout(() => greeting.remove(), 500);
      }, 5000);
    }, 3000);
  }
  
  // Public API
  window.LeniLaniChatbot = {
    open: () => {
      if (!isOpen) toggleWidget();
    },
    close: () => {
      if (isOpen) toggleWidget();
    },
    toggle: toggleWidget
  };
})();