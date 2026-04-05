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
        model_id=config_data.model_id,
        api_key=config_data.api_key,
        api_endpoint=config_data.api_endpoint
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return config


@router.put("/{config_id}", response_model=AIConfigResponse)
@router.patch("/{config_id}", response_model=AIConfigResponse)
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

    # 使用 exclude_unset=True 只处理前端明确传递的字段，兼容所有 Pydantic 版本
    update_data = config_data.model_dump(exclude_unset=True)

    if 'model_name' in update_data and update_data['model_name'] is not None:
        config.model_name = update_data['model_name']
    # model_id 可以是 null（清空）
    if 'model_id' in update_data:
        config.model_id = update_data['model_id']
    # api_key 只有明确提供非空值时才更新（前端编辑留空 = 不修改）
    if 'api_key' in update_data and update_data['api_key'] is not None and update_data['api_key'] != '':
        config.api_key = update_data['api_key']
    # api_endpoint 可以是 null（清空）
    if 'api_endpoint' in update_data:
        config.api_endpoint = update_data['api_endpoint']
    if 'is_active' in update_data:
        config.is_active = update_data['is_active']

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