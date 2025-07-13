/**
 * Hawaiian LeniLani Chatbot Widget Embed Script
 * Add this script to any website to include the chatbot
 */
(function() {
  // Configuration
  const CHATBOT_URL = 'https://chat.lenilani.com'; // Update this to your deployed URL
  const WIDGET_ID = 'hawaiian-lenilani-chatbot';
  
  // Create widget container
  const widgetContainer = document.createElement('div');
  widgetContainer.id = WIDGET_ID;
  widgetContainer.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    width: 400px;
    height: 600px;
    max-width: 90vw;
    max-height: 80vh;
  `;
  
  // Create iframe
  const iframe = document.createElement('iframe');
  iframe.src = CHATBOT_URL + '?embed=true';
  iframe.style.cssText = `
    width: 100%;
    height: 100%;
    border: none;
    border-radius: 16px;
    box-shadow: 0 5px 40px rgba(0,0,0,0.16);
  `;
  iframe.allow = 'microphone; camera';
  
  // Mobile responsive
  if (window.innerWidth < 768) {
    widgetContainer.style.width = '100%';
    widgetContainer.style.height = '100%';
    widgetContainer.style.bottom = '0';
    widgetContainer.style.right = '0';
    widgetContainer.style.maxWidth = '100%';
    widgetContainer.style.maxHeight = '100%';
    iframe.style.borderRadius = '0';
  }
  
  // Add iframe to container
  widgetContainer.appendChild(iframe);
  
  // Add to page when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      document.body.appendChild(widgetContainer);
    });
  } else {
    document.body.appendChild(widgetContainer);
  }
  
  // Listen for messages from iframe
  window.addEventListener('message', function(event) {
    if (event.origin !== CHATBOT_URL) return;
    
    // Handle widget commands
    if (event.data.command === 'close') {
      widgetContainer.style.display = 'none';
    } else if (event.data.command === 'open') {
      widgetContainer.style.display = 'block';
    }
  });
})();