import React from 'react';
import { Snackbar, Alert } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { hideNotification } from '../store/slices/uiSlice';

const Notification: React.FC = () => {
  const dispatch = useDispatch();
  const { notifications } = useSelector((state: RootState) => state.ui);

  const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    dispatch(hideNotification());
  };

  return (
    <Snackbar
      open={notifications.open}
      autoHideDuration={6000}
      onClose={handleClose}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    >
      <Alert
        onClose={handleClose}
        severity={notifications.severity}
        variant="filled"
        sx={{ width: '100%' }}
      >
        {notifications.message}
      </Alert>
    </Snackbar>
  );
};

export default Notification; 