from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import service_service
from app.schemas.service import Service, ServiceCreate, ServiceUpdate
from app.db.session import get_db
from app.api.v1 import dependencies
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Service)
def create_service(service: ServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(dependencies.get_current_active_superuser)):
    return service_service.create_service(db=db, service=service)

@router.get("/", response_model=list[Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(dependencies.get_current_active_user)):
    services = service_service.get_services(db, skip=skip, limit=limit)
    return services

@router.get("/{service_id}", response_model=Service)
def read_service(service_id: int, db: Session = Depends(get_db), current_user: User = Depends(dependencies.get_current_active_user)):
    db_service = service_service.get_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@router.put("/{service_id}", response_model=Service)
def update_service(service_id: int, service: ServiceUpdate, db: Session = Depends(get_db), current_user: User = Depends(dependencies.get_current_active_superuser)):
    db_service = service_service.get_service(db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_service.update_service(db=db, db_service=db_service, service_in=service)

@router.delete("/{service_id}", response_model=Service)
def delete_service(service_id: int, db: Session = Depends(get_db), current_user: User = Depends(dependencies.get_current_active_superuser)):
    db_service = service_service.get_service(db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_service.delete_service(db=db, service_id=service_id)