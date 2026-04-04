# OntologyFlow - 本体关系分析平台

从图片、视频、文字中提取实体与关系，构建知识图谱。

## 技术栈

- **前端**: Vue 3 + Vite + TypeScript + AntV X6
- **后端**: Python FastAPI
- **数据库**: PostgreSQL
- **AI**: 支持多种大模型 (Claude, GPT, Gemini, GLM, Qwen, DeepSeek 等)

## 快速开始

### 1. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置数据库连接

# 前端
cd frontend
npm install
```

### 2. 创建数据库

```bash
# PostgreSQL 中创建数据库
createdb ontology_flow

# 或使用 psql 执行
psql -U postgres -f docs/database/schema.sql
```

### 3. 启动服务

```bash
# 启动后端
cd backend
uvicorn app.main:app --reload --port 8000

# 启动前端
cd frontend
npm run dev
```

### 4. 访问应用

- 前端: http://localhost:3000
- API文档: http://localhost:8000/docs

## 功能

- 上传图片/视频/文字数据
- AI 自动识别实体和关系
- 数据血缘风格图谱展示
- 图谱编辑和导出
- 多用户隔离