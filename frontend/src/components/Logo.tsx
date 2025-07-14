import React from 'react';
import { styled } from '@mui/material/styles';
import { Box, Typography } from '@mui/material';

interface LogoProps {
  variant?: 'full' | 'icon';
  size?: 'small' | 'medium' | 'large';
  light?: boolean;
}

const LogoContainer = styled(Box)<{ size: string }>(({ size }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: size === 'small' ? '8px' : size === 'medium' ? '12px' : '16px',
  cursor: 'pointer',
  userSelect: 'none',
}));

const LogoImage = styled('img')<{ size: string }>(({ size }) => {
  const dimensions = size === 'small' ? 40 : size === 'medium' ? 56 : 80;
  return {
    width: dimensions,
    height: dimensions,
    objectFit: 'contain',
    filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))',
  };
});

const LogoText = styled(Typography)<{ size: string; light: boolean }>(({ size, light }) => ({
  fontFamily: '"Inter", sans-serif',
  fontSize: size === 'small' ? '20px' : size === 'medium' ? '24px' : '32px',
  fontWeight: 600,
  color: light ? '#FFFFFF' : '#2D3748',
  letterSpacing: '-0.5px',
  '& .highlight': {
    color: '#F4A261',
    fontWeight: 700,
  }
}));

const Logo: React.FC<LogoProps> = ({ 
  variant = 'full', 
  size = 'medium', 
  light = false 
}) => {
  return (
    <LogoContainer size={size}>
      <LogoImage 
        src="/images/lenilani-logo.webp" 
        alt="LeniLani Consulting Logo" 
        size={size}
        onError={(e) => {
          // Fallback if logo not found
          e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxjaXJjbGUgY3g9IjUwIiBjeT0iNTAiIHI9IjQ1IiBmaWxsPSJ1cmwoI3BhaW50MF9saW5lYXIpIi8+CjxwYXRoIGQ9Ik0zNSAzNUg0NVY2NUgzNVYzNVoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik01NSAzNUg2NVY2NUg1NVYzNVoiIGZpbGw9IndoaXRlIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9InBhaW50MF9saW5lYXIiIHgxPSI1MCIgeTE9IjUiIHgyPSI1MCIgeTI9Ijk1IiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNGNEEyNjEiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjRTc2RjUxIi8+CjwvbGluZWFyR3JhZGllbnQ+CjwvZGVmcz4KPC9zdmc+';
        }}
      />
      {variant === 'full' && (
        <LogoText size={size} light={light}>
          Leni<span className="highlight">Lani</span>
        </LogoText>
      )}
    </LogoContainer>
  );
};

export default Logo;