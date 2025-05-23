import { ThemeMode, ExtendedThemeOptions } from '../themeTypes';

// Standard-Theme
export const getDefaultTheme = (mode: ThemeMode): ExtendedThemeOptions => {
  // Basis-Farben für Standard-Theme
  const primaryMain = mode === 'dark' ? '#90caf9' : '#1976d2';
  const primaryLight = mode === 'dark' ? '#e3f2fd' : '#42a5f5';
  const primaryDark = mode === 'dark' ? '#42a5f5' : '#1565c0';
  
  const secondaryMain = mode === 'dark' ? '#f48fb1' : '#dc004e';
  const secondaryLight = mode === 'dark' ? '#fce4ec' : '#ff4081';
  const secondaryDark = mode === 'dark' ? '#ff4081' : '#c51162';

  // Anpassung für Hochkontrast-Modus
  if (mode === 'high-contrast') {
    return {
      palette: {
        mode: 'dark',
        primary: {
          main: '#FFFFFF',
          light: '#FFFFFF',
          dark: '#CCCCCC',
          contrastText: '#000000',
        },
        secondary: {
          main: '#FFFF00',
          light: '#FFFF33',
          dark: '#CCCC00',
          contrastText: '#000000',
        },
        background: {
          default: '#000000',
          paper: '#333333',
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#FFFF00',
        },
        divider: '#FFFFFF',
      },
      typography: {
        fontFamily: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          'Arial',
          'sans-serif',
        ].join(','),
        h1: {
          fontSize: '2.5rem',
          fontWeight: 600,
        },
        h2: {
          fontSize: '2rem',
          fontWeight: 600,
        },
        h3: {
          fontSize: '1.75rem',
          fontWeight: 600,
        },
        h4: {
          fontSize: '1.5rem',
          fontWeight: 600,
        },
        h5: {
          fontSize: '1.25rem',
          fontWeight: 600,
        },
        h6: {
          fontSize: '1rem',
          fontWeight: 600,
        },
        subtitle1: {
          fontSize: '1rem',
          fontWeight: 400,
          color: '#FFFF00',
        },
        body1: {
          fontSize: '1rem',
        },
        button: {
          textTransform: 'uppercase',
          fontWeight: 500,
        },
      },
      components: {
        MuiButton: {
          styleOverrides: {
            root: {
              borderRadius: 4,
              padding: '6px 16px',
              fontWeight: 500,
              border: '2px solid white',
            },
            contained: {
              boxShadow: 'none',
            },
          },
        },
        MuiCard: {
          styleOverrides: {
            root: {
              borderRadius: 4,
              border: '2px solid white',
            },
          },
        },
      },
    };
  }

  // Light und Dark Mode für Standard-Theme
  return {
    palette: {
      mode: mode === 'dark' ? 'dark' : 'light',
      primary: {
        main: primaryMain,
        light: primaryLight,
        dark: primaryDark,
      },
      secondary: {
        main: secondaryMain,
        light: secondaryLight,
        dark: secondaryDark,
      },
      success: {
        main: mode === 'dark' ? '#4caf50' : '#2e7d32',
        light: mode === 'dark' ? '#81c784' : '#4caf50',
        dark: mode === 'dark' ? '#2e7d32' : '#1b5e20',
      },
      info: {
        main: mode === 'dark' ? '#29b6f6' : '#0288d1',
        light: mode === 'dark' ? '#4fc3f7' : '#29b6f6',
        dark: mode === 'dark' ? '#0288d1' : '#01579b',
      },
      warning: {
        main: mode === 'dark' ? '#ffc107' : '#ed6c02',
        light: mode === 'dark' ? '#ffcd38' : '#ff9800',
        dark: mode === 'dark' ? '#e69500' : '#e65100',
      },
      error: {
        main: mode === 'dark' ? '#f44336' : '#d32f2f',
        light: mode === 'dark' ? '#e57373' : '#ef5350',
        dark: mode === 'dark' ? '#d32f2f' : '#c62828',
      },
      background: {
        default: mode === 'dark' ? '#121212' : '#f5f5f5',
        paper: mode === 'dark' ? '#1e1e1e' : '#ffffff',
      },
      text: {
        primary: mode === 'dark' ? '#ffffff' : '#212121',
        secondary: mode === 'dark' ? '#b0b0b0' : '#757575',
      },
      divider: mode === 'dark' ? '#424242' : '#e0e0e0',
      customBackground: {
        header: mode === 'dark' ? '#1a1a1a' : '#ffffff',
        sidebar: mode === 'dark' ? '#2c2c2c' : '#f5f5f5',
        card: mode === 'dark' ? '#2c2c2c' : '#ffffff',
        hover: mode === 'dark' ? '#3c3c3c' : '#f0f0f0',
      },
    },
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        'Arial',
        'sans-serif',
      ].join(','),
      h1: {
        fontSize: '2.5rem',
        fontWeight: 600,
      },
      h2: {
        fontSize: '2rem',
        fontWeight: 600,
      },
      h3: {
        fontSize: '1.75rem',
        fontWeight: 600,
      },
      h4: {
        fontSize: '1.5rem',
        fontWeight: 600,
      },
      h5: {
        fontSize: '1.25rem',
        fontWeight: 600,
      },
      h6: {
        fontSize: '1rem',
        fontWeight: 600,
      },
      subtitle1: {
        fontSize: '1rem',
        fontWeight: 400,
        color: mode === 'dark' ? '#b0b0b0' : '#757575',
      },
      body1: {
        fontSize: '1rem',
      },
      button: {
        textTransform: 'uppercase',
        fontWeight: 500,
      },
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 4,
            padding: '6px 16px',
            fontWeight: 500,
          },
          contained: {
            boxShadow: '0px 3px 1px -2px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 1px 5px 0px rgba(0,0,0,0.12)',
          },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: 4,
            boxShadow: '0px 2px 1px -1px rgba(0,0,0,0.2), 0px 1px 1px 0px rgba(0,0,0,0.14), 0px 1px 3px 0px rgba(0,0,0,0.12)',
          },
        },
      },
      MuiAppBar: {
        styleOverrides: {
          root: {
            boxShadow: '0px 2px 4px -1px rgba(0,0,0,0.2), 0px 4px 5px 0px rgba(0,0,0,0.14), 0px 1px 10px 0px rgba(0,0,0,0.12)',
          },
        },
      },
      MuiTable: {
        styleOverrides: {
          root: {
            borderCollapse: 'collapse',
          },
        },
      },
      MuiTableCell: {
        styleOverrides: {
          head: {
            backgroundColor: mode === 'dark' ? '#2c2c2c' : '#f5f5f5',
            fontWeight: 600,
          },
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            borderRadius: 16,
          },
        },
      },
      MuiTab: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 500,
            fontSize: '0.875rem',
          },
        },
      },
    },
    shape: {
      borderRadius: 4,
    },
    spacing: 8,
    visualDensity: 0, // Standard-Dichte
  };
}; 