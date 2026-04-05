from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# 用户相关
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    nickname: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# AI配置相关
class AIConfigCreate(BaseModel):
    model_name: str
    model_id: Optional[str] = None
    api_key: str  # 创建时必须提供 API Key
    api_endpoint: Optional[str] = None


class AIConfigUpdate(BaseModel):
    model_name: Optional[str] = None
    model_id: Optional[str] = None
    api_key: Optional[str] = None  # 更新时可选，留空表示不修改
    api_endpoint: Optional[str] = None
    is_active: Optional[bool] = None


class AIConfigResponse(BaseModel):
    id: int
    user_id: int
    model_name: str
    model_id: Optional[str]
    api_key: Optional[str]
    api_endpoint: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# 项目相关
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    default_model_config_id: Optional[int] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    default_model_config_id: Optional[int] = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    default_model_config_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 数据源相关
class DataSourceResponse(BaseModel):
    id: int
    project_id: int
    type: str
    file_path: Optional[str]
    content: Optional[str]
    file_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# 分析任务相关
class TaskCreate(BaseModel):
    project_id: int
    data_source_id: int
    ai_config_id: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    project_id: int
    data_source_id: int
    ai_config_id: Optional[int]
    status: str
    raw_output: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# 实体相关
class EntityCreate(BaseModel):
    task_id: int
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[dict] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    is_user_created: bool = False


class EntityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[dict] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None


class EntityResponse(BaseModel):
    id: int
    task_id: int
    name: str
    type: Optional[str]
    description: Optional[str]
    properties: Optional[dict]
    position_x: Optional[float]
    position_y: Optional[float]
    is_user_created: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 关系相关
class RelationCreate(BaseModel):
    task_id: int
    source_entity_id: int
    target_entity_id: int
    relation_type: Optional[str] = None
    description: Optional[str] = None
    is_user_created: bool = False


class RelationUpdate(BaseModel):
    source_entity_id: Optional[int] = None
    target_entity_id: Optional[int] = None
    relation_type: Optional[str] = None
    description: Optional[str] = None


class RelationResponse(BaseModel):
    id: int
    task_id: int
    source_entity_id: int
    target_entity_id: int
    relation_type: Optional[str]
    description: Optional[str]
    is_user_created: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True