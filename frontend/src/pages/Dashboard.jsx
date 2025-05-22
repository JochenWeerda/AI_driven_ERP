import React, { useState } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Tabs, 
  Tab,
  Divider,
  AppBar,
  Toolbar,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  FormControl,
  InputLabel,
  Select
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import TseStatus from '../components/TSE/TseStatus';
import WaagenStatus from '../components/Waage/WaagenStatus';
import WaagenMessungen from '../components/Waage/WaagenMessungen';
import ArtikelKatalog from '../components/Artikel/ArtikelKatalog';

const Dashboard = () => {
  const [tabValue, setTabValue] = useState(0);
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedKunde, setSelectedKunde] = useState('');

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleKundeChange = (event) => {
    setSelectedKunde(event.target.value);
  };

  const renderTabContent = () => {
    switch (tabValue) {
      case 0: // Übersicht
        return (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TseStatus />
            </Grid>
            <Grid item xs={12} md={6}>
              <WaagenStatus />
            </Grid>
            <Grid item xs={12}>
              <Paper sx={{ p: 2, mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Willkommen beim AI-gesteuerten ERP-System
                </Typography>
                <Typography variant="body1">
                  Dieses System bietet umfassende Funktionen für die Verwaltung Ihres Unternehmens, 
                  unterstützt durch künstliche Intelligenz für optimierte Prozesse und Entscheidungshilfen.
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="body2">
                  Über die Tabs oben können Sie zu den verschiedenen Funktionsbereichen navigieren.
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        );
      case 1: // Artikel
        return <ArtikelKatalog kundenNr={selectedKunde} />;
      case 2: // Waagen
        return <WaagenMessungen />;
      default:
        return (
          <Box textAlign="center" py={4}>
            <Typography variant="h6">Inhalt wird geladen...</Typography>
          </Box>
        );
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={handleMenuOpen}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI-gesteuertes ERP-System
          </Typography>
          <IconButton color="inherit">
            <AccountCircleIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>Einstellungen</MenuItem>
        <MenuItem onClick={handleMenuClose}>Hilfe</MenuItem>
        <MenuItem onClick={handleMenuClose}>Abmelden</MenuItem>
      </Menu>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box sx={{ mb: 3 }}>
          <Paper>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              variant="fullWidth"
              aria-label="Haupt-Navigation"
            >
              <Tab label="Übersicht" />
              <Tab label="Artikel" />
              <Tab label="Waagen" />
            </Tabs>
          </Paper>
        </Box>

        {tabValue === 1 && (
          <Box sx={{ mb: 3 }}>
            <FormControl fullWidth>
              <InputLabel id="kunde-select-label">Kunde auswählen (für Empfehlungen)</InputLabel>
              <Select
                labelId="kunde-select-label"
                value={selectedKunde}
                label="Kunde auswählen (für Empfehlungen)"
                onChange={handleKundeChange}
              >
                <MenuItem value="">
                  <em>Kein Kunde ausgewählt</em>
                </MenuItem>
                <MenuItem value="K00001">Kunde 00001</MenuItem>
                <MenuItem value="K00002">Kunde 00002</MenuItem>
                <MenuItem value="K00003">Kunde 00003</MenuItem>
              </Select>
            </FormControl>
          </Box>
        )}

        {renderTabContent()}
      </Container>
    </Box>
  );
};

export default Dashboard; 