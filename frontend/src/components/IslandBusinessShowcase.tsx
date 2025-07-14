import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  IconButton,
  Grid,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Agriculture as AgricultureIcon,
  Restaurant as RestaurantIcon,
  BeachAccess as TourismIcon,
  Store as RetailIcon,
  NavigateNext as NextIcon,
  NavigateBefore as PrevIcon,
} from '@mui/icons-material';
import styled from 'styled-components';
import { hawaiianColors } from '../styles/hawaiian-theme';

const ShowcaseContainer = styled(Box)`
  margin: 24px 0;
`;

const IslandCard = styled(Card)`
  background: white;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  min-height: 300px;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, 
      ${hawaiianColors.oceanDeep} 0%, 
      ${hawaiianColors.oceanMid} 50%, 
      ${hawaiianColors.oceanLight} 100%
    );
  }
`;

const IslandHeader = styled(Box)`
  padding: 20px;
  background: linear-gradient(135deg, ${hawaiianColors.sand} 0%, white 100%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
`;

const MetricCard = styled(Box)`
  background: ${hawaiianColors.sand};
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 129, 167, 0.15);
  }
`;

const IndustryChip = styled(Chip)`
  margin: 4px;
`;

const NavigationButton = styled(IconButton)`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
  
  &:hover {
    background: ${hawaiianColors.sand};
  }
`;

interface IslandData {
  name: string;
  nickname: string;
  emoji: string;
  keyMetrics: {
    population: string;
    annualVisitors: string;
    topIndustries: string[];
  };
  opportunities: string[];
  challenges: string[];
  successStory: {
    type: string;
    result: string;
    icon: React.ReactElement;
  };
}

const islandData: IslandData[] = [
  {
    name: 'Oahu',
    nickname: 'The Gathering Place',
    emoji: '🏙️',
    keyMetrics: {
      population: '1M+',
      annualVisitors: '5M+',
      topIndustries: ['Tourism', 'Military', 'Tech', 'Healthcare'],
    },
    opportunities: [
      'Large local customer base',
      'Tech hub development',
      'Government contracts',
      'International connections',
    ],
    challenges: [
      'High competition',
      'Expensive real estate',
      'Traffic congestion',
    ],
    successStory: {
      type: 'Tourism Analytics',
      result: '35% increase in off-season bookings',
      icon: <TourismIcon />,
    },
  },
  {
    name: 'Maui',
    nickname: 'The Valley Isle',
    emoji: '🌺',
    keyMetrics: {
      population: '167K',
      annualVisitors: '3M',
      topIndustries: ['Tourism', 'Agriculture', 'Real Estate'],
    },
    opportunities: [
      'Luxury tourism market',
      'Wedding industry',
      'Agritourism potential',
      'Renewable energy',
    ],
    challenges: [
      'Seasonal fluctuations',
      'Water restrictions',
      'Limited workforce',
    ],
    successStory: {
      type: 'Restaurant AI',
      result: '30% reduction in food waste',
      icon: <RestaurantIcon />,
    },
  },
  {
    name: 'Big Island',
    nickname: 'The Orchid Isle',
    emoji: '🌋',
    keyMetrics: {
      population: '200K',
      annualVisitors: '1.8M',
      topIndustries: ['Agriculture', 'Tourism', 'Astronomy', 'Energy'],
    },
    opportunities: [
      'Agricultural innovation',
      'Volcano tourism',
      'Astronomy sector',
      'Geothermal energy',
    ],
    challenges: [
      'Geographic size',
      'Infrastructure gaps',
      'Natural disasters',
    ],
    successStory: {
      type: 'Agriculture Tech',
      result: '25% increase in crop yield',
      icon: <AgricultureIcon />,
    },
  },
  {
    name: 'Kauai',
    nickname: 'The Garden Isle',
    emoji: '🌿',
    keyMetrics: {
      population: '73K',
      annualVisitors: '1.3M',
      topIndustries: ['Tourism', 'Agriculture', 'Film'],
    },
    opportunities: [
      'Eco-tourism leadership',
      'Film production',
      'Sustainable agriculture',
      'Wellness retreats',
    ],
    challenges: [
      'Small market size',
      'Development limits',
      'Single-road access',
    ],
    successStory: {
      type: 'Retail AI',
      result: '40% increase in local sales',
      icon: <RetailIcon />,
    },
  },
];

const IslandBusinessShowcase: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % islandData.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + islandData.length) % islandData.length);
  };

  const currentIsland = islandData[currentIndex];

  return (
    <ShowcaseContainer>
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Hawaiian Island Business Insights
      </Typography>

      <Box position="relative">
        <NavigationButton
          onClick={handlePrev}
          sx={{ left: -20 }}
          size="small"
        >
          <PrevIcon />
        </NavigationButton>

        <NavigationButton
          onClick={handleNext}
          sx={{ right: -20 }}
          size="small"
        >
          <NextIcon />
        </NavigationButton>

        <AnimatePresence mode="wait">
          <motion.div
            key={currentIsland.name}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            <IslandCard>
              <IslandHeader>
                <Box display="flex" alignItems="center" gap={2}>
                  <Typography variant="h4">{currentIsland.emoji}</Typography>
                  <Box>
                    <Typography variant="h5" sx={{ fontWeight: 600 }}>
                      {currentIsland.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {currentIsland.nickname}
                    </Typography>
                  </Box>
                </Box>
              </IslandHeader>

              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Box display="flex" gap={2} flexWrap="wrap" mb={2}>
                      <MetricCard>
                        <Typography variant="h6" color="primary">
                          {currentIsland.keyMetrics.population}
                        </Typography>
                        <Typography variant="caption">Population</Typography>
                      </MetricCard>
                      <MetricCard>
                        <Typography variant="h6" color="primary">
                          {currentIsland.keyMetrics.annualVisitors}
                        </Typography>
                        <Typography variant="caption">Annual Visitors</Typography>
                      </MetricCard>
                    </Box>
                  </Grid>

                  <Grid item xs={12}>
                    <Typography variant="subtitle2" gutterBottom>
                      Top Industries
                    </Typography>
                    <Box>
                      {currentIsland.keyMetrics.topIndustries.map((industry) => (
                        <IndustryChip
                          key={industry}
                          label={industry}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                      🎯 Opportunities
                    </Typography>
                    <ul style={{ margin: 0, paddingLeft: 20 }}>
                      {currentIsland.opportunities.map((opp, index) => (
                        <li key={index}>
                          <Typography variant="body2">{opp}</Typography>
                        </li>
                      ))}
                    </ul>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                      🌊 Challenges
                    </Typography>
                    <ul style={{ margin: 0, paddingLeft: 20 }}>
                      {currentIsland.challenges.map((challenge, index) => (
                        <li key={index}>
                          <Typography variant="body2">{challenge}</Typography>
                        </li>
                      ))}
                    </ul>
                  </Grid>

                  <Grid item xs={12}>
                    <Box
                      sx={{
                        mt: 2,
                        p: 2,
                        bgcolor: hawaiianColors.sand,
                        borderRadius: 2,
                      }}
                    >
                      <Typography variant="subtitle2" gutterBottom>
                        🌟 Success Story
                      </Typography>
                      <Box display="flex" alignItems="center" gap={2}>
                        {currentIsland.successStory.icon}
                        <Box>
                          <Typography variant="body2" fontWeight={500}>
                            {currentIsland.successStory.type}
                          </Typography>
                          <Typography variant="body2" color="success.main">
                            {currentIsland.successStory.result}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </IslandCard>
          </motion.div>
        </AnimatePresence>
      </Box>

      <Box display="flex" justifyContent="center" gap={1} mt={2}>
        {islandData.map((_, index) => (
          <Box
            key={index}
            sx={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              bgcolor: index === currentIndex ? 'primary.main' : 'grey.300',
              transition: 'all 0.3s ease',
              cursor: 'pointer',
            }}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </Box>
    </ShowcaseContainer>
  );
};

export default IslandBusinessShowcase;