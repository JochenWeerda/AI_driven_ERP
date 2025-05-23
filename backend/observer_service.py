"""
Observer-Service für das AI-gesteuerte ERP-System
Überwacht die Performance-Metriken und reagiert auf potenzielle Probleme
"""

import os
import sys
import json
import time
import logging
import requests
import psutil
import signal
import threading
import schedule
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import matplotlib.pyplot as plt
import numpy as np

# Eigene Module importieren
try:
    from simple_optimizer import SimpleOptimizer
except ImportError:
    # Wenn nicht gefunden, versuche relativen Import
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from simple_optimizer import SimpleOptimizer
    except ImportError:
        print("WARNUNG: simple_optimizer konnte nicht importiert werden. Automatische Optimierung deaktiviert.")
        SimpleOptimizer = None

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('observer.log')
    ]
)
logger = logging.getLogger("observer_service")

class ObserverService:
    """
    Observer-Service zur Überwachung der Performance des ERP-Systems und 
    zur Ausführung automatischer Optimierungsmaßnahmen.
    """
    
    def __init__(self, config_path: str = "observer_config.json"):
        """
        Initialisiert den Observer-Service
        
        Args:
            config_path: Pfad zur Konfigurationsdatei
        """
        self.config = self._load_config(config_path)
        self.server_url = self.config.get("server_url", "http://localhost:8000")
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history_size = self.config.get("max_history_size", 1000)
        self.alert_thresholds = self.config.get("alert_thresholds", {})
        self.check_interval = self.config.get("check_interval", 60)  # Sekunden
        self.data_dir = Path(self.config.get("data_dir", "observer_data"))
        self.chart_dir = self.data_dir / "charts"
        self.running = False
        self.optimizer = None
        
        # Verzeichnisse erstellen, falls nicht vorhanden
        self.data_dir.mkdir(exist_ok=True)
        self.chart_dir.mkdir(exist_ok=True)
        
        # Optimizer erstellen, wenn verfügbar
        if SimpleOptimizer is not None and self.config.get("enable_optimizer", False):
            optimizer_config = self.config.get("optimizer_config", "optimizer_config.json")
            self.optimizer = SimpleOptimizer(optimizer_config)
            logger.info(f"SimpleOptimizer initialisiert mit Konfiguration: {optimizer_config}")
        
        logger.info(f"ObserverService initialisiert mit Server-URL: {self.server_url}")
        logger.info(f"Überwachungsintervall: {self.check_interval} Sekunden")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Lädt die Konfiguration aus einer JSON-Datei
        
        Args:
            config_path: Pfad zur Konfigurationsdatei
            
        Returns:
            Die geladene Konfiguration als Dictionary
        """
        default_config = {
            "server_url": "http://localhost:8000",
            "check_interval": 60,
            "max_history_size": 1000,
            "data_dir": "observer_data",
            "alert_thresholds": {
                "cpu_usage_percent": 85.0,
                "memory_usage_percent": 90.0,
                "average_response_time_ms": 1000.0,
                "error_rate_percent": 10.0
            },
            "enable_optimizer": False,
            "optimizer_config": "optimizer_config.json",
            "chart_generation_interval": 3600  # 1 Stunde
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                logger.info(f"Konfiguration geladen aus: {config_path}")
                
                # Zusammenführen mit Standard-Konfiguration
                for key, value in loaded_config.items():
                    if isinstance(value, dict) and key in default_config:
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
                        
                return default_config
            else:
                logger.warning(f"Konfigurationsdatei nicht gefunden: {config_path}")
                logger.info("Erstelle Standard-Konfigurationsdatei...")
                
                # Standard-Konfiguration speichern
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                
                return default_config
        except Exception as e:
            logger.error(f"Fehler beim Laden der Konfiguration: {str(e)}")
            return default_config
    
    def get_server_metrics(self) -> Dict[str, Any]:
        """
        Ruft die Performance-Metriken vom Server ab
        
        Returns:
            Dictionary mit Server-Metriken oder leeres Dictionary bei Fehler
        """
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                metrics = response.json()
                logger.debug(f"Server-Metriken abgerufen: {metrics}")
                
                # Zeitstempel hinzufügen
                metrics["timestamp"] = datetime.now().isoformat()
                
                return metrics
            else:
                logger.error(f"Fehler beim Abrufen der Metriken: HTTP {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Server-Metriken: {str(e)}")
            return {}
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prüft, ob Metriken Schwellenwerte überschreiten und generiert Alerts
        
        Args:
            metrics: Dictionary mit Server-Metriken
            
        Returns:
            Liste der generierten Alerts
        """
        if not metrics:
            return []
        
        alerts = []
        server_metrics = metrics.get("metrics", {})
        timestamp = metrics.get("timestamp", datetime.now().isoformat())
        
        # CPU-Auslastung prüfen
        cpu_usage = server_metrics.get("cpu_usage_percent", 0)
        cpu_threshold = self.alert_thresholds.get("cpu_usage_percent", 85)
        if cpu_usage > cpu_threshold:
            alerts.append({
                "timestamp": timestamp,
                "type": "high_cpu",
                "metric": "cpu_usage_percent",
                "value": cpu_usage,
                "threshold": cpu_threshold,
                "message": f"Hohe CPU-Auslastung: {cpu_usage}% (Schwellenwert: {cpu_threshold}%)"
            })
        
        # Speicherauslastung prüfen
        memory_usage = server_metrics.get("memory_usage_percent", 0)
        memory_threshold = self.alert_thresholds.get("memory_usage_percent", 90)
        if memory_usage > memory_threshold:
            alerts.append({
                "timestamp": timestamp,
                "type": "high_memory",
                "metric": "memory_usage_percent",
                "value": memory_usage,
                "threshold": memory_threshold,
                "message": f"Hohe Speicherauslastung: {memory_usage}% (Schwellenwert: {memory_threshold}%)"
            })
        
        # Antwortzeit prüfen
        response_time = server_metrics.get("average_response_time_ms", 0)
        response_time_threshold = self.alert_thresholds.get("average_response_time_ms", 1000)
        if response_time > response_time_threshold:
            alerts.append({
                "timestamp": timestamp,
                "type": "high_response_time",
                "metric": "average_response_time_ms",
                "value": response_time,
                "threshold": response_time_threshold,
                "message": f"Hohe Antwortzeit: {response_time} ms (Schwellenwert: {response_time_threshold} ms)"
            })
        
        # Weitere Metriken können hier hinzugefügt werden
        
        return alerts
    
    def save_metrics(self, metrics: Dict[str, Any]):
        """
        Speichert die Metriken in der Historie und in einer JSON-Datei
        
        Args:
            metrics: Dictionary mit Server-Metriken
        """
        if not metrics:
            return
        
        # Zur Historie hinzufügen
        self.metrics_history.append(metrics)
        
        # Historie auf maximale Größe begrenzen
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
        
        # Metriken für den aktuellen Tag speichern
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            metrics_file = self.data_dir / f"metrics_{date_str}.json"
            
            # Bestehende Metriken laden, falls vorhanden
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    try:
                        daily_metrics = json.load(f)
                    except json.JSONDecodeError:
                        daily_metrics = []
            else:
                daily_metrics = []
            
            # Neue Metriken hinzufügen
            daily_metrics.append(metrics)
            
            # Metriken speichern
            with open(metrics_file, 'w') as f:
                json.dump(daily_metrics, f, indent=2)
                
            logger.debug(f"Metriken gespeichert in: {metrics_file}")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Metriken: {str(e)}")
    
    def save_alerts(self, alerts: List[Dict[str, Any]]):
        """
        Speichert Alerts in einer JSON-Datei
        
        Args:
            alerts: Liste der zu speichernden Alerts
        """
        if not alerts:
            return
        
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            alerts_file = self.data_dir / f"alerts_{date_str}.json"
            
            # Bestehende Alerts laden, falls vorhanden
            if alerts_file.exists():
                with open(alerts_file, 'r') as f:
                    try:
                        daily_alerts = json.load(f)
                    except json.JSONDecodeError:
                        daily_alerts = []
            else:
                daily_alerts = []
            
            # Neue Alerts hinzufügen
            daily_alerts.extend(alerts)
            
            # Alerts speichern
            with open(alerts_file, 'w') as f:
                json.dump(daily_alerts, f, indent=2)
            
            logger.info(f"{len(alerts)} Alerts gespeichert in: {alerts_file}")
            
            # Alerts protokollieren
            for alert in alerts:
                logger.warning(f"ALERT: {alert['message']}")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Alerts: {str(e)}")
    
    def generate_charts(self):
        """Generiert Diagramme aus den gesammelten Metriken"""
        if not self.metrics_history:
            logger.info("Keine Metriken für die Diagrammerstellung verfügbar")
            return
        
        try:
            # Zeitstempel für die Diagramm-Dateinamen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Daten extrahieren
            timestamps = []
            cpu_values = []
            memory_values = []
            response_times = []
            
            for entry in self.metrics_history:
                try:
                    dt = datetime.fromisoformat(entry.get("timestamp", ""))
                    timestamps.append(dt)
                    
                    metrics = entry.get("metrics", {})
                    cpu_values.append(metrics.get("cpu_usage_percent", 0))
                    memory_values.append(metrics.get("memory_usage_percent", 0))
                    response_times.append(metrics.get("average_response_time_ms", 0))
                except (ValueError, TypeError) as e:
                    logger.warning(f"Fehler bei der Datenextraktion für Diagramme: {str(e)}")
                    continue
            
            if not timestamps:
                logger.warning("Keine gültigen Zeitstempel für die Diagrammerstellung gefunden")
                return
            
            # CPU-Auslastungs-Diagramm
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, cpu_values, 'b-', label='CPU-Auslastung (%)')
            plt.axhline(y=self.alert_thresholds.get("cpu_usage_percent", 85), color='r', linestyle='--', label='Schwellenwert')
            plt.title('CPU-Auslastung über Zeit')
            plt.xlabel('Zeit')
            plt.ylabel('CPU-Auslastung (%)')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            cpu_chart_path = self.chart_dir / f"cpu_usage_{timestamp}.png"
            plt.savefig(cpu_chart_path)
            plt.close()
            
            # Speicherauslastungs-Diagramm
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, memory_values, 'g-', label='Speicherauslastung (%)')
            plt.axhline(y=self.alert_thresholds.get("memory_usage_percent", 90), color='r', linestyle='--', label='Schwellenwert')
            plt.title('Speicherauslastung über Zeit')
            plt.xlabel('Zeit')
            plt.ylabel('Speicherauslastung (%)')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            memory_chart_path = self.chart_dir / f"memory_usage_{timestamp}.png"
            plt.savefig(memory_chart_path)
            plt.close()
            
            # Antwortzeit-Diagramm
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, response_times, 'm-', label='Antwortzeit (ms)')
            plt.axhline(y=self.alert_thresholds.get("average_response_time_ms", 1000), color='r', linestyle='--', label='Schwellenwert')
            plt.title('Antwortzeit über Zeit')
            plt.xlabel('Zeit')
            plt.ylabel('Antwortzeit (ms)')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            response_time_chart_path = self.chart_dir / f"response_time_{timestamp}.png"
            plt.savefig(response_time_chart_path)
            plt.close()
            
            logger.info(f"Diagramme erstellt in: {self.chart_dir}")
            
            # Aktuelle Diagramme auch unter festen Namen speichern für Dashboards
            cpu_chart_path_latest = self.chart_dir / "cpu_usage_latest.png"
            memory_chart_path_latest = self.chart_dir / "memory_usage_latest.png"
            response_time_chart_path_latest = self.chart_dir / "response_time_latest.png"
            
            # Kopieren der aktuellen Diagramme
            import shutil
            shutil.copy(cpu_chart_path, cpu_chart_path_latest)
            shutil.copy(memory_chart_path, memory_chart_path_latest)
            shutil.copy(response_time_chart_path, response_time_chart_path_latest)
            
        except Exception as e:
            logger.error(f"Fehler bei der Diagrammerstellung: {str(e)}")
    
    def run_monitoring_cycle(self):
        """Führt einen vollständigen Überwachungszyklus aus"""
        logger.debug("Starte Überwachungszyklus...")
        
        # Server-Metriken abrufen
        metrics = self.get_server_metrics()
        if not metrics:
            logger.warning("Keine Metriken verfügbar, überspringe Zyklus")
            return
        
        # Metriken speichern
        self.save_metrics(metrics)
        
        # Alerts prüfen und speichern
        alerts = self.check_alerts(metrics)
        if alerts:
            self.save_alerts(alerts)
        
        # Optimizer ausführen, wenn verfügbar und aktiviert
        if self.optimizer is not None:
            logger.debug("Führe Optimierungszyklus aus...")
            self.optimizer.run_optimization_cycle()
    
    def start(self):
        """Startet den Observer-Service"""
        if self.running:
            logger.warning("Observer-Service läuft bereits")
            return
        
        self.running = True
        logger.info("Observer-Service gestartet")
        
        # Initiales Diagramm erstellen
        self.generate_charts()
        
        # Planen der regelmäßigen Diagrammerstellung
        chart_interval = self.config.get("chart_generation_interval", 3600)  # Standardmäßig stündlich
        schedule.every(chart_interval).seconds.do(self.generate_charts)
        
        # Signal-Handler für sauberes Beenden
        def signal_handler(sig, frame):
            logger.info("Beende Observer-Service...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Überwachungsschleife starten
        try:
            while self.running:
                self.run_monitoring_cycle()
                
                # Geplante Aufgaben ausführen
                schedule.run_pending()
                
                # Warten bis zum nächsten Zyklus
                time.sleep(self.check_interval)
        except Exception as e:
            logger.error(f"Fehler im Überwachungszyklus: {str(e)}")
            self.running = False
    
    def stop(self):
        """Stoppt den Observer-Service"""
        if not self.running:
            return
        
        self.running = False
        logger.info("Observer-Service gestoppt")
        
        # Abschließendes Diagramm erstellen
        self.generate_charts()

def create_startup_scripts():
    """Erstellt Startup-Skripte für verschiedene Betriebssysteme"""
    # Windows-Batch-Skript
    windows_script = """@echo off
echo Starte Observer-Service...
python observer_service.py
pause
"""
    
    # Linux/macOS-Shell-Skript
    linux_script = """#!/bin/bash
echo "Starte Observer-Service..."
python3 observer_service.py
"""
    
    try:
        # Windows-Skript erstellen
        with open("start_observer.bat", 'w') as f:
            f.write(windows_script)
        
        # Linux-Skript erstellen
        with open("start_observer.sh", 'w') as f:
            f.write(linux_script)
        
        # Linux-Skript ausführbar machen (falls unter Linux/macOS)
        try:
            os.chmod("start_observer.sh", 0o755)
        except:
            pass
        
        logger.info("Startup-Skripte erstellt: start_observer.bat, start_observer.sh")
    except Exception as e:
        logger.error(f"Fehler beim Erstellen der Startup-Skripte: {str(e)}")

def main():
    """Hauptfunktion für die Ausführung des Observer-Service"""
    # Konfigurationspfad bestimmen
    config_path = os.environ.get("OBSERVER_CONFIG", "observer_config.json")
    
    # Startup-Skripte erstellen
    create_startup_scripts()
    
    # Observer-Service erstellen und starten
    observer = ObserverService(config_path)
    observer.start()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 