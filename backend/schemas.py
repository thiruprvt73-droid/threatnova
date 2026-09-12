from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from backend.models import SeverityLevel, ThreatStatus, AlertStatus


# Threat Schemas
class ThreatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    severity: SeverityLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    threat_type: str = Field(..., min_length=1, max_length=100)
    source: Optional[str] = None
    indicators: Optional[str] = None
    mitigation_steps: Optional[str] = None


class ThreatCreate(ThreatBase):
    pass


class ThreatUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[SeverityLevel] = None
    status: Optional[ThreatStatus] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    threat_type: Optional[str] = Field(None, min_length=1, max_length=100)
    source: Optional[str] = None
    indicators: Optional[str] = None
    mitigation_steps: Optional[str] = None


class ThreatResponse(ThreatBase):
    id: int
    threat_id: str
    status: ThreatStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Alert Schemas
class AlertBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    severity: SeverityLevel
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    affected_systems: Optional[str] = None
    detection_time: datetime
    threat_id: Optional[int] = None
    assigned_to: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    severity: Optional[SeverityLevel] = None
    status: Optional[AlertStatus] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    affected_systems: Optional[str] = None
    threat_id: Optional[int] = None
    assigned_to: Optional[str] = None


class AlertResponse(AlertBase):
    id: int
    alert_id: str
    status: AlertStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Analysis Schemas
class AnalysisBase(BaseModel):
    threat_id: int
    analysis_type: str = Field(..., min_length=1, max_length=100)
    findings: str = Field(..., min_length=1)
    recommendations: str = Field(..., min_length=1)
    risk_score: float = Field(..., ge=0.0, le=10.0)
    analyst: Optional[str] = None
    ai_generated: bool = True


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = Field(None, min_length=1, max_length=100)
    findings: Optional[str] = Field(None, min_length=1)
    recommendations: Optional[str] = Field(None, min_length=1)
    risk_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    analyst: Optional[str] = None


class AnalysisResponse(AnalysisBase):
    id: int
    analysis_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
