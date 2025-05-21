from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db.base import Base
from app.schemas.odata_schemas import TourStatus, PicklisteStatus, AuftragStatus, AuftragArt

class Pickliste(Base):
    __tablename__ = "picklisten"
    
    id = Column(Integer, primary_key=True, index=True)
    picklistnr = Column(Integer, unique=True, index=True)
    erstelltam = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(PicklisteStatus), default=PicklisteStatus.NEU, nullable=False)
    tour_id = Column(Integer, ForeignKey("touren.id"), nullable=False)
    
    # Beziehungen
    tour = relationship("Tour", back_populates="picklisten")
    auftraege = relationship("Auftrag", back_populates="pickliste", cascade="all, delete-orphan")

class Tour(Base):
    __tablename__ = "touren"
    
    id = Column(Integer, primary_key=True, index=True)
    tournr = Column(Integer, unique=True, index=True)
    datum = Column(DateTime, nullable=False)
    status = Column(Enum(TourStatus), default=TourStatus.PLANUNG, nullable=False)
    
    # Beziehungen
    picklisten = relationship("Pickliste", back_populates="tour", cascade="all, delete-orphan")

class Auftrag(Base):
    __tablename__ = "auftraege"
    
    id = Column(Integer, primary_key=True, index=True)
    belegnr = Column(Integer, unique=True, index=True)
    datum = Column(DateTime, nullable=False)
    art = Column(Enum(AuftragArt), nullable=False)
    status = Column(Enum(AuftragStatus), default=AuftragStatus.NEU, nullable=False)
    pickliste_id = Column(Integer, ForeignKey("picklisten.id"), nullable=False)
    
    # Beziehungen
    pickliste = relationship("Pickliste", back_populates="auftraege")
    positionen = relationship("Auftragsposition", back_populates="auftrag", cascade="all, delete-orphan")

class Auftragsposition(Base):
    __tablename__ = "auftragspositionen"
    
    id = Column(Integer, primary_key=True, index=True)
    artikelnr = Column(String(50), nullable=False, index=True)
    menge = Column(Integer, nullable=False)
    auftrag_id = Column(Integer, ForeignKey("auftraege.id"), nullable=False)
    
    # Beziehungen
    auftrag = relationship("Auftrag", back_populates="positionen") 