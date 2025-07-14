import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Container, Grid, Typography, Button } from '@mui/material';
import { hawaiianTheme } from './styles/hawaiian-theme';
import HawaiianChatWidget from './components/HawaiianChatWidget';
import Logo from './components/Logo';
import './styles/App.css';

function App() {
  return (
    <ThemeProvider theme={hawaiianTheme}>
      <CssBaseline />
      <div className="App">
        <header className="App-header">
          <Container maxWidth="lg">
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
              <Logo variant="full" size="large" light />
              <Typography variant="h3" component="h1" sx={{ fontWeight: 700, textAlign: 'center' }}>
                Hawaiian Business AI Assistant
              </Typography>
              <Typography variant="h6" sx={{ opacity: 0.9, textAlign: 'center', maxWidth: 600 }}>
                Experience the power of AI-driven business consulting with authentic Hawaiian cultural values
              </Typography>
              <Button 
                variant="contained" 
                size="large"
                href="https://hawaii.lenilani.com/#cta"
                target="_blank"
                rel="noopener noreferrer"
                sx={{ 
                  mt: 2,
                  px: 4,
                  py: 1.5,
                  fontSize: '1.1rem',
                  backgroundColor: '#F4A261',
                  '&:hover': {
                    backgroundColor: '#E76F51'
                  }
                }}
              >
                Start Talking Story 🤙
              </Button>
            </Box>
          </Container>
        </header>
        <main className="App-main">
          <Container maxWidth="lg">
            <Box className="hero-section" sx={{ mb: 6 }}>
              <Typography variant="h4" component="h2" sx={{ textAlign: 'center', mb: 2, color: '#264653' }}>
                Why Choose LeniLani Consulting?
              </Typography>
              <Typography variant="body1" sx={{ textAlign: 'center', mb: 4, color: '#2D3436', maxWidth: 800, mx: 'auto' }}>
                Our AI assistant understands the unique challenges and opportunities of running a business in Hawaii. 
                From navigating local regulations to building community relationships, we're here to help you succeed.
              </Typography>
            </Box>
            
            <div className="features">
              <div className="feature">
                <span className="emoji">🌴</span>
                <h3>Island-Specific Intelligence</h3>
                <p>Deep understanding of each island's unique business environment and local markets</p>
              </div>
              <div className="feature">
                <span className="emoji">🤙</span>
                <h3>Authentic Communication</h3>
                <p>Natural Hawaiian Pidgin English that resonates with local customers and partners</p>
              </div>
              <div className="feature">
                <span className="emoji">🌺</span>
                <h3>Cultural Values</h3>
                <p>Aloha, Ohana, and Malama 'Aina integrated into every business recommendation</p>
              </div>
              <div className="feature">
                <span className="emoji">🎯</span>
                <h3>Local Solutions</h3>
                <p>Technology and strategies specifically designed for Hawaiian business success</p>
              </div>
            </div>
            
            <Box className="testimonial-section" sx={{ mt: 8, mb: 6 }}>
              <Typography variant="h4" component="h2" sx={{ textAlign: 'center', mb: 4, color: '#264653' }}>
                Trusted by Hawaiian Businesses
              </Typography>
              <Grid container spacing={4}>
                <Grid item xs={12} md={4}>
                  <Box className="testimonial">
                    <Typography variant="body1" sx={{ fontStyle: 'italic', mb: 2 }}>
                      "LeniLani Consulting helped me understand local regulations and connect with the right suppliers on Maui. 
                      The cultural insights were invaluable!"
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#666' }}>
                      - Keoni, Maui Restaurant Owner
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box className="testimonial">
                    <Typography variant="body1" sx={{ fontStyle: 'italic', mb: 2 }}>
                      "Finally, an AI that gets island time and local business practices. 
                      It's like having a kama'aina business consultant available 24/7."
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#666' }}>
                      - Leilani, Big Island Tour Operator
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box className="testimonial">
                    <Typography variant="body1" sx={{ fontStyle: 'italic', mb: 2 }}>
                      "The pidgin communication style makes it so easy to explain what I need. 
                      It's not just translation - it truly understands local context."
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#666' }}>
                      - Uncle Kimo, Oahu Retail Shop
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </Box>
            
            <Box className="cta-section" sx={{ textAlign: 'center', py: 6 }}>
              <Typography variant="h4" component="h2" sx={{ mb: 2, color: '#264653' }}>
                Ready to Grow Your Hawaiian Business?
              </Typography>
              <Typography variant="body1" sx={{ mb: 3, color: '#2D3436' }}>
                Start a conversation with LeniLani Consulting today and discover how we can help you thrive
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button 
                  variant="contained" 
                  size="large"
                  href="https://hawaii.lenilani.com/#cta"
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ 
                    px: 4,
                    py: 1.5,
                    backgroundColor: '#F4A261',
                    '&:hover': {
                      backgroundColor: '#E76F51'
                    }
                  }}
                >
                  Contact Now 💬
                </Button>
                <Button 
                  variant="outlined" 
                  size="large"
                  href="mailto:reno@lenilani.com"
                  sx={{ 
                    px: 4,
                    py: 1.5,
                    borderColor: '#F4A261',
                    color: '#F4A261',
                    '&:hover': {
                      borderColor: '#E76F51',
                      backgroundColor: 'rgba(244, 162, 97, 0.1)'
                    }
                  }}
                >
                  Contact Reno 📧
                </Button>
              </Box>
              <Typography variant="body2" sx={{ mt: 3, color: '#666' }}>
                Questions? Call Reno at 808-766-1164
              </Typography>
            </Box>
          </Container>
        </main>
        <HawaiianChatWidget />
      </div>
    </ThemeProvider>
  );
}

export default App;