-- OntologyFlow 数据库建表脚本
-- PostgreSQL

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户AI配置表
CREATE TABLE IF NOT EXISTS ai_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL,
    api_key TEXT,
    api_endpoint TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 项目表
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    default_model_config_id INTEGER REFERENCES ai_configs(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据源表
CREATE TABLE IF NOT EXISTS data_sources (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,
    file_path TEXT,
    content TEXT,
    file_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 分析任务表
CREATE TABLE IF NOT EXISTS analysis_tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    data_source_id INTEGER REFERENCES data_sources(id) ON DELETE CASCADE,
    ai_config_id INTEGER REFERENCES ai_configs(id),
    status VARCHAR(20) DEFAULT 'pending',
    raw_output TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 实体表
CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES analysis_tasks(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50),
    description TEXT,
    properties JSONB,
    position_x FLOAT,
    position_y FLOAT,
    is_user_created BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 关系表
CREATE TABLE IF NOT EXISTS relations (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES analysis_tasks(id) ON DELETE CASCADE,
    source_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    target_entity_id INTEGER REFERENCES entities(id) ON DELETE CASCADE,
    relation_type VARCHAR(100),
    description TEXT,
    is_user_created BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_projects_user ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_data_sources_project ON data_sources(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_project ON analysis_tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_entities_task ON entities(task_id);
CREATE INDEX IF NOT EXISTS idx_relations_task ON relations(task_id);
CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_entity_id);