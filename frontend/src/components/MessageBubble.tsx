import React from 'react';
import { motion } from 'framer-motion';
import { Avatar, Typography, Box } from '@mui/material';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import { format } from 'date-fns';
import { ChatMessage } from '../types/chat';
import { hawaiianColors } from '../styles/hawaiian-theme';

interface MessageBubbleProps {
  message: ChatMessage;
  isFirst: boolean;
  isLast: boolean;
}

const BubbleContainer = styled(motion.div)<{ sender: 'user' | 'bot'; isLast: boolean }>`
  display: flex;
  margin-bottom: ${props => props.isLast ? '16px' : '4px'};
  justify-content: ${props => props.sender === 'user' ? 'flex-end' : 'flex-start'};
  align-items: flex-end;
  gap: 8px;
`;

const Bubble = styled.div<{ sender: 'user' | 'bot'; isFirst: boolean; isLast: boolean }>`
  max-width: 70%;
  padding: 12px 16px;
  background: ${props => 
    props.sender === 'user' 
      ? `linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%)`
      : 'white'
  };
  color: ${props => props.sender === 'user' ? 'white' : hawaiianColors.lavaRock};
  border-radius: ${props => {
    if (props.sender === 'user') {
      return props.isFirst && props.isLast ? '20px'
        : props.isFirst ? '20px 20px 4px 20px'
        : props.isLast ? '20px 4px 20px 20px'
        : '20px 4px 4px 20px';
    } else {
      return props.isFirst && props.isLast ? '20px'
        : props.isFirst ? '20px 20px 20px 4px'
        : props.isLast ? '4px 20px 20px 20px'
        : '4px 20px 20px 4px';
    }
  }};
  box-shadow: ${props => 
    props.sender === 'bot' ? '0 2px 8px rgba(0, 0, 0, 0.1)' : 'none'
  };
  
  p {
    margin: 0;
    line-height: 1.5;
  }
  
  a {
    color: ${props => props.sender === 'user' ? 'white' : hawaiianColors.oceanDeep};
    text-decoration: underline;
  }
  
  ul, ol {
    margin: 8px 0;
    padding-left: 20px;
  }
  
  li {
    margin: 4px 0;
  }
`;

const BotAvatar = styled(Avatar)`
  background: linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%);
  width: 32px;
  height: 32px;
  font-size: 16px;
`;

const Timestamp = styled(Typography)`
  font-size: 0.75rem;
  color: ${hawaiianColors.volcanic};
  opacity: 0.6;
  margin-top: 4px;
`;

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isFirst, isLast }) => {
  const showAvatar = message.sender === 'bot' && isLast;
  const showTimestamp = isLast;

  const bubbleVariants = {
    initial: { 
      opacity: 0, 
      y: 10,
      scale: 0.8 
    },
    animate: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: 0.3,
        ease: 'easeOut'
      }
    },
  };

  return (
    <Box>
      <BubbleContainer
        sender={message.sender}
        isLast={isLast}
        variants={bubbleVariants}
        initial="initial"
        animate="animate"
      >
        {showAvatar && (
          <BotAvatar>🌺</BotAvatar>
        )}
        {message.sender === 'bot' && !showAvatar && (
          <Box width={32} />
        )}
        
        <Bubble 
          sender={message.sender} 
          isFirst={isFirst}
          isLast={isLast}
        >
          <ReactMarkdown>
            {message.text}
          </ReactMarkdown>
        </Bubble>
      </BubbleContainer>
      
      {showTimestamp && (
        <Box 
          display="flex" 
          justifyContent={message.sender === 'user' ? 'flex-end' : 'flex-start'}
          px={message.sender === 'bot' ? '40px' : '0'}
        >
          <Timestamp variant="caption">
            {format(message.timestamp, 'h:mm a')}
          </Timestamp>
        </Box>
      )}
    </Box>
  );
};

export default MessageBubble;