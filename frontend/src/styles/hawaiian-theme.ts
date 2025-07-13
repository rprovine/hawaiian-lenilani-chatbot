import { createTheme } from '@mui/material/styles';

// Hawaiian-inspired color palette
const hawaiianColors = {
  // Ocean blues
  oceanDeep: '#0081A7',
  oceanMid: '#00AFB9',
  oceanLight: '#5DCED0',
  
  // Sand and earth tones
  sand: '#FDFCDC',
  warmSand: '#FED9B7',
  coral: '#F07167',
  
  // Nature greens
  palmGreen: '#2A9D8F',
  leafGreen: '#52B788',
  
  // Sunset colors
  sunset: '#F4A261',
  sunsetPink: '#E76F51',
  
  // Neutrals
  lavaRock: '#264653',
  volcanic: '#2D3436',
  white: '#FFFFFF',
  
  // Status colors
  success: '#52B788',
  warning: '#F4A261',
  error: '#E76F51',
  info: '#00AFB9'
};

export const hawaiianTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: hawaiianColors.oceanDeep,
      light: hawaiianColors.oceanLight,
      dark: hawaiianColors.lavaRock,
      contrastText: hawaiianColors.white,
    },
    secondary: {
      main: hawaiianColors.palmGreen,
      light: hawaiianColors.leafGreen,
      dark: hawaiianColors.lavaRock,
      contrastText: hawaiianColors.white,
    },
    background: {
      default: hawaiianColors.sand,
      paper: hawaiianColors.white,
    },
    text: {
      primary: hawaiianColors.lavaRock,
      secondary: hawaiianColors.volcanic,
    },
    success: {
      main: hawaiianColors.success,
    },
    warning: {
      main: hawaiianColors.warning,
    },
    error: {
      main: hawaiianColors.error,
    },
    info: {
      main: hawaiianColors.info,
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica Neue", Arial, sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          padding: '10px 20px',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 4px 12px rgba(0, 129, 167, 0.3)',
          },
        },
        containedPrimary: {
          background: `linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 100%)`,
          '&:hover': {
            background: `linear-gradient(135deg, ${hawaiianColors.oceanMid} 0%, ${hawaiianColors.oceanDeep} 100%)`,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 4px 20px rgba(0, 129, 167, 0.1)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
        },
      },
    },
  },
});

// Additional Hawaiian styling utilities
export const hawaiianStyles = {
  gradients: {
    ocean: `linear-gradient(135deg, ${hawaiianColors.oceanDeep} 0%, ${hawaiianColors.oceanMid} 50%, ${hawaiianColors.oceanLight} 100%)`,
    sunset: `linear-gradient(135deg, ${hawaiianColors.sunset} 0%, ${hawaiianColors.sunsetPink} 50%, ${hawaiianColors.coral} 100%)`,
    tropical: `linear-gradient(135deg, ${hawaiianColors.palmGreen} 0%, ${hawaiianColors.leafGreen} 100%)`,
    sand: `linear-gradient(135deg, ${hawaiianColors.sand} 0%, ${hawaiianColors.warmSand} 100%)`,
  },
  shadows: {
    soft: '0 2px 8px rgba(38, 70, 83, 0.1)',
    medium: '0 4px 20px rgba(0, 129, 167, 0.15)',
    strong: '0 8px 32px rgba(0, 129, 167, 0.2)',
  },
  animations: {
    wave: `
      @keyframes wave {
        0% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-5px) translateY(-5px); }
        50% { transform: translateX(0) translateY(-10px); }
        75% { transform: translateX(5px) translateY(-5px); }
        100% { transform: translateX(0) translateY(0); }
      }
    `,
    float: `
      @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
      }
    `,
  },
};

export { hawaiianColors };
export default hawaiianTheme;