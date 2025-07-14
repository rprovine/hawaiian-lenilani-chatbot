import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// For standalone app
const appRoot = document.getElementById('root');
if (appRoot) {
  const root = ReactDOM.createRoot(appRoot);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

// For embedded widget
const widgetRoot = document.getElementById('hawaiian-chatbot-root');
if (widgetRoot) {
  import('./components/HawaiianChatWidget').then(({ default: HawaiianChatWidget }) => {
    const root = ReactDOM.createRoot(widgetRoot);
    root.render(
      <React.StrictMode>
        <HawaiianChatWidget />
      </React.StrictMode>
    );
  });
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();