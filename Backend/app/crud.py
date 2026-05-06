from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash
from typing import Optional

# ---------- User ----------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------- Project ----------
def get_user_projects(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int, owner_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id, models.Project.owner_id == owner_id).first()

def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    db_project = models.Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, db_project: models.Project, project_update: schemas.ProjectUpdate):
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, db_project: models.Project):
    db.delete(db_project)
    db.commit()

# ---------- Task ----------
def get_user_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Task).filter(models.Task.owner_id == owner_id).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int, owner_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == owner_id).first()

def create_task(db: Session, task: schemas.TaskCreate, owner_id: int):
    db_task = models.Task(**task.dict(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: models.Task, task_update: schemas.TaskUpdate):
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: models.Task):
    db.delete(db_task)
    db.commit()