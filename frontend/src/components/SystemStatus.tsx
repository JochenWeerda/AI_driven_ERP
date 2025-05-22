import React, { useState, useEffect } from 'react';
import { Paper, Typography, Box, CircularProgress, Chip, Tooltip, Alert, LinearProgress, Grid, Divider, useTheme, IconButton } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import WarningIcon from '@mui/icons-material/Warning';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import RefreshIcon from '@mui/icons-material/Refresh';
import MemoryIcon from '@mui/icons-material/Memory';
import StorageIcon from '@mui/icons-material/Storage';
import DeveloperBoardIcon from '@mui/icons-material/DeveloperBoard';
import SettingsIcon from '@mui/icons-material/Settings';
import axios from 'axios';

interface SystemStatusProps {
  expanded?: boolean;
}

interface DetailedStatus {
  timestamp: string;
  system_info: {
    system: string;
    version: string;
    python_version: string;
    cpu_count: number;
    memory_total: number;
    memory_available: number;
  };
  current_stats: {
    cpu_percent: number;
    memory_percent: number;
    disk_percent: number;
  };
  database: {
    status: string;
    response_time_ms: number;
    error?: string;
  };
  app_info: {
    version: string;
    project_name: string;
    api_prefix: string;
  };
  status: string;
  cache: {
    from_cache: boolean;
    cached_at?: string;
    cache_age_seconds?: number;
  };
}

const SystemStatus: React.FC<SystemStatusProps> = ({ expanded = false }) => {
  const theme = useTheme();
  const [backendStatus, setBackendStatus] = useState<'healthy' | 'warning' | 'error' | 'checking' | 'timeout'>('checking');
  const [lastChecked, setLastChecked] = useState<Date | null>(null);
  const [consecutiveFailures, setConsecutiveFailures] = useState(0);
  const [message, setMessage] = useState<string>('');
  const [showDetails, setShowDetails] = useState(expanded);
  const [detailedStatus, setDetailedStatus] = useState<DetailedStatus | null>(null);
  const [loadingDetailed, setLoadingDetailed] = useState(false);

  // Einfacher Gesundheitscheck
  const checkBackendStatus = async () => {
    try {
      setBackendStatus('checking');
      const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/health`, {
        timeout: 5000, // 5 Sekunden Timeout
      });
      
      if (response.data.status === 'healthy') {
        setBackendStatus('healthy');
        setConsecutiveFailures(0);
        setMessage('');
      } else {
        setBackendStatus('warning');
        setConsecutiveFailures(prev => prev + 1);
        setMessage('Der Backend-Server meldet einen ungesunden Zustand.');
      }
    } catch (error) {
      setBackendStatus('timeout');
      setConsecutiveFailures(prev => prev + 1);
      setMessage('Keine Verbindung zum Backend-Server möglich.');
    } finally {
      setLastChecked(new Date());
    }
  };

  // Detaillierter Statusbericht
  const fetchDetailedStatus = async () => {
    if (backendStatus === 'timeout') {
      return; // Keine Verbindung, kein Versuch
    }
    
    setLoadingDetailed(true);
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/system/status`, {
        timeout: 8000, // 8 Sekunden Timeout für detaillierte Informationen
      });
      
      setDetailedStatus(response.data);
      
      // Aktualisiere den Gesamtstatus basierend auf dem detaillierten Status
      if (response.data.status === 'healthy') {
        setBackendStatus('healthy');
      } else if (response.data.status === 'warning') {
        setBackendStatus('warning');
      } else {
        setBackendStatus('error');
      }
    } catch (error) {
      console.error('Fehler beim Abrufen des detaillierten Status:', error);
      setDetailedStatus(null);
    } finally {
      setLoadingDetailed(false);
    }
  };

  // Kombinierter Check beim Laden und dann alle 30 Sekunden
  useEffect(() => {
    const checkStatus = async () => {
      await checkBackendStatus();
      if (showDetails) {
        await fetchDetailedStatus();
      }
    };
    
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    
    return () => clearInterval(interval);
  }, [showDetails]);

  // Wenn Details angezeigt werden sollen, aber noch nicht geladen wurden
  useEffect(() => {
    if (showDetails && !detailedStatus && backendStatus !== 'timeout') {
      fetchDetailedStatus();
    }
  }, [showDetails, detailedStatus, backendStatus]);

  const getStatusColor = () => {
    switch (backendStatus) {
      case 'healthy': return 'success';
      case 'warning': return 'warning';
      case 'error': 
      case 'timeout': return 'error';
      case 'checking': return 'info';
      default: return 'default';
    }
  };

  const getStatusIcon = () => {
    switch (backendStatus) {
      case 'healthy': return <CheckCircleIcon fontSize="small" />;
      case 'warning': return <WarningIcon fontSize="small" />;
      case 'error': 
      case 'timeout': return <ErrorIcon fontSize="small" />;
      case 'checking': return <HourglassEmptyIcon fontSize="small" />;
      default: return null;
    }
  };

  const getStatusText = () => {
    switch (backendStatus) {
      case 'healthy': return 'Online';
      case 'warning': return 'Warnung';
      case 'error': return 'Fehler';
      case 'timeout': return 'Offline';
      case 'checking': return 'Überprüfe...';
      default: return 'Unbekannt';
    }
  };

  // Formatiere Bytes in lesbare Größe
  const formatBytes = (bytes: number, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };

  // Farbcodierung für Prozentsätze
  const getColorForPercent = (percent: number) => {
    if (percent < 60) return theme.palette.success.main;
    if (percent < 80) return theme.palette.warning.main;
    return theme.palette.error.main;
  };

  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 2, 
        mb: 2,
        transition: 'all 0.3s',
        '&:hover': { 
          boxShadow: 4,
        }
      }}
    >
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box display="flex" alignItems="center" sx={{ cursor: 'pointer' }} onClick={() => setShowDetails(!showDetails)}>
          <SettingsIcon sx={{ mr: 1, color: 'text.secondary' }} />
          <Typography variant="subtitle1" fontWeight="bold">
            Systemstatus
          </Typography>
        </Box>
        
        <Box display="flex" alignItems="center">
          <Chip
            icon={getStatusIcon()}
            label={getStatusText()}
            color={getStatusColor() as any}
            size="small"
            sx={{ mr: 1 }}
          />
          
          <Tooltip title="Status aktualisieren">
            <IconButton 
              size="small" 
              onClick={(e) => {
                e.stopPropagation();
                checkBackendStatus();
                if (showDetails) fetchDetailedStatus();
              }}
              color="primary"
            >
              <RefreshIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      {showDetails && (
        <Box mt={2}>
          {backendStatus !== 'healthy' && message && (
            <Alert severity={backendStatus === 'warning' ? 'warning' : 'error'} sx={{ mb: 2 }}>
              {message}
              {consecutiveFailures > 1 && (
                <Typography variant="caption" display="block">
                  {consecutiveFailures} aufeinanderfolgende Fehler
                </Typography>
              )}
            </Alert>
          )}
          
          {loadingDetailed && <LinearProgress sx={{ mb: 2 }} />}
          
          {detailedStatus && (
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <DeveloperBoardIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="subtitle2">CPU-Auslastung</Typography>
                  </Box>
                  <Box sx={{ mb: 1 }}>
                    <Box display="flex" justifyContent="space-between" mb={0.5}>
                      <Typography variant="body2" color="text.secondary">
                        Auslastung
                      </Typography>
                      <Typography variant="body2" fontWeight="medium">
                        {detailedStatus.current_stats.cpu_percent}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={detailedStatus.current_stats.cpu_percent} 
                      sx={{ 
                        height: 8, 
                        borderRadius: 1,
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: getColorForPercent(detailedStatus.current_stats.cpu_percent)
                        }
                      }}
                    />
                  </Box>
                  <Typography variant="caption" display="block" color="text.secondary">
                    {detailedStatus.system_info.cpu_count} Kerne verfügbar
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <MemoryIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="subtitle2">Speichernutzung</Typography>
                  </Box>
                  <Box sx={{ mb: 1 }}>
                    <Box display="flex" justifyContent="space-between" mb={0.5}>
                      <Typography variant="body2" color="text.secondary">
                        Auslastung
                      </Typography>
                      <Typography variant="body2" fontWeight="medium">
                        {detailedStatus.current_stats.memory_percent}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={detailedStatus.current_stats.memory_percent} 
                      sx={{ 
                        height: 8, 
                        borderRadius: 1,
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: getColorForPercent(detailedStatus.current_stats.memory_percent)
                        }
                      }}
                    />
                  </Box>
                  <Typography variant="caption" display="block" color="text.secondary">
                    {formatBytes(detailedStatus.system_info.memory_available)} von {formatBytes(detailedStatus.system_info.memory_total)} frei
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={12}>
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <StorageIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="subtitle2">Datenbank</Typography>
                  </Box>
                  <Box display="flex" alignItems="center">
                    <Chip 
                      size="small" 
                      label={detailedStatus.database.status === 'connected' ? 'Verbunden' : 'Fehler'} 
                      color={detailedStatus.database.status === 'connected' ? 'success' : 'error'}
                      sx={{ mr: 2 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      Antwortzeit: {detailedStatus.database.response_time_ms} ms
                    </Typography>
                  </Box>
                  {detailedStatus.database.error && (
                    <Typography variant="caption" color="error" display="block" mt={1}>
                      Fehler: {detailedStatus.database.error}
                    </Typography>
                  )}
                </Paper>
              </Grid>
            </Grid>
          )}
          
          {!loadingDetailed && !detailedStatus && backendStatus !== 'checking' && (
            <Alert severity="info">
              Detaillierte Statusinformationen konnten nicht geladen werden.
              <Box display="flex" justifyContent="flex-end" mt={1}>
                <Chip 
                  label="Neu laden" 
                  size="small" 
                  color="primary" 
                  onClick={() => fetchDetailedStatus()} 
                  sx={{ cursor: 'pointer' }}
                />
              </Box>
            </Alert>
          )}
          
          <Divider sx={{ my: 2 }} />
          
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="caption" color="text.secondary">
              Letzte Prüfung: {lastChecked ? new Intl.DateTimeFormat('de-DE', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
              }).format(lastChecked) : 'Noch nicht geprüft'}
            </Typography>
            
            {detailedStatus?.cache.from_cache && (
              <Tooltip title="Daten aus Cache">
                <Chip 
                  label={`Cache (${Math.round(detailedStatus.cache.cache_age_seconds || 0)}s)`} 
                  size="small" 
                  variant="outlined"
                  color="secondary"
                />
              </Tooltip>
            )}
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default SystemStatus; 