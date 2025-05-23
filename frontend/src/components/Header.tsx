import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  MenuItem,
  Avatar,
  Box,
  useTheme,
  Badge,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  SelectChangeEvent,
  TextField,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
  Palette as PaletteIcon,
} from '@mui/icons-material';
import { useThemeSystem } from '../themes/ThemeProvider';
import { ThemeConfig, ThemeMode, ThemeVariant } from '../themes/index';
import { LLMService } from '../services/llmService';

const Header: React.FC = () => {
  const theme = useTheme();
  // Lokaler State statt Redux
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [user, setUser] = useState({ fullName: 'Demo User' });
  
  const { updateTheme, currentThemeConfig } = useThemeSystem();
  
  // State für Menüs
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationsAnchorEl, setNotificationsAnchorEl] = useState<null | HTMLElement>(null);
  
  // State für Theme-Dialog
  const [themeDialogOpen, setThemeDialogOpen] = useState(false);
  const [themeFormData, setThemeFormData] = useState<Partial<ThemeConfig>>({
    mode: currentThemeConfig.mode,
    variant: currentThemeConfig.variant,
    parameters: { ...currentThemeConfig.parameters }
  });
  
  // Theme-Dialog öffnen
  const handleOpenThemeDialog = () => {
    setThemeFormData({
      mode: currentThemeConfig.mode,
      variant: currentThemeConfig.variant,
      parameters: { ...currentThemeConfig.parameters }
    });
    setThemeDialogOpen(true);
  };
  
  // Theme-Dialog schließen
  const handleCloseThemeDialog = () => {
    setThemeDialogOpen(false);
  };
  
  // Theme-Änderungen anwenden
  const handleApplyThemeChanges = () => {
    updateTheme(themeFormData);
    setThemeDialogOpen(false);
  };
  
  // Änderungen im Theme-Formular verarbeiten
  const handleThemeModeChange = (event: SelectChangeEvent<string>) => {
    setThemeFormData({
      ...themeFormData,
      mode: event.target.value as ThemeMode
    });
  };
  
  const handleThemeVariantChange = (event: SelectChangeEvent<string>) => {
    setThemeFormData({
      ...themeFormData,
      variant: event.target.value as ThemeVariant
    });
  };
  
  const handleParameterChange = (paramName: string, value: string) => {
    setThemeFormData({
      ...themeFormData,
      parameters: {
        ...themeFormData.parameters,
        [paramName]: value
      }
    });
  };

  // Benutzermenü öffnen
  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  // Benachrichtigungsmenü öffnen
  const handleNotificationsMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationsAnchorEl(event.currentTarget);
  };

  // Menüs schließen
  const handleMenuClose = () => {
    setAnchorEl(null);
    setNotificationsAnchorEl(null);
  };

  // Dark Mode umschalten
  const handleToggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  // Sidebar umschalten
  const handleToggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };

  const notificationsMenuId = 'notifications-menu';
  const renderNotificationsMenu = (
    <Menu
      anchorEl={notificationsAnchorEl}
      id={notificationsMenuId}
      keepMounted
      open={Boolean(notificationsAnchorEl)}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={handleMenuClose}>Keine neuen Benachrichtigungen</MenuItem>
    </Menu>
  );

  const profileMenuId = 'primary-search-account-menu';
  const renderProfileMenu = (
    <Menu
      anchorEl={anchorEl}
      id={profileMenuId}
      keepMounted
      open={Boolean(anchorEl)}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={handleMenuClose}>Profil</MenuItem>
      <MenuItem onClick={handleMenuClose}>Mein Konto</MenuItem>
      <MenuItem onClick={handleMenuClose}>Abmelden</MenuItem>
    </Menu>
  );

  // Theme-Dialog-Komponente
  const renderThemeDialog = (
    <Dialog open={themeDialogOpen} onClose={handleCloseThemeDialog}>
      <DialogTitle>Theme-Einstellungen</DialogTitle>
      <DialogContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
          <FormControl fullWidth>
            <InputLabel id="theme-mode-label">Modus</InputLabel>
            <Select
              labelId="theme-mode-label"
              value={themeFormData.mode || 'light'}
              label="Modus"
              onChange={handleThemeModeChange}
            >
              <MenuItem value="light">Hell</MenuItem>
              <MenuItem value="dark">Dunkel</MenuItem>
              <MenuItem value="high-contrast">Hoher Kontrast</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth>
            <InputLabel id="theme-variant-label">Variante</InputLabel>
            <Select
              labelId="theme-variant-label"
              value={themeFormData.variant || 'odoo'}
              label="Variante"
              onChange={handleThemeVariantChange}
            >
              <MenuItem value="odoo">Odoo</MenuItem>
              <MenuItem value="default">Standard</MenuItem>
              <MenuItem value="modern">Modern</MenuItem>
              <MenuItem value="classic">Klassisch</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth>
            <InputLabel id="font-size-label">Schriftgröße</InputLabel>
            <Select
              labelId="font-size-label"
              value={themeFormData.parameters?.fontSize || 'medium'}
              label="Schriftgröße"
              onChange={(e) => handleParameterChange('fontSize', e.target.value)}
            >
              <MenuItem value="small">Klein</MenuItem>
              <MenuItem value="medium">Mittel</MenuItem>
              <MenuItem value="large">Groß</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth>
            <InputLabel id="spacing-label">Abstände</InputLabel>
            <Select
              labelId="spacing-label"
              value={themeFormData.parameters?.spacing || 'normal'}
              label="Abstände"
              onChange={(e) => handleParameterChange('spacing', e.target.value)}
            >
              <MenuItem value="compact">Kompakt</MenuItem>
              <MenuItem value="normal">Normal</MenuItem>
              <MenuItem value="comfortable">Komfortabel</MenuItem>
            </Select>
          </FormControl>
          
          <FormControl fullWidth>
            <InputLabel id="border-radius-label">Eckenradius</InputLabel>
            <Select
              labelId="border-radius-label"
              value={themeFormData.parameters?.borderRadius || 'small'}
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
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCloseThemeDialog}>Abbrechen</Button>
        <Button onClick={handleApplyThemeChanges} variant="contained" color="primary">
          Anwenden
        </Button>
      </DialogActions>
    </Dialog>
  );

  return (
    <>
      <AppBar
        position="fixed"
        sx={{
          zIndex: theme.zIndex.drawer + 1,
          transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleToggleSidebar}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            AI-Driven ERP
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <IconButton 
              color="inherit"
              onClick={handleToggleDarkMode}
              aria-label={darkMode ? 'Hellmodus aktivieren' : 'Dunkelmodus aktivieren'}
            >
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
            
            <IconButton
              color="inherit"
              onClick={handleOpenThemeDialog}
              aria-label="Theme-Einstellungen"
            >
              <PaletteIcon />
            </IconButton>
            
            <IconButton
              color="inherit"
              aria-label="show notifications"
              aria-controls={notificationsMenuId}
              onClick={handleNotificationsMenuOpen}
            >
              <Badge badgeContent={0} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
            
            <IconButton
              edge="end"
              aria-label="account of current user"
              aria-controls={profileMenuId}
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              {user?.fullName ? (
                <Avatar sx={{ width: 32, height: 32 }}>
                  {user.fullName.charAt(0)}
                </Avatar>
              ) : (
                <AccountCircle />
              )}
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
      {renderProfileMenu}
      {renderNotificationsMenu}
      {renderThemeDialog}
    </>
  );
};

export default Header; 