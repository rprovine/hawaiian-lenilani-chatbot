import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Typography, Box, Paper } from '@mui/material';
import styled from 'styled-components';
import { formatInTimeZone } from 'date-fns-tz';
import { hawaiianColors } from '../styles/hawaiian-theme';

const GreetingContainer = styled(Paper)`
  padding: 24px;
  background: linear-gradient(135deg, ${hawaiianColors.sand} 0%, ${hawaiianColors.warmSand} 100%);
  border-radius: 16px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
`;

const GreetingEmoji = styled(motion.div)`
  font-size: 48px;
  position: absolute;
  top: -10px;
  right: 20px;
  opacity: 0.3;
`;

const TimeDisplay = styled(Typography)`
  color: ${hawaiianColors.volcanic};
  font-weight: 500;
  margin-bottom: 8px;
`;

const CulturalMessage = styled(Typography)`
  color: ${hawaiianColors.lavaRock};
  font-style: italic;
  margin-top: 12px;
  font-size: 0.9rem;
`;

interface GreetingData {
  hawaiian: string;
  english: string;
  pidgin: string;
  emoji: string;
  culturalNote: string;
}

const CulturalGreeting: React.FC = () => {
  const [greeting, setGreeting] = useState<GreetingData | null>(null);
  const [hawaiiTime, setHawaiiTime] = useState<string>('');

  useEffect(() => {
    const updateGreeting = () => {
      const now = new Date();
      const hawaiiTimeStr = formatInTimeZone(now, 'Pacific/Honolulu', 'h:mm a zzz');
      setHawaiiTime(hawaiiTimeStr);

      const hour = parseInt(formatInTimeZone(now, 'Pacific/Honolulu', 'H'));

      let greetingData: GreetingData;

      if (hour >= 5 && hour < 10) {
        greetingData = {
          hawaiian: 'Aloha kakahiaka',
          english: 'Good morning',
          pidgin: 'Howzit! Early bird, yeah?',
          emoji: '🌅',
          culturalNote: 'Morning is sacred time in Hawaiian culture - time for gratitude and new beginnings',
        };
      } else if (hour >= 10 && hour < 14) {
        greetingData = {
          hawaiian: 'Aloha awakea',
          english: 'Good afternoon',
          pidgin: 'Howzit! Hot one today!',
          emoji: '☀️',
          culturalNote: 'Midday is for productivity and connection with ohana',
        };
      } else if (hour >= 14 && hour < 17) {
        greetingData = {
          hawaiian: 'Aloha ʻauinalā',
          english: 'Good late afternoon',
          pidgin: 'Almost pau hana time!',
          emoji: '🌴',
          culturalNote: 'Afternoon brings the cooling trade winds and time to prepare for evening',
        };
      } else if (hour >= 17 && hour < 20) {
        greetingData = {
          hawaiian: 'Aloha ahiahi',
          english: 'Good evening',
          pidgin: 'Pau hana! Time for relax!',
          emoji: '🌅',
          culturalNote: 'Evening is time for family, reflection, and watching the sunset',
        };
      } else {
        greetingData = {
          hawaiian: 'Aloha pō',
          english: 'Good night',
          pidgin: 'Late night hustle, respect!',
          emoji: '🌙',
          culturalNote: 'Night brings peace and preparation for tomorrow\'s opportunities',
        };
      }

      setGreeting(greetingData);
    };

    updateGreeting();
    const interval = setInterval(updateGreeting, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  if (!greeting) return null;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        key={greeting.hawaiian}
        style={{
          padding: '24px',
          background: `linear-gradient(135deg, ${hawaiianColors.sand} 0%, ${hawaiianColors.warmSand} 100%)`,
          borderRadius: '16px',
          border: `2px solid ${hawaiianColors.oceanLight}`,
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden',
          marginBottom: '24px'
        }}
      >
        <GreetingEmoji
          initial={{ rotate: -180, opacity: 0 }}
          animate={{ rotate: 0, opacity: 0.3 }}
          transition={{ duration: 0.5, type: 'spring' }}
        >
          {greeting.emoji}
        </GreetingEmoji>

        <TimeDisplay variant="caption">
          {hawaiiTime}
        </TimeDisplay>

        <Box>
          <Typography variant="h5" sx={{ color: hawaiianColors.oceanDeep, fontWeight: 600 }}>
            {greeting.hawaiian}
          </Typography>
          <Typography variant="body2" sx={{ color: hawaiianColors.volcanic, mt: 0.5 }}>
            {greeting.english} • {greeting.pidgin}
          </Typography>
        </Box>

        <CulturalMessage>
          {greeting.culturalNote}
        </CulturalMessage>
      </motion.div>
    </AnimatePresence>
  );
};

export default CulturalGreeting;