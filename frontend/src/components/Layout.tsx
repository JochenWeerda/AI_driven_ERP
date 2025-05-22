import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CssBaseline, useTheme } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import Sidebar from './Sidebar';
import Header from './Header';
import Notification from './Notification';
import SystemStatus from './SystemStatus';

const Layout: React.FC = () => {
  const theme = useTheme();
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <CssBaseline />
      <Header />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${sidebarOpen ? 240 : 0}px)` },
          ml: { sm: `${sidebarOpen ? 240 : 0}px` },
          transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
        }}
      >
        <Box sx={{ mt: 8 }}>
          <SystemStatus />
          <Outlet />
        </Box>
      </Box>
      <Notification />
    </Box>
  );
};

export default Layout; 