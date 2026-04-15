from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    projects = relationship("Project", back_populates="manager")

    tasks = relationship("Task",back_populates="developer",foreign_keys="Task.developer_id")

    managed_tasks = relationship("Task",back_populates="manager",foreign_keys="Task.manager_id")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager_id = Column(Integer, ForeignKey("users.id"))
    
    manager = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    time_estimate = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    status_id = Column(Integer, ForeignKey("status.id"))

    project_id = Column(Integer, ForeignKey("projects.id"))
    developer_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    

    project = relationship("Project", back_populates="tasks")

    developer = relationship("User",back_populates="tasks",foreign_keys=[developer_id])

    manager = relationship("User",back_populates="managed_tasks",foreign_keys=[manager_id])
    
    status = relationship("Status", back_populates="tasks")
    
class Status(Base):
    __tablename__ ="status"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    
    tasks = relationship("Task", back_populates="status")

class TaskHistory(Base):
    __tablename__ = "task_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    
    field_name = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    old_time_estimate = Column(String, nullable=True)
    new_time_estimate = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.now)

    task = relationship("Task")
    user = relationship("User")