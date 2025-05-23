"""
Core-Modul des AI-Driven ERP-Systems

Dieses Modul enthält zentrale Funktionalitäten und Dienste, die im gesamten System verwendet werden.
"""

# Initialisierung der Pfadregistrierung
try:
    from .path_registry import get_registry
    
    # Singleton-Instanz initialisieren
    registry = get_registry()
    
    # Informationsmeldung
    print("Pfadregister erfolgreich initialisiert.")
except ImportError as e:
    print(f"Warnung: Pfadregister konnte nicht initialisiert werden: {e}")
    print("Falle zurück auf Standard-Import-Mechanismen.")

# Initialisierung des Import-Handlers
try:
    from .import_handler import get_import_handler
    
    # Singleton-Instanz initialisieren
    handler = get_import_handler()
    
    # Informationsmeldung
    print("Import-Handler erfolgreich initialisiert.")
except ImportError as e:
    print(f"Warnung: Import-Handler konnte nicht initialisiert werden: {e}")
    print("Falle zurück auf Standard-Import-Mechanismen.") 