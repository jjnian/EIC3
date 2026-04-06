"""
对话式AI分析模块
支持流式响应，边对话边提取实体和关系，实时展示在画布上
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, AsyncGenerator
import json
import asyncio

from app.database import get_db
from app.models import User, AIConfig
from app.services.auth import get_current_user
from app.adapters import get_adapter

router = APIRouter(prefix="/chat", tags=["对话分析"])


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    ai_config_id: int
    project_id: Optional[int] = None


class ExtractedEntity(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    # 用于画布展示
    x: Optional[float] = None
    y: Optional[float] = None


class ExtractedRelation(BaseModel):
    source: str
    target: str
    type: str
    description: Optional[str] = None


DIALOG_PROMPT = """你是一个本体分析助手。请分析用户的输入，提取其中的实体和关系。

当前已知的实体：{existing_entities}

用户的输入：{user_input}

请分析并返回JSON格式：
{{
  "entities": [
    {{"name": "实体名称", "type": "类型", "description": "描述"}}
  ],
  "relations": [
    {{"source": "源实体", "target": "目标实体", "type": "关系类型", "description": "描述"}}
  ],
  "response": "对用户的自然语言回复"
}}

注意：
1. 如果实体已存在，不要重复添加
2. 关系必须在已存在的实体之间建立
3. response 字段是你的对话回复，要友好自然
4. 实体类型：person(人物)、concept(概念)、process(流程)、object(物体)、event(事件)
5. 关系类型：依赖、包含、导致、关联、属于、产生
"""


async def stream_chat_analysis(
    messages: List[ChatMessage],
    ai_config: AIConfig,
    existing_entities: List[str]
) -> AsyncGenerator[str, None]:
    """
    流式分析对话，逐步返回结果
    
    事件类型：
    - event: content: 文本回复内容
    - event: entities: 提取的实体列表
    - event: relations: 提取的关系列表  
    - event: complete: 完成
    """
    
    # 构造最终的用户输入（最后一条消息）
    user_input = messages[-1].content if messages else ""
    
    # 构造系统提示词
    system_prompt = DIALOG_PROMPT.format(
        existing_entities=", ".join(existing_entities) if existing_entities else "无",
        user_input=user_input
    )
    
    # 构造 messages
    chat_messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # 添加历史对话上下文
    for msg in messages:
        chat_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    # 获取适配器
    adapter = get_adapter(
        ai_config.model_name,
        api_key=ai_config.api_key,
        api_endpoint=ai_config.api_endpoint,
        model_id=ai_config.model_id
    )
    
    try:
        # 尝试流式调用（如果模型支持）
        if hasattr(adapter, 'chat_stream'):
            async for chunk in adapter.chat_stream(chat_messages):
                yield f"event: content\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        else:
            # 非流式调用，返回完整结果
            # 使用 analyze 方法，但构造合适的 prompt
            full_prompt = system_prompt
            result = await adapter.analyze(
                content=user_input,
                content_type="text",
                prompt=full_prompt
            )
            
            # 解析结果
            if isinstance(result, dict):
                response_text = result.get('response', '')
                entities = result.get('entities', [])
                relations = result.get('relations', [])
                
                # 模拟流式返回文本
                if response_text:
                    for char in response_text:
                        yield f"event: content\ndata: {json.dumps({'content': char}, ensure_ascii=False)}\n\n"
                        await asyncio.sleep(0.01)  # 模拟打字效果
                
                # 返回实体
                if entities:
                    yield f"event: entities\ndata: {json.dumps({'entities': entities}, ensure_ascii=False)}\n\n"
                
                # 返回关系
                if relations:
                    yield f"event: relations\ndata: {json.dumps({'relations': relations}, ensure_ascii=False)}\n\n"
        
        # 发送完成事件
        yield f"event: complete\ndata: {json.dumps({'status': 'done'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"


@router.post("/stream")
async def chat_stream_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """流式对话分析接口（SSE）"""
    
    from sqlalchemy import select
    
    # 获取AI配置
    result = await db.execute(
        select(AIConfig).where(
            AIConfig.id == request.ai_config_id,
            AIConfig.user_id == current_user.id
        )
    )
    ai_config = result.scalar_one_or_none()
    
    if not ai_config:
        raise HTTPException(status_code=404, detail="AI配置不存在")
    
    # 返回 SSE 流
    return StreamingResponse(
        stream_chat_analysis(
            messages=request.messages,
            ai_config=ai_config,
            existing_entities=[]  # 可以传入当前已有的实体名称列表
        ),
        media_type="text/event-stream"
    )


@router.post("/analyze")
async def chat_analyze_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """非流式对话分析接口，返回完整分析结果"""
    
    from sqlalchemy import select
    
    # 获取AI配置
    result = await db.execute(
        select(AIConfig).where(
            AIConfig.id == request.ai_config_id,
            AIConfig.user_id == current_user.id
        )
    )
    ai_config = result.scalar_one_or_none()
    
    if not ai_config:
        raise HTTPException(status_code=404, detail="AI配置不存在")
    
    # 获取最后一条用户输入
    user_input = request.messages[-1].content if request.messages else ""
    existing_entities = []  # 可以传入当前已有的实体
    
    # 构造提示词
    system_prompt = DIALOG_PROMPT.format(
        existing_entities=", ".join(existing_entities) if existing_entities else "无",
        user_input=user_input
    )
    
    # 获取适配器
    adapter = get_adapter(
        ai_config.model_name,
        api_key=ai_config.api_key,
        api_endpoint=ai_config.api_endpoint,
        model_id=ai_config.model_id
    )
    
    try:
        # 调用AI分析
        result = await adapter.analyze(
            content=user_input,
            content_type="text",
            prompt=system_prompt
        )
        
        # 解析返回结果
        if isinstance(result, dict):
            return {
                "response": result.get('response', ''),
                "entities": result.get('entities', []),
                "relations": result.get('relations', [])
            }
        else:
            return {
                "response": str(result),
                "entities": [],
                "relations": []
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
