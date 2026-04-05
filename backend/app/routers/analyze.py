from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import base64
import os

from app.database import get_db
from app.models import User, AIConfig
from app.schemas import EntityResponse, RelationResponse
from app.services.auth import get_current_user
from app.adapters import get_adapter, DEFAULT_PROMPT
from app.config import settings

router = APIRouter(prefix="/analyze", tags=["分析"])


@router.post("")
async def analyze_content(
    content: str = Form(""),
    file_url: str = Form(None),
    file_type: str = Form(None),
    ai_config_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """分析内容，返回实体和关系"""
    # 获取AI配置
    result = await db.execute(select(AIConfig).where(
        AIConfig.id == ai_config_id,
        AIConfig.user_id == current_user.id
    ))
    ai_config = result.scalar_one_or_none()
    if not ai_config:
        raise HTTPException(status_code=404, detail="AI配置不存在")

    # 准备内容
    analysis_content = ""
    content_type = "text"

    if file_url and file_type:
        content_type = file_type
        # 读取文件
        file_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(file_url))
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                analysis_content = base64.b64encode(f.read()).decode()
    else:
        analysis_content = content

    # 调用AI
    adapter = get_adapter(
        ai_config.model_name,
        api_key=ai_config.api_key,
        api_endpoint=ai_config.api_endpoint,
        model_id=ai_config.model_id
    )

    prompt = DEFAULT_PROMPT.format(content_type=content_type)
    result_data = await adapter.analyze(analysis_content, content_type, prompt)

    # 构造返回数据（临时ID）
    entities = []
    relations = []

    for i, entity_data in enumerate(result_data.get("entities", [])):
        entities.append({
            "id": i + 1,
            "name": entity_data.get("name", ""),
            "type": entity_data.get("type"),
            "description": entity_data.get("description", "")
        })

    # 构建名称到ID的映射
    name_to_id = {e["name"]: e["id"] for e in entities}

    for i, rel_data in enumerate(result_data.get("relations", [])):
        source_name = rel_data.get("source")
        target_name = rel_data.get("target")

        relations.append({
            "id": i + 1,
            "source": source_name,
            "target": target_name,
            "source_entity_id": name_to_id.get(source_name),
            "target_entity_id": name_to_id.get(target_name),
            "type": rel_data.get("type"),
            "description": rel_data.get("description", "")
        })

    return {
        "entities": entities,
        "relations": relations
    }