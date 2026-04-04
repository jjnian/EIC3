import json
import csv
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, Project, AnalysisTask, Entity, Relation
from app.schemas import EntityCreate, EntityUpdate, EntityResponse, RelationCreate, RelationUpdate, RelationResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/graph", tags=["图谱"])


# ===== 实体相关 =====

@router.get("/entities", response_model=list[EntityResponse])
async def get_entities(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证任务存在
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.id == task_id,
            Project.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="任务不存在")

    result = await db.execute(select(Entity).where(Entity.task_id == task_id))
    return result.scalars().all()


@router.post("/entities", response_model=EntityResponse)
async def create_entity(
    entity_data: EntityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 验证任务存在
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.id == entity_data.task_id,
            Project.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="任务不存在")

    entity = Entity(
        task_id=entity_data.task_id,
        name=entity_data.name,
        type=entity_data.type,
        description=entity_data.description,
        properties=entity_data.properties,
        position_x=entity_data.position_x,
        position_y=entity_data.position_y,
        is_user_created=entity_data.is_user_created
    )
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


@router.put("/entities/{entity_id}", response_model=EntityResponse)
async def update_entity(
    entity_id: int,
    entity_data: EntityUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Entity).join(AnalysisTask).join(Project).where(
            Entity.id == entity_id,
            Project.user_id == current_user.id
        )
    )
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="实体不存在")

    if entity_data.name is not None:
        entity.name = entity_data.name
    if entity_data.type is not None:
        entity.type = entity_data.type
    if entity_data.description is not None:
        entity.description = entity_data.description
    if entity_data.properties is not None:
        entity.properties = entity_data.properties
    if entity_data.position_x is not None:
        entity.position_x = entity_data.position_x
    if entity_data.position_y is not None:
        entity.position_y = entity_data.position_y

    await db.commit()
    await db.refresh(entity)
    return entity


@router.delete("/entities/{entity_id}")
async def delete_entity(
    entity_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Entity).join(AnalysisTask).join(Project).where(
            Entity.id == entity_id,
            Project.user_id == current_user.id
        )
    )
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="实体不存在")

    await db.delete(entity)
    await db.commit()
    return {"message": "删除成功"}


# ===== 关系相关 =====

@router.get("/relations", response_model=list[RelationResponse])
async def get_relations(
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
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="任务不存在")

    result = await db.execute(select(Relation).where(Relation.task_id == task_id))
    return result.scalars().all()


@router.post("/relations", response_model=RelationResponse)
async def create_relation(
    relation_data: RelationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.id == relation_data.task_id,
            Project.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="任务不存在")

    relation = Relation(
        task_id=relation_data.task_id,
        source_entity_id=relation_data.source_entity_id,
        target_entity_id=relation_data.target_entity_id,
        relation_type=relation_data.relation_type,
        description=relation_data.description,
        is_user_created=relation_data.is_user_created
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


@router.put("/relations/{relation_id}", response_model=RelationResponse)
async def update_relation(
    relation_id: int,
    relation_data: RelationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Relation).join(AnalysisTask).join(Project).where(
            Relation.id == relation_id,
            Project.user_id == current_user.id
        )
    )
    relation = result.scalar_one_or_none()
    if not relation:
        raise HTTPException(status_code=404, detail="关系不存在")

    if relation_data.source_entity_id is not None:
        relation.source_entity_id = relation_data.source_entity_id
    if relation_data.target_entity_id is not None:
        relation.target_entity_id = relation_data.target_entity_id
    if relation_data.relation_type is not None:
        relation.relation_type = relation_data.relation_type
    if relation_data.description is not None:
        relation.description = relation_data.description

    await db.commit()
    await db.refresh(relation)
    return relation


@router.delete("/relations/{relation_id}")
async def delete_relation(
    relation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Relation).join(AnalysisTask).join(Project).where(
            Relation.id == relation_id,
            Project.user_id == current_user.id
        )
    )
    relation = result.scalar_one_or_none()
    if not relation:
        raise HTTPException(status_code=404, detail="关系不存在")

    await db.delete(relation)
    await db.commit()
    return {"message": "删除成功"}


# ===== 导出相关 =====

@router.post("/export")
async def export_graph(
    task_id: int,
    format: str = "json",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AnalysisTask).join(Project).where(
            AnalysisTask.id == task_id,
            Project.user_id == current_user.id
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="任务不存在")

    # 获取实体和关系
    result = await db.execute(select(Entity).where(Entity.task_id == task_id))
    entities = result.scalars().all()

    result = await db.execute(select(Relation).where(Relation.task_id == task_id))
    relations = result.scalars().all()

    if format == "json":
        data = {
            "entities": [
                {"id": e.id, "name": e.name, "type": e.type, "description": e.description}
                for e in entities
            ],
            "relations": [
                {
                    "id": r.id,
                    "source": r.source_entity_id,
                    "target": r.target_entity_id,
                    "type": r.relation_type,
                    "description": r.description
                }
                for r in relations
            ]
        }
        return data

    elif format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)

        # 写入实体
        writer.writerow(["entities"])
        writer.writerow(["id", "name", "type", "description"])
        for e in entities:
            writer.writerow([e.id, e.name, e.type or "", e.description or ""])

        writer.writerow([])
        writer.writerow(["relations"])
        writer.writerow(["id", "source_id", "target_id", "type", "description"])
        for r in relations:
            writer.writerow([r.id, r.source_entity_id, r.target_entity_id, r.relation_type or "", r.description or ""])

        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=graph_{task_id}.csv"}
        )

    elif format == "png":
        # PNG导出需要前端使用X6的toPNG方法
        return {"message": "请使用前端导出PNG功能"}

    else:
        raise HTTPException(status_code=400, detail="不支持的导出格式")