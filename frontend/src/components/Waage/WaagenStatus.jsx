import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Card, 
  CardHeader, 
  CardContent, 
  Typography, 
  CircularProgress,
  Chip,
  Grid,
  Button,
  Alert,
  Divider
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import ScaleIcon from '@mui/icons-material/Scale';
import api from '../../services/api';

const WaagenStatus = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [waagenStatus, setWaagenStatus] = useState(null);

  const fetchWaagenStatus = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/v1/waage/waagen/status');
      setWaagenStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Fehler beim Abrufen des Waagen-Status. Bitte versuchen Sie es später erneut.');
      console.error('Waagen Status Fehler:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWaagenStatus();
    // Aktualisiere den Status alle 2 Minuten
    const intervalId = setInterval(fetchWaagenStatus, 2 * 60 * 1000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Card>
      <CardHeader 
        title="Fuhrwerkswaagen Status" 
        avatar={<ScaleIcon />}
        action={
          <Button variant="outlined" onClick={fetchWaagenStatus}>
            Aktualisieren
          </Button>
        }
      />
      <CardContent>
        {waagenStatus && waagenStatus.waagen.map((waage, index) => (
          <Box key={waage.id} mb={index < waagenStatus.waagen.length - 1 ? 3 : 0}>
            {index > 0 && <Divider sx={{ my: 2 }} />}
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Typography variant="h6" component="div" mr={2}>
                    {waage.name} ({waage.id}):
                  </Typography>
                  <Chip
                    icon={waage.status === 'online' ? <CheckCircleIcon /> : <ErrorIcon />}
                    label={waage.status === 'online' ? 'Online' : 'Offline'}
                    color={waage.status === 'online' ? 'success' : 'error'}
                  />
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                  <strong>Maximales Gewicht:</strong> {waage.max_gewicht} {waage.einheit}
                </Typography>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Typography variant="body1">
                  <strong>Kalibrierungsdatum:</strong> {new Date(waage.kalibrierungsdatum).toLocaleDateString()}
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="body1">
                  <strong>Letzte Messung:</strong> {new Date(waage.letzte_messung).toLocaleString()}
                </Typography>
              </Grid>
            </Grid>
          </Box>
        ))}
      </CardContent>
    </Card>
  );
};

export default WaagenStatus; 