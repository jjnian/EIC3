import os
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.config import settings
from app.models import User, Project, DataSource
from app.schemas import DataSourceResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/data-sources", tags=["数据源"])

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DataSourceResponse)
async def upload_file(
    project_id: int = Form(...),
    file: UploadFile = File(None),
    content: str = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证项目存在
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    if file:
        # 处理文件上传
        file_type = "text"
        if file.content_type and file.content_type.startswith("image"):
            file_type = "image"
        elif file.content_type and file.content_type.startswith("video"):
            file_type = "video"

        # 保存文件
        file_path = os.path.join(settings.UPLOAD_DIR, f"{project_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content_bytes = await file.read()
            f.write(content_bytes)

        data_source = DataSource(
            project_id=project_id,
            type=file_type,
            file_path=file_path,
            file_name=file.filename
        )
    elif content:
        # 处理文字输入
        data_source = DataSource(
            project_id=project_id,
            type="text",
            content=content
        )
    else:
        raise HTTPException(status_code=400, detail="请上传文件或输入文字")

    db.add(data_source)
    await db.commit()
    await db.refresh(data_source)
    return data_source


@router.get("", response_model=list[DataSourceResponse])
async def get_data_sources(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证项目存在
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    result = await db.execute(select(DataSource).where(DataSource.project_id == project_id))
    return result.scalars().all()


@router.delete("/{data_source_id}")
async def delete_data_source(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DataSource).join(Project).where(
            DataSource.id == data_source_id,
            Project.user_id == current_user.id
        )
    )
    data_source = result.scalar_one_or_none()
    if not data_source:
        raise HTTPException(status_code=404, detail="数据源不存在")

    # 删除文件
    if data_source.file_path and os.path.exists(data_source.file_path):
        os.remove(data_source.file_path)

    await db.delete(data_source)
    await db.commit()
    return {"message": "删除成功"}