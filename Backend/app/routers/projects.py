from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_current_user
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[schemas.ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    projects = crud.get_user_projects(db, owner_id=current_user.id, skip=skip, limit=limit)
    # Считаем количество задач для каждого проекта
    for p in projects:
        task_count = db.query(crud.models.Task).filter(crud.models.Task.project_id == p.id).count()
        p.task_count = task_count
    return projects

@router.post("/", response_model=schemas.ProjectOut, status_code=201)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.create_project(db, project, owner_id=current_user.id)

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = crud.get_project(db, project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    task_count = db.query(crud.models.Task).filter(crud.models.Task.project_id == project_id).count()
    db_project.task_count = task_count
    return db_project

@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = crud.get_project(db, project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.update_project(db, db_project, project_update)

@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_project = crud.get_project(db, project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    # При удалении проекта задачи открепляются (project_id = NULL)
    db.query(crud.models.Task).filter(crud.models.Task.project_id == project_id).update({"project_id": None})
    crud.delete_project(db, db_project)