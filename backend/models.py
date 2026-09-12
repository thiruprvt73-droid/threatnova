from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


class SeverityLevel(str, enum.Enum):
    """Threat severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ThreatStatus(str, enum.Enum):
    """Threat status"""
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    MITIGATED = "mitigated"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class AlertStatus(str, enum.Enum):
    """Alert status"""
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class Threat(Base):
    """Threat intelligence model"""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    status = Column(Enum(ThreatStatus), default=ThreatStatus.ACTIVE)
    confidence_score = Column(Float, nullable=False)
    threat_type = Column(String(100), nullable=False)
    source = Column(String(255))
    indicators = Column(Text)  # JSON string of IOCs
    mitigation_steps = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts = relationship("Alert", back_populates="threat")
    analyses = relationship("Analysis", back_populates="threat")


class Alert(Base):
    """Security alert model"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.NEW)
    source_ip = Column(String(45))
    destination_ip = Column(String(45))
    affected_systems = Column(Text)  # JSON string
    detection_time = Column(DateTime, nullable=False)
    threat_id = Column(Integer, ForeignKey("threats.id"))
    assigned_to = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    threat = relationship("Threat", back_populates="alerts")


class Analysis(Base):
    """Threat analysis model"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String(100), unique=True, index=True, nullable=False)
    threat_id = Column(Integer, ForeignKey("threats.id"), nullable=False)
    analysis_type = Column(String(100), nullable=False)
    findings = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=False)
    risk_score = Column(Float, nullable=False)
    analyst = Column(String(100))
    ai_generated = Column(Integer, default=1)  # Boolean: 1=True, 0=False
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    threat = relationship("Threat", back_populates="analyses")
