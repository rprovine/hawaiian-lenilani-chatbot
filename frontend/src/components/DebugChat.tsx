import React, { useState } from 'react';
import { Button, TextField, Box, Typography, Paper } from '@mui/material';
import { chatService } from '../services/chatService';

const DebugChat: React.FC = () => {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    setError('');
    setResponse(null);
    
    try {
      const result = await chatService.sendMessage(
        message,
        'debug-session-' + Date.now(),
        'debug-user'
      );
      setResponse(result);
    } catch (err: any) {
      setError(err.message || 'Unknown error occurred');
      console.error('Chat error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>Debug Chat Interface</Typography>
      
      <Box sx={{ mb: 2 }}>
        <TextField
          fullWidth
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          variant="outlined"
        />
      </Box>
      
      <Button 
        variant="contained" 
        onClick={handleSend}
        disabled={loading || !message.trim()}
      >
        {loading ? 'Sending...' : 'Send Message'}
      </Button>
      
      {error && (
        <Paper sx={{ p: 2, mt: 2, bgcolor: 'error.light' }}>
          <Typography color="error">Error: {error}</Typography>
        </Paper>
      )}
      
      {response && (
        <Paper sx={{ p: 2, mt: 2 }}>
          <Typography variant="h6">Response:</Typography>
          <Typography>{response.response}</Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="caption">
              Raw Response: {JSON.stringify(response, null, 2)}
            </Typography>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default DebugChat;