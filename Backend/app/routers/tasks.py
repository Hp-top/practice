from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_current_user
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    return crud.get_user_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.TaskOut, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_task(db, task, owner_id=current_user.id)

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id, owner_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id, owner_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, db_task, task_update)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = crud.get_task(db, task_id, owner_id=current_user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, db_task)