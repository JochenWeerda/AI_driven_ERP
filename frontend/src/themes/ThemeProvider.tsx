import React, { createContext, useContext, useState, useEffect } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { getCurrentTheme, updateThemeConfig } from './themeService';
import { ThemeConfig, ThemeMode, ThemeVariant } from './themeTypes';

// Context für das Theme-System
interface ThemeContextType {
  updateTheme: (config: Partial<ThemeConfig>) => void;
  currentThemeConfig: ThemeConfig;
  toggleMode: () => void;
  setVariant: (variant: ThemeVariant) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Hook für den Zugriff auf das Theme-System
export const useThemeSystem = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeSystem muss innerhalb eines ThemeProviders verwendet werden');
  }
  return context;
};

// ThemeProvider-Komponente
export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Lokaler State für das aktuelle Theme
  const [darkMode, setDarkMode] = useState(false);
  const [theme, setTheme] = useState(getCurrentTheme());
  const [themeConfig, setThemeConfig] = useState<ThemeConfig>({
    mode: darkMode ? 'dark' : 'light',
    variant: 'odoo',
    parameters: {
      fontSize: 'medium',
      spacing: 'normal',
      borderRadius: 'small',
    }
  });

  // Bei Änderungen des Dark Mode-Status das Theme aktualisieren
  useEffect(() => {
    const newMode: ThemeMode = darkMode ? 'dark' : 'light';
    if (themeConfig.mode !== newMode) {
      const newConfig = { ...themeConfig, mode: newMode };
      setThemeConfig(newConfig);
      setTheme(updateThemeConfig(newConfig));
    }
  }, [darkMode, themeConfig]);

  // Funktion zum Umschalten des Modus
  const toggleMode = () => {
    setDarkMode(prev => !prev);
  };

  // Funktion zum Ändern der Theme-Variante
  const setVariant = (variant: ThemeVariant) => {
    updateTheme({ variant });
  };

  // Funktion zum Aktualisieren des Themes
  const updateTheme = (config: Partial<ThemeConfig>) => {
    const newConfig = { ...themeConfig, ...config };
    setThemeConfig(newConfig);
    setTheme(updateThemeConfig(newConfig));
  };

  // Theme-Context-Wert
  const contextValue: ThemeContextType = {
    updateTheme,
    currentThemeConfig: themeConfig,
    toggleMode,
    setVariant,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
}; 