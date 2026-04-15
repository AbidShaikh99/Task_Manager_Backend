from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.config.settings import get_current_developer,get_current_user
from fastapi.responses import JSONResponse
from app.schemas.user import TaskStatusUpdate,TaskUpdate


router = APIRouter(prefix="/user", tags=["Developer"])

@router.get("/tasks")
def get_my_task(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_developer)
):
    tasks = db.query(models.Task).filter(
        models.Task.developer_id == current_user.id
    ).all()
    return{
        "status":True,
        "message":"Tasks Geted Successfully.",
        "data": tasks
    }

@router.get("/projects")
def get_my_project(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_developer)
):
    projects = db.query(models.Project).join(models.Task).filter(
        models.Task.developer_id == current_user.id
    ).all()
    
    return{
        "status":True,
        "message": "Project Geted Successfully.",
        "data":projects
    }

@router.put("/task/{task_id}/status")
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_developer)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.developer_id == current_user.id
    ).first()

    if not task:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Task not found"
            }
        )

    new_status = db.query(models.Status).filter(
        models.Status.id == payload.status_id
    ).first()

    if not new_status:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Invalid status_id"
            }
        )

    if task.status_id == new_status.id:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": f"Task already in '{new_status.name}' status"
            }
        )
    pending = db.query(models.Status).filter(
        models.Status.name == "todo"
    ).first()

    in_progress = db.query(models.Status).filter(
        models.Status.name == "in progress"
    ).first()

    if (
        pending and in_progress and
        task.status_id == in_progress.id and
        new_status.id == pending.id
    ):
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "This task is in progress"
            }
        )


    completed = db.query(models.Status).filter(
        models.Status.name == "completed"
    ).first()

    if completed and task.status_id == completed.id:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Task already completed, cannot change status"
            }
        )

    task.status_id = new_status.id
    db.commit()
    db.refresh(task)    

    return {
        "status": True,
        "message": "Task status updated successfully",
        "task_id": task.id,
        "new_status": new_status.name
    }

@router.get("/task/{task_id}")
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not task:
        return JSONResponse(
            status_code=404,
            content={
                "status": False,
                "message": "Task not found",
                "data": None
            }
        )

    if task.developer_id != current_user.id and task.manager_id != current_user.id:
        return JSONResponse(
            status_code=403,
            content={
                "status": False,
                "message": "You are not authorized for this task",
                "data": None
            }
        )

    return {
        "status": True,
        "message": "Task fetched successfully",
        "data": {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "project_id": task.project_id,
            "developer_id": task.developer_id,
            "manager_id": task.manager_id,
            "status_id": task.status_id,
            "created_at": task.created_at
        }
    }

