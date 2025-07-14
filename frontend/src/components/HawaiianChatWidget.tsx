import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Paper,
  IconButton,
  TextField,
  Typography,
  Chip,
  Avatar,
  CircularProgress,
  Fade,
  Box,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Close as CloseIcon,
  Send as SendIcon,
  WbSunny as SunIcon,
  NightsStay as MoonIcon,
} from '@mui/icons-material';
import styled from 'styled-components';
import { format } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';
import { v4 as uuidv4 } from 'uuid';
import { ChatMessage, QuickReply, ChatState } from '../types/chat';
import { chatService } from '../services/chatService';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import QuickReplies from './QuickReplies';
import { hawaiianColors } from '../styles/hawaiian-theme';
import Logo from './Logo';

const WidgetContainer = styled.div`
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
`;

const ChatButton = styled(motion.div)`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 129, 167, 0.3);
  
  &:hover {
    box-shadow: 0 6px 30px rgba(0, 129, 167, 0.4);
  }
`;

const ChatWindow = styled(motion.div)`
  width: 380px;
  height: 600px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 129, 167, 0.2);
  background: white;
  display: flex;
  flex-direction: column;
  
  @media (max-width: 420px) {
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 0;
  }
`;

const ChatHeader = styled.div<{ timeOfDay: string }>`
  background: ${props => 
    props.timeOfDay === 'night' 
      ? `linear-gradient(135deg, #2C3E50 0%, #34495E 100%)`
      : props.timeOfDay === 'evening'
      ? `linear-gradient(135deg, ${hawaiianColors.sunset} 0%, ${hawaiianColors.sunsetPink} 100%)`
      : `linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%)`
  };
  color: white;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: ${hawaiianColors.sand};
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${hawaiianColors.oceanLight};
    border-radius: 3px;
  }
`;

const InputContainer = styled.div`
  padding: 16px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
`;

const StyledTextField = styled(TextField)`
  .MuiOutlinedInput-root {
    border-radius: 25px;
    background: ${hawaiianColors.sand};
    
    &:hover fieldset {
      border-color: ${hawaiianColors.oceanMid};
    }
    
    &.Mui-focused fieldset {
      border-color: ${hawaiianColors.oceanDeep};
    }
  }
`;

const WelcomeMessage = styled(motion.div)`
  text-align: center;
  padding: 40px 20px;
  
  h3 {
    color: ${hawaiianColors.lavaRock};
    margin-bottom: 16px;
  }
  
  p {
    color: ${hawaiianColors.volcanic};
    margin-bottom: 24px;
  }
`;

const BusinessTypeChip = styled(Chip)`
  margin: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 129, 167, 0.2);
  }
`;

const HawaiianChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [chatState, setChatState] = useState<ChatState>({
    sessionId: uuidv4(),
    userId: localStorage.getItem('lenilani_user_id') || uuidv4(),
    context: {},
  });
  const [quickReplies, setQuickReplies] = useState<QuickReply[]>([]);
  const [timeOfDay, setTimeOfDay] = useState<string>('day');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Save user ID for return visits
    localStorage.setItem('lenilani_user_id', chatState.userId);
    
    // Update time of day
    const updateTimeOfDay = () => {
      const hawaiiTime = formatInTimeZone(new Date(), 'Pacific/Honolulu', 'HH');
      const hour = parseInt(hawaiiTime);
      
      if (hour >= 5 && hour < 10) {
        setTimeOfDay('morning');
      } else if (hour >= 10 && hour < 17) {
        setTimeOfDay('day');
      } else if (hour >= 17 && hour < 20) {
        setTimeOfDay('evening');
      } else {
        setTimeOfDay('night');
      }
    };
    
    updateTimeOfDay();
    const interval = setInterval(updateTimeOfDay, 60000); // Update every minute
    
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleOpen = () => {
    setIsOpen(true);
    
    // Don't auto-send message - let user choose from menu or type message
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const sendMessage = async (text: string, isInitial: boolean = false) => {
    if (!text.trim() && !isInitial) return;

    const userMessage: ChatMessage = {
      id: uuidv4(),
      text: text,
      sender: 'user',
      timestamp: new Date(),
    };

    if (!isInitial) {
      setMessages(prev => [...prev, userMessage]);
      setInputValue('');
      setQuickReplies([]);
    }

    setIsTyping(true);

    try {
      const response = await chatService.sendMessage(
        text,
        chatState.sessionId,
        chatState.userId,
        chatState.context
      );

      const botMessage: ChatMessage = {
        id: uuidv4(),
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        metadata: response.metadata,
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Update context
      if (response.metadata?.intent) {
        setChatState(prev => ({
          ...prev,
          context: {
            ...prev.context,
            lastIntent: response.metadata?.intent,
          },
        }));
      }

      // Set quick replies if available
      if (response.quick_replies && response.quick_replies.length > 0) {
        setQuickReplies(response.quick_replies.map(text => ({
          text,
          action: () => sendMessage(text),
        })));
      }
    } catch (error: any) {
      console.error('Error sending message:', error);
      console.error('Error details:', error.response?.data || error.message);
      
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        text: "Ho brah, sorry! Having some technical difficulties. Try again in a moment yeah? 🌺",
        sender: 'bot',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickReply = (text: string) => {
    sendMessage(text);
  };

  const handleBusinessTypeSelect = (businessType: string) => {
    setChatState(prev => ({
      ...prev,
      context: {
        ...prev.context,
        businessType,
      },
    }));
    sendMessage(`I have a ${businessType} business`);
  };

  const getTimeIcon = () => {
    if (timeOfDay === 'night' || timeOfDay === 'evening') {
      return <MoonIcon />;
    }
    return <SunIcon />;
  };

  const getHawaiianTime = () => {
    return formatInTimeZone(new Date(), 'Pacific/Honolulu', 'h:mm a');
  };

  return (
    <WidgetContainer>
      <AnimatePresence>
        {!isOpen && (
          <ChatButton
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleOpen}
          >
            <ChatIcon sx={{ color: 'white', fontSize: 28 }} />
          </ChatButton>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {isOpen && (
          <ChatWindow
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.3 }}
          >
            <ChatHeader timeOfDay={timeOfDay}>
              <Box display="flex" alignItems="center" gap={2}>
                <Logo variant="icon" size="small" light />
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Leni Begonia
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.9 }}>
                    LeniLani Consulting • {getHawaiianTime()} HST {getTimeIcon()}
                  </Typography>
                </Box>
              </Box>
              <IconButton onClick={handleClose} sx={{ color: 'white' }}>
                <CloseIcon />
              </IconButton>
            </ChatHeader>

            <MessagesContainer>
              {messages.length === 0 && (
                <WelcomeMessage
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <h3>Aloha! I'm Leni Begonia 🌺</h3>
                  <p>I'm here to help your Hawaiian business thrive with AI technology!</p>
                  <Typography variant="body2" gutterBottom>
                    What kind of business do you have?
                  </Typography>
                  <Box>
                    {['Tourism', 'Restaurant', 'Agriculture', 'Retail', 'Other'].map((type) => (
                      <BusinessTypeChip
                        key={type}
                        label={type}
                        color="primary"
                        variant="outlined"
                        onClick={() => handleBusinessTypeSelect(type.toLowerCase())}
                      />
                    ))}
                  </Box>
                </WelcomeMessage>
              )}
              
              {messages.map((message, index) => (
                <MessageBubble
                  key={message.id}
                  message={message}
                  isFirst={index === 0 || messages[index - 1].sender !== message.sender}
                  isLast={index === messages.length - 1 || messages[index + 1]?.sender !== message.sender}
                />
              ))}
              
              {isTyping && <TypingIndicator />}
              
              <div ref={messagesEndRef} />
            </MessagesContainer>

            {quickReplies.length > 0 && (
              <QuickReplies
                replies={quickReplies}
                onSelect={handleQuickReply}
              />
            )}

            <InputContainer>
              <Box display="flex" gap={1} alignItems="flex-end">
                <StyledTextField
                  fullWidth
                  variant="outlined"
                  placeholder="Type your message..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage(inputValue);
                    }
                  }}
                  inputRef={inputRef}
                  size="small"
                  multiline
                  maxRows={3}
                />
                <IconButton
                  color="primary"
                  onClick={() => sendMessage(inputValue)}
                  disabled={!inputValue.trim()}
                  sx={{
                    bgcolor: hawaiianColors.oceanDeep,
                    color: 'white',
                    '&:hover': {
                      bgcolor: hawaiianColors.oceanMid,
                    },
                    '&:disabled': {
                      bgcolor: 'rgba(0, 0, 0, 0.12)',
                    },
                  }}
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </InputContainer>
          </ChatWindow>
        )}
      </AnimatePresence>
    </WidgetContainer>
  );
};

export default HawaiianChatWidget;