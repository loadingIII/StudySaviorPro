# StudySaviorPro

基于 FastAPI + LangChain 构建的 AI 学习助手后端服务，支持 RAG 知识库问答、智能出题、流式对话等功能。

## 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| AI / LLM | LangChain、通义千问（Qwen） |
| 向量数据库 | ChromaDB |
| 关系数据库 | PostgreSQL (asyncpg + SQLAlchemy) |
| 缓存 / 记忆 | Redis |
| 认证 | JWT |

## 项目结构

```
StudySaviorPro/
├── main.py                  # 应用入口
├── agent/                   # AI Agent 核心
│   ├── agent.py             # Agent 调度逻辑
│   ├── llms/                # LLM 封装（Qwen / Zip）
│   ├── memory/              # 对话记忆（Redis / PostgreSQL）
│   ├── prompts/             # Prompt 模板
│   ├── rag/                 # RAG 检索增强
│   ├── smart_question/      # 智能出题
│   └── tool/                # 自定义工具
├── crud/                    # 数据库 CRUD 操作
├── middleware/              # JWT 中间件
├── model/                   # SQLAlchemy 数据模型
├── properties/              # 配置文件（数据库、向量库）
├── router/                  # API 路由
│   ├── agent_router.py      # Agent 相关接口
│   ├── user_router.py       # 用户接口
│   └── vector_store_router.py # 知识库接口
├── schemas/                 # Pydantic 数据模式
├── test/                    # 测试
└── utils/                   # 工具类（JWT、DB、日志等）
```

## API 接口

### Agent（`/agent`）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/agent/question/invoke` | 同步问答 |
| POST | `/agent/question/stream` | 流式问答（SSE） |
| GET  | `/agent/question/get_new_session_id` | 获取新会话 ID |
| GET  | `/agent/question/get_chat_sessions` | 获取所有会话列表 |
| GET  | `/agent/question/get_chat_history/{session_id}` | 获取会话历史记录 |
| POST | `/agent/question/generate_question` | 智能出题 |
| GET  | `/agent/question/get_user_generated_questions` | 获取用户已生成题目 |

### 向量知识库（`/vector`）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST   | `/vector/add_documents` | 上传文件到知识库 |
| GET    | `/vector/get_all_files` | 获取所有知识库文件 |
| DELETE | `/vector/delete_file/{file_id}` | 删除知识库文件 |

### 用户（`/user`）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/user/login` | 用户登录 |

## 代码统计

> 统计范围：项目所有 `.py` 源文件（不含测试框架、第三方依赖及自动生成文件）。

| 模块 | 文件 | 行数 |
|------|------|-----:|
| utils | `utils/file_handler.py` | 180 |
| crud | `crud/ai_response_service.py` | 159 |
| crud | `crud/vector_store_service.py` | 111 |
| router | `router/agent_router.py` | 97 |
| agent/rag | `agent/rag/vector_store.py` | 93 |
| agent/smart_question | `agent/smart_question/ai_response.py` | 82 |
| model | `model/Question.py` | 78 |
| agent | `agent/agent.py` | 71 |
| model | `model/FileInfo.py` | 69 |
| utils | `utils/jwtUtils.py` | 60 |
| utils | `utils/logger_handler.py` | 59 |
| agent/tool | `agent/tool/base_tool.py` | 49 |
| agent/rag | `agent/rag/rag_service.py` | 49 |
| middleware | `middleware/jwtMiddleware.py` | 48 |
| agent/llms | `agent/llms/zip_llms.py` | 45 |
| router | `router/vector_store_router.py` | 40 |
| utils | `utils/dbUtils.py` | 36 |
| model | `model/Users.py` | 32 |
| utils | `utils/configUtils.py` | 31 |
| utils | `utils/prompt_loader.py` | 30 |
| crud | `crud/user_service.py` | 28 |
| agent/llms | `agent/llms/llms.py` | 27 |
| model | `model/ChatHistory.py` | 26 |
| schemas | `schemas/agent_schemas.py` | 25 |
| agent/llms | `agent/llms/qwen_llm.py` | 24 |
| utils | `utils/path_tool.py` | 23 |
| utils | `utils/envUtils.py` | 22 |
| router | `router/user_router.py` | 21 |
| agent/memory | `agent/memory/pg_memory.py` | 21 |
| agent/memory | `agent/memory/redis_memory.py` | 19 |
| schemas | `schemas/result.py` | 17 |
| — | `main.py` | 16 |
| schemas | `schemas/quesion_schemas.py` | 15 |
| utils | `utils/threadUtils.py` | 14 |
| test | `test/test1.py` | 14 |
| schemas | `schemas/user_schemas.py` | 13 |
| schemas | `schemas/file_schemas.py` | 9 |
| model | `model/base.py` | 8 |
| **合计** | **38 个 .py 文件** | **1,761** |

**项目 Python 源码共计 1,761 行。**
