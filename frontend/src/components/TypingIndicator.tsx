import React from 'react';
import { motion } from 'framer-motion';
import { Box } from '@mui/material';
import styled from 'styled-components';
import { hawaiianColors } from '../styles/hawaiian-theme';

const IndicatorContainer = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
`;

const BubbleContainer = styled.div`
  background: white;
  padding: 12px 16px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 4px;
`;

const Dot = styled(motion.div)`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${hawaiianColors.oceanMid};
`;

const TypingIndicator: React.FC = () => {
  const dotVariants = {
    initial: { y: 0 },
    animate: {
      y: [-3, 3, -3],
      transition: {
        duration: 0.8,
        repeat: Infinity,
        ease: 'easeInOut',
      },
    },
  };

  return (
    <IndicatorContainer
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ duration: 0.2 }}
    >
      <Box width={32} />
      <BubbleContainer>
        <Dot
          variants={dotVariants}
          initial="initial"
          animate="animate"
          style={{ animationDelay: '0s' }}
        />
        <Dot
          variants={dotVariants}
          initial="initial"
          animate="animate"
          style={{ animationDelay: '0.2s' }}
        />
        <Dot
          variants={dotVariants}
          initial="initial"
          animate="animate"
          style={{ animationDelay: '0.4s' }}
        />
      </BubbleContainer>
    </IndicatorContainer>
  );
};

export default TypingIndicator;