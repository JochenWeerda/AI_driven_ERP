import React, { useState } from 'react';
import { Box, CssBaseline } from '@mui/material';
import Sidebar from './Sidebar';
import Header from './Header';
import Notification from './Notification';
import SystemStatus from './SystemStatus';
import { useThemeSystem } from '../themes/ThemeProvider';

const Layout: React.FC = () => {
  // Lokaler State statt Redux
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { currentThemeConfig } = useThemeSystem();
  
  // Visuellen Abstand (Dichte) aus dem Theme verwenden
  const visualDensity = currentThemeConfig.parameters?.visualDensity || 'medium';
  const paddingValue = visualDensity === 'low' ? 4 : (visualDensity === 'high' ? 2 : 3);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <CssBaseline />
      <Header />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: paddingValue,
          width: { sm: `calc(100% - ${sidebarOpen ? 240 : 0}px)` },
          ml: { sm: `${sidebarOpen ? 240 : 0}px` },
          transition: (theme) => theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
          bgcolor: 'background.default',
        }}
      >
        <Box sx={{ mt: 8 }}>
          <SystemStatus />
          {/* Outlet wird durch Unterrouten ersetzt */}
          <div className="outlet-placeholder" />
        </Box>
      </Box>
      <Notification />
    </Box>
  );
};

export default Layout; 