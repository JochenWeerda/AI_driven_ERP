"""
Datenbankmodelle für die Inventurverwaltung
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Versuche verschiedene Import-Pfade
try:
    from backend.db.base import Base
except ImportError:
    try:
        from backend.app.db.base import Base
    except ImportError:
        from app.db.base import Base

class InventurStatus(enum.Enum):
    """Status einer Inventur"""
    NEU = "neu"
    IN_BEARBEITUNG = "in_bearbeitung"
    ABGESCHLOSSEN = "abgeschlossen"
    STORNIERT = "storniert"

class Inventur(Base):
    """Modell für eine Inventur"""
    __tablename__ = "inventuren"
    
    id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(255), nullable=False)
    inventurdatum = Column(Date, nullable=False, default=datetime.now().date)
    status = Column(Enum(InventurStatus), nullable=False, default=InventurStatus.NEU)
    lager_id = Column(Integer, ForeignKey("lager.id"), nullable=True)
    bemerkung = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # Beziehungen
    lager = relationship("Lager", back_populates="inventuren")
    positionen = relationship("Inventurposition", back_populates="inventur", cascade="all, delete-orphan")

class Inventurposition(Base):
    """Modell für eine Inventurposition"""
    __tablename__ = "inventurpositionen"
    
    id = Column(Integer, primary_key=True, index=True)
    inventur_id = Column(Integer, ForeignKey("inventuren.id"), nullable=False)
    artikel_id = Column(Integer, ForeignKey("artikel.id"), nullable=False)
    artikelnr = Column(String(50), nullable=False)
    menge_gezaehlt = Column(Float, nullable=False)
    menge_system = Column(Float, nullable=False)
    differenz = Column(Float, nullable=False)
    lagerort = Column(String(50), nullable=True)
    bemerkung = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # Beziehungen
    inventur = relationship("Inventur", back_populates="positionen")
    artikel = relationship("Artikel", back_populates="inventurpositionen")

class Lager(Base):
    """Modell für ein Lager"""
    __tablename__ = "lager"
    
    id = Column(Integer, primary_key=True, index=True)
    bezeichnung = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    adresse = Column(Text, nullable=True)
    aktiv = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # Beziehungen
    inventuren = relationship("Inventur", back_populates="lager")
    bestände = relationship("Artikelbestand", back_populates="lager")

class Artikelbestand(Base):
    """Modell für den Bestand eines Artikels in einem Lager"""
    __tablename__ = "artikelbestaende"
    
    id = Column(Integer, primary_key=True, index=True)
    artikel_id = Column(Integer, ForeignKey("artikel.id"), nullable=False)
    lager_id = Column(Integer, ForeignKey("lager.id"), nullable=False)
    menge = Column(Float, nullable=False, default=0)
    letzte_inventur = Column(Date, nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # Beziehungen
    artikel = relationship("Artikel", back_populates="bestände")
    lager = relationship("Lager", back_populates="bestände")

# Erweiterung des bestehenden Artikel-Modells (nehmen wir an, dass es in WWS_Artikel existiert)
class Artikel(Base):
    """Modell für einen Artikel (vereinfacht)"""
    __tablename__ = "artikel"
    
    id = Column(Integer, primary_key=True, index=True)
    artikelnr = Column(String(50), nullable=False, unique=True)
    bezeichnung = Column(String(255), nullable=False)
    einheit = Column(String(10), nullable=False, default="STK")
    preis = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)
    
    # Beziehungen
    bestände = relationship("Artikelbestand", back_populates="artikel")
    inventurpositionen = relationship("Inventurposition", back_populates="artikel") 