from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import logging
from backend.database import get_db
from backend.models import Analysis
from backend.schemas import AnalysisCreate, AnalysisUpdate, AnalysisResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(analysis: AnalysisCreate, db: Session = Depends(get_db)):
    """Create a new threat analysis"""
    try:
        db_analysis = Analysis(
            analysis_id=f"ANL-{uuid.uuid4().hex[:8].upper()}",
            **analysis.model_dump()
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        logger.info(f"Created analysis: {db_analysis.analysis_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create analysis"
        )


@router.get("/", response_model=List[AnalysisResponse])
def list_analyses(
    skip: int = 0,
    limit: int = 100,
    threat_id: int = None,
    db: Session = Depends(get_db)
):
    """List all analyses with optional filtering"""
    try:
        query = db.query(Analysis)
        
        if threat_id:
            query = query.filter(Analysis.threat_id == threat_id)
        
        analyses = query.offset(skip).limit(limit).all()
        return analyses
    except Exception as e:
        logger.error(f"Error listing analyses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analyses"
        )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Get a specific analysis by ID"""
    analysis = db.query(Analysis).filter(Analysis.analysis_id == analysis_id).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    return analysis


@router.put("/{analysis_id}", response_model=AnalysisResponse)
def update_analysis(
    analysis_id: str,
    analysis_update: AnalysisUpdate,
    db: Session = Depends(get_db)
):
    """Update an analysis"""
    db_analysis = db.query(Analysis).filter(Analysis.analysis_id == analysis_id).first()
    if not db_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    
    try:
        update_data = analysis_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_analysis, field, value)
        
        db.commit()
        db.refresh(db_analysis)
        logger.info(f"Updated analysis: {analysis_id}")
        return db_analysis
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update analysis"
        )


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Delete an analysis"""
    db_analysis = db.query(Analysis).filter(Analysis.analysis_id == analysis_id).first()
    if not db_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )
    
    try:
        db.delete(db_analysis)
        db.commit()
        logger.info(f"Deleted analysis: {analysis_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete analysis"
        )
