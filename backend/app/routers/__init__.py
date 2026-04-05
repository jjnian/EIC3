from .auth import router as auth_router
from .ai_configs import router as ai_configs_router
from .projects import router as projects_router
from .data_sources import router as data_sources_router
from .tasks import router as tasks_router
from .graph import router as graph_router
from .analyze import router as analyze_router

__all__ = [
    "auth_router",
    "ai_configs_router",
    "projects_router",
    "data_sources_router",
    "tasks_router",
    "graph_router",
    "analyze_router"
]