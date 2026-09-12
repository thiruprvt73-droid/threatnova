from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import logging
from backend.database import get_db
from backend.models import Threat
from backend.schemas import ThreatCreate, ThreatUpdate, ThreatResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ThreatResponse, status_code=status.HTTP_201_CREATED)
def create_threat(threat: ThreatCreate, db: Session = Depends(get_db)):
    """Create a new threat"""
    try:
        db_threat = Threat(
            threat_id=f"THR-{uuid.uuid4().hex[:8].upper()}",
            **threat.model_dump()
        )
        db.add(db_threat)
        db.commit()
        db.refresh(db_threat)
        logger.info(f"Created threat: {db_threat.threat_id}")
        return db_threat
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating threat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create threat"
        )


@router.get("/", response_model=List[ThreatResponse])
def list_threats(
    skip: int = 0,
    limit: int = 100,
    severity: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List all threats with optional filtering"""
    try:
        query = db.query(Threat)
        
        if severity:
            query = query.filter(Threat.severity == severity)
        if status:
            query = query.filter(Threat.status == status)
        
        threats = query.offset(skip).limit(limit).all()
        return threats
    except Exception as e:
        logger.error(f"Error listing threats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve threats"
        )


@router.get("/{threat_id}", response_model=ThreatResponse)
def get_threat(threat_id: str, db: Session = Depends(get_db)):
    """Get a specific threat by ID"""
    threat = db.query(Threat).filter(Threat.threat_id == threat_id).first()
    if not threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat {threat_id} not found"
        )
    return threat


@router.put("/{threat_id}", response_model=ThreatResponse)
def update_threat(
    threat_id: str,
    threat_update: ThreatUpdate,
    db: Session = Depends(get_db)
):
    """Update a threat"""
    db_threat = db.query(Threat).filter(Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat {threat_id} not found"
        )
    
    try:
        update_data = threat_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_threat, field, value)
        
        db.commit()
        db.refresh(db_threat)
        logger.info(f"Updated threat: {threat_id}")
        return db_threat
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating threat {threat_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update threat"
        )


@router.delete("/{threat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_threat(threat_id: str, db: Session = Depends(get_db)):
    """Delete a threat"""
    db_threat = db.query(Threat).filter(Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat {threat_id} not found"
        )
    
    try:
        db.delete(db_threat)
        db.commit()
        logger.info(f"Deleted threat: {threat_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting threat {threat_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete threat"
        )
