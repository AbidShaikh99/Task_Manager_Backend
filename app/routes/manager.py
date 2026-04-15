from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.user import ProjectCreate, TaskCreate, TaskUpdate, TaskHistoryListResponse
from app.config.settings import get_current_manager
from fastapi.responses import JSONResponse
from app.db.utils import track_task_changes
# router = APIRouter(prefix="/manager", tags=["Manager"])
router = APIRouter()


@router.post("/project")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    new_project = models.Project(
        name=project.name,
        manager_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "status": True,
        "message": "Project created successfully",
        "data": {
            "id": new_project.id,
            "name": new_project.name
        }
    }


@router.post("/task")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    project = db.query(models.Project).filter(
        models.Project.id == task.project_id,
        models.Project.manager_id == current_user.id
    ).first()

    if not project:
        return JSONResponse(
            status_code=404,
            content={
                "status": False,
                "message": "Project not found or not yours",
                "data": None
            }
        )

    developer = db.query(models.User).filter(
        models.User.id == task.developer_id,
        models.User.role == "developer"
    ).first()

    if not developer:
        return JSONResponse(
            status_code=404,
            content={
                "status": False,
                "message": "Developer not found",
                "data": None
            }
        )
    status = db.query(models.Status).filter(
        models.Status.name == "todo"
    ).first()
    
    if not status:
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Default status not found",
                "data": None
            }
        )
    new_task = models.Task(
        title=task.title,
        description = task.description,
        time_estimate = task.time_estimate,
        project_id=task.project_id,
        developer_id=task.developer_id,
        manager_id = current_user.id,
        status_id = status.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": True,
        "message": "Task assigned successfully",
        "data": {
            "task_id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "time_estimate": new_task.time_estimate,
            "created_at": new_task.created_at,
            "developer_id": new_task.developer_id,
            "manager_id": new_task.manager_id,
            "status": new_task.status.name
        }
    }



@router.get("/projects")
def get_my_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    projects = db.query(models.Project).filter(
        models.Project.manager_id == current_user.id
    ).all()

    return {
        "status": True,
        "message": "Projects Geted successfully",
        "data": projects
    }

# @router.get("/tasks")
# def get_my_task(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_manager)
# ):
#     tasks = db.query(models.Task).join(models.Project).filter(
#             models.Project.manager_id == current_user.id

#     ).all()
#     return {
#         "status":True,
#         "message":"Task Geted Successfully.",
#         "data": tasks
#     }


@router.get("/tasks")
def get_tasks(
    project_id: int = Query(None),
    status_id: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if project_id:
        query = query.filter(models.Task.project_id == project_id)

    if status_id:
        query = query.filter(models.Task.status_id == status_id)

    tasks = query.all()

    if not tasks:
        return JSONResponse(
            status_code=400,
            content=
            {
            
            "status": False,
            "message": "No tasks found",
            "data": []
        }) 

    return {
        "status": True,
        "message": "Tasks fetched successfully",
        "data": [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "project_id": task.project_id,
                "status_id": task.status_id
            }
            for task in tasks
        ]
    }


@router.put("/task/{task_id}")
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.manager_id == current_user.id
    ).first()
    
    if not task:
        return{
            "status": False,
            "message": "Task Not Found"
        }
    
    update_data = {}
    
    if payload.title:
        update_data["title"] = payload.title
    
    if payload.description:
        update_data["description"] = payload.description
        
    if payload.developer_id:
        update_data["developer_id"] = payload.developer_id
    
    if payload.project_id:
        update_data["project_id"] = payload.project_id
    
    if payload.status_id:
        update_data["status_id"] = payload.status_id
    
    if payload.time_estimate:
        update_data["time_estimate"] = payload.time_estimate
        
    
    track_task_changes(db, task, update_data, current_user.id)
    
    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    
    return{
        "status":True,
        "message": "Task Update Succesfully."
    }
@router.get("/task/history/{task_id}", response_model=TaskHistoryListResponse)
def get_my_history(
    task_id: int,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_manager)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()
    
    if not task:
        return{
            "status": False,
            "message": "Task Not Found.",
            "data":[]
        }
    if task.developer_id !=  current_user.id and task.manager_id != current_user.id:
        return {
            "Status":False,
            "message": "NOt Authorized",
            "data": []
        }
    
    history = db.query(models.TaskHistory).filter(
        models.TaskHistory.task_id == task_id
    ).all()
    
    return{
        "status":True,
        "message":"History Fetched",
        "data": history
    }
