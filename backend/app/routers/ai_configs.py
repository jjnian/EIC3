from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, AIConfig
from app.schemas import AIConfigCreate, AIConfigUpdate, AIConfigResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/ai-configs", tags=["AI配置"])


@router.get("", response_model=list[AIConfigResponse])
async def get_ai_configs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(AIConfig).where(AIConfig.user_id == current_user.id))
    return result.scalars().all()


@router.post("", response_model=AIConfigResponse)
async def create_ai_config(
    config_data: AIConfigCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    config = AIConfig(
        user_id=current_user.id,
        model_name=config_data.model_name,
        api_key=config_data.api_key,
        api_endpoint=config_data.api_endpoint
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


@router.put("/{config_id}", response_model=AIConfigResponse)
async def update_ai_config(
    config_id: int,
    config_data: AIConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AIConfig).where(AIConfig.id == config_id, AIConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    if config_data.model_name is not None:
        config.model_name = config_data.model_name
    if config_data.api_key is not None:
        config.api_key = config_data.api_key
    if config_data.api_endpoint is not None:
        config.api_endpoint = config_data.api_endpoint
    if config_data.is_active is not None:
        config.is_active = config_data.is_active

    await db.commit()
    await db.refresh(config)
    return config


@router.delete("/{config_id}")
async def delete_ai_config(
    config_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AIConfig).where(AIConfig.id == config_id, AIConfig.user_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    await db.delete(config)
    await db.commit()
    return {"message": "删除成功"}