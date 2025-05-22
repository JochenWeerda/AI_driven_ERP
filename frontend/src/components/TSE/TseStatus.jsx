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
  Alert
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import api from '../../services/api';

const TseStatus = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tseStatus, setTseStatus] = useState(null);

  const fetchTseStatus = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/v1/tse/status/');
      setTseStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Fehler beim Abrufen des TSE-Status. Bitte versuchen Sie es später erneut.');
      console.error('TSE Status Fehler:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTseStatus();
    // Aktualisiere den Status alle 5 Minuten
    const intervalId = setInterval(fetchTseStatus, 5 * 60 * 1000);
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
        title="TSE Status" 
        action={
          <Button variant="outlined" onClick={fetchTseStatus}>
            Aktualisieren
          </Button>
        }
      />
      <CardContent>
        {tseStatus && (
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Box display="flex" alignItems="center" mb={2}>
                <Typography variant="h6" component="div" mr={2}>
                  Status:
                </Typography>
                <Chip
                  icon={tseStatus.status === 'aktiv' ? <CheckCircleIcon /> : <ErrorIcon />}
                  label={tseStatus.status === 'aktiv' ? 'Aktiv' : 'Inaktiv'}
                  color={tseStatus.status === 'aktiv' ? 'success' : 'error'}
                />
              </Box>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="body1">
                <strong>Seriennummer:</strong> {tseStatus.seriennummer}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="body1">
                <strong>Signaturzähler:</strong> {tseStatus.signaturzaehler}
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="body1">
                <strong>Restkapazität:</strong> {tseStatus.restkapazitaet}%
              </Typography>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Typography variant="body1">
                <strong>Letzte Signatur:</strong> {tseStatus.letzte_signatur}
              </Typography>
            </Grid>
            
            <Grid item xs={12}>
              <Typography variant="body1">
                <strong>Letzter Zeitpunkt:</strong> {new Date(tseStatus.zeitpunkt).toLocaleString()}
              </Typography>
            </Grid>
          </Grid>
        )}
      </CardContent>
    </Card>
  );
};

export default TseStatus; 