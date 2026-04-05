from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.routers import (
    auth_router,
    ai_configs_router,
    projects_router,
    data_sources_router,
    tasks_router,
    graph_router,
    analyze_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield


app = FastAPI(
    title="OntologyFlow API",
    description="本体关系分析平台 API",
    version="0.1.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001",
        "http://localhost:5173", "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(ai_configs_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(data_sources_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(graph_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "OntologyFlow API", "docs": "/docs"}