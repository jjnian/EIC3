import asyncio
import base64
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, Project, DataSource, AnalysisTask, AIConfig, Entity, Relation, TaskStatus
from app.schemas import TaskCreate, TaskResponse
from app.services.auth import get_current_user
from app.adapters import get_adapter, DEFAULT_PROMPT

router = APIRouter(prefix="/tasks", tags=["分析任务"])


async def run_analysis(task_id: int, data_source_id: int, ai_config_id: int, db_url: str):
    """后台执行分析任务"""
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

    engine = create_async_engine(db_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        try:
            # 更新任务状态
            result = await db.execute(select(AnalysisTask).where(AnalysisTask.id == task_id))
            task = result.scalar_one_or_none()
            if not task:
                return

            task.status = TaskStatus.running
            await db.commit()

            # 获取数据源
            result = await db.execute(select(DataSource).where(DataSource.id == data_source_id))
            data_source = result.scalar_one_or_none()
            if not data_source:
                task.status = TaskStatus.failed
                task.error_message = "数据源不存在"
                await db.commit()
                return

            # 获取AI配置
            result = await db.execute(select(AIConfig).where(AIConfig.id == ai_config_id))
            ai_config = result.scalar_one_or_none()
            if not ai_config:
                task.status = TaskStatus.failed
                task.error_message = "AI配置不存在"
                await db.commit()
                return

            # 准备内容
            content = ""
            content_type = data_source.type

            if data_source.type == "text":
                content = data_source.content or ""
            else:
                # 读取文件并转base64
                if data_source.file_path:
                    with open(data_source.file_path, "rb") as f:
                        content = base64.b64encode(f.read()).decode()

            # 调用AI模型
            adapter = get_adapter(
                ai_config.model_name,
                api_key=ai_config.api_key,
                api_endpoint=ai_config.api_endpoint
            )

            prompt = DEFAULT_PROMPT.format(content_type=content_type)
            result_data = await adapter.analyze(content, content_type, prompt)

            # 保存结果
            task.raw_output = str(result_data)

            # 保存实体
            entities_map = {}
            for entity_data in result_data.get("entities", []):
                entity = Entity(
                    task_id=task_id,
                    name=entity_data.get("name", ""),
                    type=entity_data.get("type"),
                    description=entity_data.get("description")
                )
                db.add(entity)
                await db.flush()
                entities_map[entity.name] = entity.id

            # 保存关系
            for relation_data in result_data.get("relations", []):
                source_name = relation_data.get("source")
                target_name = relation_data.get("target")

                if source_name in entities_map and target_name in entities_map:
                    relation = Relation(
                        task_id=task_id,
                        source_entity_id=entities_map[source_name],
                        target_entity_id=entities_map[target_name],
                        relation_type=relation_data.get("type"),
                        description=relation_data.get("description")
                    )
                    db.add(relation)

            task.status = TaskStatus.completed
            task.completed_at = datetime.utcnow()
            await db.commit()

        except Exception as e:
            async with async_session() as db:
                result = await db.execute(select(AnalysisTask).where(AnalysisTask.id == task_id))
                task = result.scalar_one_or_none()
                if task:
                    task.status = TaskStatus.failed
                    task.error_message = str(e)
                    await db.commit()


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证项目存在
    result = await db.execute(
        select(Project).where(Project.id == task_data.project_id, Project.user_id == current_user.id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 验证数据源存在
    result = await db.execute(
        select(DataSource).where(DataSource.id == task_data.data_source_id, DataSource.project_id == task_data.project_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="数据源不存在")

    # 创建任务
    task = AnalysisTask(
        project_id=task_data.project_id,
        data_source_id=task_data.data_source_id,
        ai_config_id=task_data.ai_config_id
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    # 后台执行分析
    from app.config import settings
    background_tasks.add_task(
        run_analysis,
        task.id,
        task_data.data_source_id,
        task_data.ai_config_id,
        settings.DATABASE_URL
    )

    return task


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.project_id == project_id,
            Project.user_id == current_user.id
        )
    )
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.id == task_id,
            Project.user_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task