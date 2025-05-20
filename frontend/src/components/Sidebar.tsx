import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  Divider,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  ShoppingCart as OrdersIcon,
  People as CustomersIcon,
  Inventory as InventoryIcon,
  Category as ProductsIcon,
  Psychology as AIIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Produkte', icon: <ProductsIcon />, path: '/products' },
  { text: 'Bestellungen', icon: <OrdersIcon />, path: '/orders' },
  { text: 'Kunden', icon: <CustomersIcon />, path: '/customers' },
  { text: 'Lager', icon: <InventoryIcon />, path: '/inventory' },
  { text: 'KI-Analyse', icon: <AIIcon />, path: '/ai' },
];

const Sidebar: React.FC = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarOpen } = useSelector((state: RootState) => state.ui);

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={sidebarOpen}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          marginTop: '64px', // Header height
          height: 'calc(100% - 64px)',
        },
      }}
    >
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => navigate(item.path)}
            selected={location.pathname === item.path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: theme.palette.primary.light,
                '&:hover': {
                  backgroundColor: theme.palette.primary.light,
                },
                '& .MuiListItemIcon-root': {
                  color: theme.palette.primary.main,
                },
                '& .MuiListItemText-primary': {
                  color: theme.palette.primary.main,
                },
              },
            }}
          >
            <ListItemIcon
              sx={{
                color: location.pathname === item.path
                  ? theme.palette.primary.main
                  : 'inherit',
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar; 