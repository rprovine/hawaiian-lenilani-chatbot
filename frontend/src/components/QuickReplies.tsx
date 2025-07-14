import React from 'react';
import { motion } from 'framer-motion';
import { Chip, Box } from '@mui/material';
import styled from 'styled-components';
import { QuickReply } from '../types/chat';
import { hawaiianColors } from '../styles/hawaiian-theme';

interface QuickRepliesProps {
  replies: QuickReply[];
  onSelect: (text: string) => void;
}

const Container = styled(motion.div)`
  padding: 12px 16px;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  overflow-x: auto;
  
  &::-webkit-scrollbar {
    height: 4px;
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${hawaiianColors.oceanLight};
    border-radius: 2px;
  }
`;

const QuickReplyChip = styled(Chip)`
  cursor: pointer;
  transition: all 0.3s ease;
  background: ${hawaiianColors.sand};
  border-color: ${hawaiianColors.oceanMid};
  color: ${hawaiianColors.lavaRock};
  
  &:hover {
    background: ${hawaiianColors.oceanLight};
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 129, 167, 0.2);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const QuickReplies: React.FC<QuickRepliesProps> = ({ replies, onSelect }) => {
  const containerVariants = {
    initial: { opacity: 0, y: 10 },
    animate: { 
      opacity: 1, 
      y: 0,
      transition: {
        duration: 0.3,
        staggerChildren: 0.05,
      }
    },
    exit: { opacity: 0, y: 10 },
  };

  const chipVariants = {
    initial: { opacity: 0, scale: 0.8 },
    animate: { 
      opacity: 1, 
      scale: 1,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 20,
      }
    },
  };

  return (
    <Container
      variants={containerVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {replies.map((reply, index) => (
        <motion.div key={index} variants={chipVariants}>
          <QuickReplyChip
            label={reply.text}
            variant="outlined"
            onClick={() => onSelect(reply.text)}
            size="medium"
          />
        </motion.div>
      ))}
    </Container>
  );
};

export default QuickReplies;