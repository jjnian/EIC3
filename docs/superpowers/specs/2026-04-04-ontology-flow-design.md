# OntologyFlow - 本体关系分析平台设计文档

> 创建日期：2026-04-04

## 一、系统概述

### 1.1 系统名称
**OntologyFlow** - 本体关系分析平台

### 1.2 核心功能
用户上传图片/视频/文字，AI自动识别其中的实体（本体）和关系，以数据血缘风格的层级流向图展示，用户可编辑、审核、导出结果。

### 1.3 目标用户
需要从多源数据中提取知识结构的研究者、分析师、知识工作者。

### 1.4 系统类型
公开平台，支持多用户注册使用，需要账户管理和数据隔离。

---

## 二、技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TypeScript + AntV X6 |
| 后端 | Python (FastAPI) |
| 数据库 | PostgreSQL |
| AI接口 | 支持多模型（Claude、GPT、Gemini、GLM、Qwen、DeepSeek等） |

---

## 三、系统架构

```
┌─────────────────────────────────────┐
│           Vue 3 前端                │
│  ┌─────────┬─────────┬───────────┐  │
│  │ 文件上传 │ 图谱展示 │ 编辑导出 │  │
│  └─────────┴─────────┴───────────┘  │
├─────────────────────────────────────┤
│        FastAPI 后端服务              │
│  ┌─────────┬─────────┬───────────┐  │
│  │ 用户认证 │ AI调度 │ 数据管理  │  │
│  └─────────┴─────────┴───────────┘  │
├─────────────────────────────────────┤
│          PostgreSQL                 │
│  ┌─────────────────────────────┐    │
│  │ 用户、项目、实体、关系数据   │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### AI模型集成方式
- 后端统一管理API调用
- 用户在前端选择模型并配置API Key
- 支持扩展新模型（插件式适配器架构）

---

## 四、核心模块设计

### 4.1 用户模块
- 注册/登录（支持邮箱注册）
- 用户配置：管理AI模型的API Key（各模型独立配置）
- 数据隔离：每个用户的项目和数据互不可见

### 4.2 项目管理模块
- 创建项目：名称、描述、选择的默认AI模型
- 项目列表：查看、搜索、删除
- 项目内包含多个分析任务

### 4.3 数据输入模块
- 支持格式：
  - 图片：PNG、JPG、SVG
  - 视频：MP4、WebM（提取关键帧分析）
  - 文字：TXT、Markdown、直接输入
- 文件上传：拖拽上传、批量上传
- 存储方式：PostgreSQL记录 + 本地文件存储

### 4.4 AI分析模块
- 任务调度：创建分析任务，选择模型
- 结果解析：统一解析各AI输出的实体和关系
- 结果存储：保存到数据库，支持复用和修改
- 任务状态：pending（排队中）、running（分析中）、completed（已完成）、failed（失败）

### 4.5 图谱展示与编辑模块（核心）
- X6可视化：层级化血缘图风格展示
- 交互功能：
  - 拖拽节点调整位置
  - 点击查看实体详情
  - 添加/删除/修改实体
  - 添加/删除/修改关系连线
  - 搜索和筛选节点
- 实时同步：编辑后自动保存到数据库

### 4.6 导出模块
- 图谱导出：PNG图片、JSON数据、CSV表格
- 支持标准格式：兼容Neo4j、Gephi导入格式

---

## 五、数据库设计

### PostgreSQL 表结构

```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户AI配置表（每个用户可配置多个模型）
CREATE TABLE ai_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL,  -- claude, openai, gemini, glm, qwen, deepseek, local
    api_key TEXT,  -- 加密存储
    api_endpoint TEXT,  -- 自定义端点，支持本地模型
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 项目表
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    default_model_config_id INTEGER REFERENCES ai_configs(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据源表（上传的文件/文字）
CREATE TABLE data_sources (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,  -- image, video, text
    file_path TEXT,  -- 文件存储路径，文字类型为空
    content TEXT,  -- 文字内容，文件类型为空
    file_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 分析任务表
CREATE TABLE analysis_tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    data_source_id INTEGER REFERENCES data_sources(id) ON DELETE CASCADE,
    ai_config_id INTEGER REFERENCES ai_configs(id),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, running, completed, failed
    raw_output TEXT,  -- AI原始返回结果
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 实体表（本体）
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES analysis_tasks(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50),  -- person, concept, process, object, event
    description TEXT,
    properties JSONB,  -- 扩展属性
    position_x FLOAT,
    position_y FLOAT,
    is_user_created BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 关系表
CREATE TABLE relations (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES analysis_tasks(id) ON DELETE CASCADE,
    source_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    target_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    relation_type VARCHAR(100),  -- 依赖, 包含, 导致, 关联, 属于, 产生
    description TEXT,
    is_user_created BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_data_sources_project ON data_sources(project_id);
CREATE INDEX idx_tasks_project ON analysis_tasks(project_id);
CREATE INDEX idx_entities_task ON entities(task_id);
CREATE INDEX idx_relations_task ON relations(task_id);
CREATE INDEX idx_relations_source ON relations(source_entity_id);
CREATE INDEX idx_relations_target ON relations(target_entity_id);
```

---

## 六、API接口设计

### 6.1 认证相关 `/api/auth`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/register` | POST | 用户注册 |
| `/login` | POST | 登录，返回JWT |
| `/me` | GET | 获取当前用户信息 |

### 6.2 AI配置相关 `/api/ai-configs`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 获取用户的AI配置列表 |
| `/` | POST | 添加新的AI配置 |
| `/{id}` | PUT | 更新配置 |
| `/{id}` | DELETE | 删除配置 |

### 6.3 项目相关 `/api/projects`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 获取项目列表 |
| `/` | POST | 创建项目 |
| `/{id}` | GET | 获取项目详情 |
| `/{id}` | PUT | 更新项目 |
| `/{id}` | DELETE | 删除项目 |

### 6.4 数据源相关 `/api/data-sources`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/upload` | POST | 上传文件 |
| `/` | GET | 获取项目内数据源列表 |
| `/{id}` | DELETE | 删除数据源 |

### 6.5 分析任务相关 `/api/tasks`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | POST | 创建分析任务 |
| `/` | GET | 获取任务列表 |
| `/{id}` | GET | 获取任务详情和结果 |
| `/{id}/status` | GET | 查询任务状态（轮询） |

### 6.6 图谱操作相关 `/api/graph`
| 接口 | 方法 | 说明 |
|------|------|------|
| `/entities` | GET | 获取任务的所有实体 |
| `/entities` | POST | 新增实体 |
| `/entities/{id}` | PUT | 更新实体 |
| `/entities/{id}` | DELETE | 删除实体 |
| `/relations` | GET | 获取任务的所有关系 |
| `/relations` | POST | 新增关系 |
| `/relations/{id}` | PUT | 更新关系 |
| `/relations/{id}` | DELETE | 删除关系 |
| `/export` | POST | 导出图谱（指定格式：png/json/csv） |

---

## 七、前端页面设计

### 7.1 页面路由结构
```
/                   → 首页（产品介绍、快速开始）
/login              → 登录页
/register           → 注册页
/dashboard          → 用户仪表盘（项目列表、创建项目）
/settings           → 设置页（AI模型配置）
/project/:id        → 项目详情页（左侧菜单+图谱编辑器）
```

### 7.2 项目详情页布局（核心页面）

```
┌──────────┬───────────────────────────────────────────────┐
│ 数据血缘 │  顶部工具栏                                   │
│ (左侧菜单)│  [项目名]  [任务选择▼]  [模型选择▼]  [导出▼]  │
├──────────┼───────────────────────────────────────────────┤
│ ┌──────┐ │                                               │
│ │数据源│ │                                               │
│ └──────┘ │                                               │
│ ┌──────┐ │         X6 图谱区域                           │
│ │任务  │ │       (主体可视化)                            │
│ └──────┘ │                                               │
│ ┌──────┐ │       支持拖拽、缩放、编辑                    │
│ │图谱  │ │                                               │
│ └──────┘ │                                               │
│ ┌──────┐ │                                               │
│ │设置  │ │                                               │
│ └──────┘ │                                               │
│          │                                               │
│ ┌──────┐ │                                               │
│ │新建  │ │                                               │
│ │分析  │ │                                               │
│ └──────┘ │                                               │
├──────────┴───────────────────────────────────────────────┤
│  底部状态栏: 实体数: 12  关系数: 8  最后保存: 14:32       │
└─────────────────────────────────────────────────────────┘
```

### 7.3 左侧菜单项
| 菜单项 | 功能 |
|--------|------|
| 数据源 | 上传文件、查看已上传的图片/视频/文字列表 |
| 任务 | 创建分析任务、查看任务状态和列表 |
| 图谱 | 进入图谱编辑器（默认选中） |
| 设置 | 项目设置、默认模型选择 |
| 新建分析 | 快速创建新的分析任务（快捷入口） |

### 7.4 前端关键组件
- **GraphEditor.vue** - X6图谱核心组件
- **FileUploader.vue** - 文件上传组件（支持拖拽）
- **TaskCard.vue** - 任务状态卡片
- **EntityPanel.vue** - 实体详情/编辑面板
- **ModelSelector.vue** - AI模型选择器
- **ExportDialog.vue** - 导出格式选择弹窗
- **SideMenu.vue** - 左侧"数据血缘"菜单

---

## 八、AI分析流程设计

### 8.1 任务执行流程
```
用户选择数据源 + AI模型
        ↓
    创建任务（status: pending）
        ↓
后端获取AI配置 → 调用对应API → 发送数据+提示词
        ↓
    AI返回结果（status: running → completed）
        ↓
后端解析结果 → 提取实体和关系 → 存入 entities/relations 表
        ↓
前端获取结果 → X6渲染图谱
```

### 8.2 AI提示词模板（统一格式）
```
请分析以下内容，提取其中的实体（本体）和它们之间的关系。

内容类型：{image/video/text}

请按以下JSON格式返回：
{
  "entities": [
    {"name": "实体名称", "type": "类型", "description": "描述"}
  ],
  "relations": [
    {"source": "源实体名称", "target": "目标实体名称", "type": "关系类型", "description": "描述"}
  ]
}

实体类型建议：person(人物)、concept(概念)、process(流程)、object(物体)、event(事件)
关系类型建议：依赖、包含、导致、关联、属于、产生
```

### 8.3 多模型适配层架构

```python
# 统一接口定义
class AIModelAdapter:
    def analyze(self, data_source, prompt_template) -> dict:
        """统一分析方法，返回实体和关系"""
        pass

# 各模型适配器实现
class ClaudeAdapter(AIModelAdapter): ...
class OpenAIAdapter(AIModelAdapter): ...
class GeminiAdapter(AIModelAdapter): ...
class GLMAdapter(AIModelAdapter): ...
class QwenAdapter(AIModelAdapter): ...
class DeepSeekAdapter(AIModelAdapter): ...
class DoubaoAdapter(AIModelAdapter): ...
class YiAdapter(AIModelAdapter): ...
class MoonshotAdapter(AIModelAdapter): ...
class LocalModelAdapter(AIModelAdapter): ...

# 模型工厂
def get_adapter(model_name, config) -> AIModelAdapter:
    adapters = {
        "claude": ClaudeAdapter,
        "openai": OpenAIAdapter,
        "gemini": GeminiAdapter,
        "glm": GLMAdapter,
        "qwen": QwenAdapter,
        "deepseek": DeepSeekAdapter,
        "doubao": DoubaoAdapter,
        "yi": YiAdapter,
        "moonshot": MoonshotAdapter,
        "local": LocalModelAdapter,
    }
    return adapters.get(model_name, LocalModelAdapter)(config)
```

### 8.4 支持的AI模型列表

| 模型 | 提供方 | SDK/API方式 |
|------|--------|-------------|
| Claude | Anthropic | anthropic SDK |
| GPT-4V / GPT-4o | OpenAI | openai SDK |
| Gemini | Google | google-generativeai SDK |
| GLM-4V | 智谱AI | zhipuai SDK / HTTP API |
| Qwen-VL | 阿里云百炼 | dashscope SDK / HTTP API |
| DeepSeek | DeepSeek | HTTP API (兼容OpenAI格式) |
| Doubao | 字节跳动 | HTTP API |
| Yi-Vision | 零一万物 | HTTP API |
| Moonshot | Kimi | HTTP API (兼容OpenAI格式) |
| 本地模型 | 用户自部署 | 自定义HTTP端点 |

---

## 九、待实现功能清单

### Phase 1 - 基础框架
- [ ] 前端项目初始化（Vue 3 + Vite + TypeScript）
- [ ] 后端项目初始化（FastAPI）
- [ ] PostgreSQL数据库表创建
- [ ] 用户注册/登录功能
- [ ] JWT认证中间件

### Phase 2 - 核心功能
- [ ] AI模型配置管理
- [ ] 项目创建与管理
- [ ] 文件上传功能
- [ ] 分析任务创建与调度
- [ ] AI模型适配器实现（至少2个模型）

### Phase 3 - 图谱功能
- [ ] X6图谱渲染
- [ ] 节点拖拽与编辑
- [ ] 实体/关系的增删改
- [ ] 数据血缘风格布局

### Phase 4 - 导出与优化
- [ ] 图谱导出（PNG/JSON/CSV）
- [ ] 任务状态轮询优化
- [ ] 性能优化
- [ ] 错误处理完善