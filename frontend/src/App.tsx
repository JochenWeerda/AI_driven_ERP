import React, { useState } from 'react';
import { CssBaseline, Box, Typography, Button, ButtonGroup, Select, MenuItem, FormControl, InputLabel, Card, CardContent } from '@mui/material';
import { ThemeProvider, useThemeSystem } from './themes/ThemeProvider';
import { ThemeVariant } from './themes/themeTypes';

// Dummy-Store für Theme-Tests
const DummyStore = {
  getState: () => ({ 
    ui: { darkMode: false }
  }),
  subscribe: () => () => {},
  dispatch: () => {}
};

// Kontext für Redux-Provider mit korrektem Typ
const ReactReduxContext = React.createContext<{store: any} | null>(null);
const Provider = ({ store, children }: { store: any, children: React.ReactNode }) => (
  <ReactReduxContext.Provider value={{ store }}>
    {children}
  </ReactReduxContext.Provider>
);

// Theme-Demo-Komponente
const ThemeDemo = () => {
  const { currentThemeConfig, toggleMode, setVariant, updateTheme } = useThemeSystem();
  
  // Lokaler State für die Formularwerte
  const [formValues, setFormValues] = useState({
    fontSize: currentThemeConfig.parameters?.fontSize || 'medium',
    spacing: currentThemeConfig.parameters?.spacing || 'normal',
    borderRadius: currentThemeConfig.parameters?.borderRadius || 'small'
  });
  
  // Handler für die Parameteränderungen
  const handleParameterChange = (paramName: string, value: any) => {
    setFormValues(prev => ({ ...prev, [paramName]: value }));
    updateTheme({ 
      parameters: { 
        ...currentThemeConfig.parameters,
        [paramName]: value 
      } 
    });
  };
  
  return (
    <Box sx={{ padding: 3, marginTop: 8 }}>
      <Typography variant="h4" gutterBottom>
        Theme-Modus: {currentThemeConfig.mode === 'dark' ? 'Dunkel' : 
                     currentThemeConfig.mode === 'high-contrast' ? 'Hoher Kontrast' : 'Hell'}
      </Typography>
      
      <Button 
        variant="contained" 
        color="primary"
        onClick={toggleMode}
        sx={{ my: 2 }}
      >
        {currentThemeConfig.mode === 'dark' ? 'Hellmodus aktivieren' : 'Dunkelmodus aktivieren'}
      </Button>
      
      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        Verfügbare Theme-Varianten:
      </Typography>
      
      <ButtonGroup variant="contained" color="primary" sx={{ mb: 4 }}>
        {(['odoo', 'default', 'modern', 'classic'] as ThemeVariant[]).map(variant => (
          <Button 
            key={variant}
            onClick={() => setVariant(variant)}
            variant={currentThemeConfig.variant === variant ? "contained" : "outlined"}
            sx={{ 
              bgcolor: currentThemeConfig.variant === variant ? 'primary.main' : 'transparent',
              color: currentThemeConfig.variant === variant ? 'white' : 'primary.main',
            }}
          >
            {variant.charAt(0).toUpperCase() + variant.slice(1)}
          </Button>
        ))}
      </ButtonGroup>
      
      <Typography variant="h5" sx={{ mb: 2 }}>
        Anpassbare Parameter:
      </Typography>
      
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400, mb: 4 }}>
        <FormControl>
          <InputLabel>Schriftgröße</InputLabel>
          <Select
            value={formValues.fontSize}
            label="Schriftgröße"
            onChange={(e) => handleParameterChange('fontSize', e.target.value)}
          >
            <MenuItem value="small">Klein</MenuItem>
            <MenuItem value="medium">Mittel</MenuItem>
            <MenuItem value="large">Groß</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl>
          <InputLabel>Abstände</InputLabel>
          <Select
            value={formValues.spacing}
            label="Abstände"
            onChange={(e) => handleParameterChange('spacing', e.target.value)}
          >
            <MenuItem value="compact">Kompakt</MenuItem>
            <MenuItem value="normal">Normal</MenuItem>
            <MenuItem value="comfortable">Komfortabel</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl>
          <InputLabel>Eckenradius</InputLabel>
          <Select
            value={formValues.borderRadius}
            label="Eckenradius"
            onChange={(e) => handleParameterChange('borderRadius', e.target.value)}
          >
            <MenuItem value="none">Keine Abrundung</MenuItem>
            <MenuItem value="small">Leicht abgerundet</MenuItem>
            <MenuItem value="medium">Mittel abgerundet</MenuItem>
            <MenuItem value="large">Stark abgerundet</MenuItem>
          </Select>
        </FormControl>
      </Box>
      
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Beispiel für Theme-Anwendung
          </Typography>
          <Typography paragraph>
            Dieser Bereich zeigt die Anwendung des aktuellen Themes mit verschiedenen UI-Elementen.
            Aktuelle Konfiguration:
          </Typography>
          <Box component="pre" sx={{ bgcolor: 'background.paper', p: 2, borderRadius: 1 }}>
            {JSON.stringify(currentThemeConfig, null, 2)}
          </Box>
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button variant="contained" color="primary">
              Primär Button
            </Button>
            <Button variant="outlined" color="primary">
              Sekundär Button
            </Button>
            <Button variant="contained" color="secondary">
              Akzent Button
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

// Vereinfachte App ohne Redux
function App() {
  return (
    <ThemeProvider>
      <CssBaseline />
      <ThemeDemo />
    </ThemeProvider>
  );
}

export default App; 