import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { hawaiianTheme } from './styles/hawaiian-theme';
import HawaiianChatWidget from './components/HawaiianChatWidget';
import './styles/App.css';

function App() {
  return (
    <ThemeProvider theme={hawaiianTheme}>
      <CssBaseline />
      <div className="App">
        <header className="App-header">
          <h1>🌺 LeniLani AI Chatbot Demo</h1>
          <p>Hawaiian Business AI Assistant with Authentic Cultural Integration</p>
        </header>
        <main className="App-main">
          <div className="demo-container">
            <h2>Try Our Chatbot!</h2>
            <p>Click the chat button in the bottom right to start talking story about your Hawaiian business needs.</p>
            
            <div className="features">
              <div className="feature">
                <span className="emoji">🌴</span>
                <h3>Island-Specific Intelligence</h3>
                <p>Understanding of each island's unique business environment</p>
              </div>
              <div className="feature">
                <span className="emoji">🤙</span>
                <h3>Authentic Pidgin</h3>
                <p>Natural Hawaiian Pidgin English communication</p>
              </div>
              <div className="feature">
                <span className="emoji">🌊</span>
                <h3>Cultural Values</h3>
                <p>Aloha, Ohana, and Malama 'Aina in every interaction</p>
              </div>
              <div className="feature">
                <span className="emoji">🎯</span>
                <h3>Local Solutions</h3>
                <p>Technology solutions designed for Hawaiian businesses</p>
              </div>
            </div>
          </div>
        </main>
        <HawaiianChatWidget />
      </div>
    </ThemeProvider>
  );
}

export default App;