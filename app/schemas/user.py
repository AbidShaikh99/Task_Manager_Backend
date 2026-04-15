from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime
class UserCreate(BaseModel):
    email : EmailStr
    password : str
    role : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    role : str
    
    class Config:
        from_attributes = True
class UserBasic(BaseModel):
    id: int
    name :str
    
    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email : EmailStr
    password : str

class ProjectCreate(BaseModel):
    name : str
    

class TaskCreate(BaseModel):
    title : str
    description :Optional[str] = None
    time_estimate : Optional[str] = None
    project_id : int
    developer_id : int

class TaskResponse(BaseModel):
    id : int
    title : str
    description : Optional[str]
    time_estimate :Optional[str]
    created_at : datetime
    manager_id : int

    project_id : int
    developer_id : int
    
    class Config:
        from_attributes = True  

class Status(BaseModel):
    status : str  

class TaskStatusUpdate(BaseModel):
    status_id: int



class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    developer_id: Optional[int] = None
    project_id: Optional[int] = None
    status_id: Optional[int] = None
    time_estimate:Optional[str]= None
class TaskHistoryResponse(BaseModel):
    field_name: str
    old_value: str
    new_value: str
    updated_at: datetime
    user: UserBasic

    class Config:
        from_attributes = True


class TaskHistoryListResponse(BaseModel):
    status: bool
    message: str
    data: List[TaskHistoryResponse]

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: Optional[str]
    project_id: int
    developer_id: int
    manager_id: int
    status_id: int
    updated_at: datetime

    class Config:
        from_attributes = True
    
