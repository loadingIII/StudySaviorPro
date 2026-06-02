# StudySaviorPro — AI 期末复习学习助手

> 一个基于 **FastAPI + Vue 3 + LangChain** 的 AI 学习助手，采用多智能体架构（Agent-as-Tool 模式），支持知识库检索（RAG）、联网搜索、智能出题和对话式答题。

<img width="1799" height="1160" alt="屏幕截图 2026-03-21 144130" src="https://github.com/user-attachments/assets/f1b9afe3-2286-4e7a-8fba-18a3c9eb5232" />
<img width="1808" height="1169" alt="2dade7b26b40786aae459483ab46ed99" src="https://github.com/user-attachments/assets/7ad80697-52af-4e92-a466-96b7db570f75" />
<img width="1793" height="1165" alt="6e9e099ab6f17f54b1734104a69e1363" src="https://github.com/user-attachments/assets/57ad410c-2de6-4ca5-84b0-694e23b8eaaf" />

---

## 功能特性

| 功能 | 描述 |
|------|------|
| **智能问答** | 基于知识库（RAG）和联网搜索，回答课程相关问题 |
| **知识库管理** | 上传 PDF / TXT / DOCX 文档，自动分块、压缩、向量化存储 |
| **RAG 检索增强** | 多查询扩展 + 去重 + RRF 重排序，精准检索 Top-K 相关片段 |
| **联网搜索** | 通过智谱 API 进行实时网络搜索，补充知识库未覆盖的内容 |
| **智能出题** | 支持选择题、填空题、判断题、主观题四种题型 |
| **会话管理** | 多会话支持，历史对话存储，可追溯和删除 |
| **JWT 认证** | 手机号 + 密码登录，Token 鉴权 |

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                          FastAPI                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐  │
│  │ Agent    │  │ User     │  │ Vector Store             │  │
│  │ Router   │  │ Router   │  │ Router                   │  │
│  └────┬─────┘  └──────────┘  └──────────────────────────┘  │
│       │                                                     │
│  ┌────▼─────────────────────────────────────────────────┐  │
│  │              Supervisor Agent (路由主管)               │  │
│  │  ┌─────────────────┐    ┌────────────────────────┐   │  │
│  │  │  context_agent   │    │   question_agent       │   │  │
│  │  │  (RAG + Web)     │    │   (智能出题)            │   │  │
│  │  └────────┬────────┘    └───────────┬────────────┘   │  │
│  │           │                         │                 │  │
│  │     ┌─────▼──────┐          ┌───────▼────────┐      │  │
│  │     │ RAG 检索    │          │ 选择题/填空/    │      │  │
│  │     │ Web Search  │          │ 判断/主观题     │      │  │
│  │     └─────────────┘          └────────────────┘      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 多智能体架构 (Agent-as-Tool)

系统采用 **Supervisor + Sub-Agent 模式**：

1. **Supervisor Agent** — 接收用户问题，根据意图路由到 `context_agent` 或 `question_agent`
2. **context_agent** — 同时从知识库（RAG）和互联网搜索获取上下文信息，融合后返回精炼摘要
3. **question_agent** — 基于知识库内容或网络信息，生成指定类型和数量的练习题

### RAG 流程

```
用户查询 → LLM 查询扩展(3变体) → ChromaDB 检索 → 去重 → RRF 重排序 → 上下文组装
```

---

## 项目结构

```
StudySaviorPro/
├── main.py                      # FastAPI 入口，注册路由和 JWT 中间件
├── requirements.txt             # Python 依赖
├── .env / .env.example          # 环境变量配置
├── CLAUDE.md                    # 项目指引
│
├── agent/                       # 多智能体系统核心
│   ├── agent.py                 # 对外接口 (agent_invoke / agent_stream)
│   ├── sub_agents/              # 子智能体
│   │   ├── supervisor.py        # 主管 Agent，路由分发
│   │   ├── context_agent.py     # 上下文检索 Agent (RAG + WebSearch)
│   │   └── question_agent.py    # 智能出题 Agent
│   ├── llms/                    # LLM 实例配置
│   │   ├── llms.py              # ChatOpenAI 实例 (chat/think/question/query)
│   │   └── zip_llms.py          # 文本压缩 LLM
│   ├── rag/                     # RAG 流水线
│   │   ├── vector_store.py      # ChromaDB 向量存储服务
│   │   ├── rag_service.py       # RAG 检索与上下文组装
│   │   ├── GetSortedDocs.py     # 多查询检索 + 去重 + RRF 排序
│   │   └── generate_queries.py  # LLM 查询扩展
│   ├── tool/                    # 工具函数 (LangChain @tool)
│   │   ├── rag_tool.py          # RAG 检索工具
│   │   ├── web_search_tool.py   # 联网搜索工具 (智谱 API)
│   │   └── question_tools.py    # 出题工具
│   ├── memory/                  # 对话记忆
│   │   ├── pg_memory.py         # PostgreSQL 检查点/存储 (LangGraph)
│   │   └── redis_memory.py      # Redis 客户端
│   ├── smart_question/          # 智能出题逻辑
│   │   └── ai_response.py       # 四种题型的生成逻辑
│   ├── prompts/                 # 提示词模板
│   │   ├── system_prompt.txt
│   │   ├── question_agent_prompt.txt
│   │   ├── context_agent_prompt.txt
│   │   └── smart_question/      # 各题型专用提示词
│   └── data/                    # 示例知识库数据
│
├── router/                      # API 路由
│   ├── agent_router.py          # /agent/* 聊天、出题、会话管理
│   ├── user_router.py           # /user/login 用户登录
│   └── vector_store_router.py   # /vector/* 文档管理
│
├── crud/                        # 业务逻辑层
│   ├── ai_response_service.py   # 聊天/出题 CRUD
│   ├── user_service.py          # 用户服务
│   └── vector_store_service.py  # 文档上传/删除/列表
│
├── model/                       # SQLAlchemy ORM 模型
│   ├── base.py                  # DeclarativeBase
│   ├── Users.py                 # 用户表
│   ├── ChatHistory.py           # 会话 + 聊天记录表
│   ├── FileInfo.py              # 文件信息表
│   ├── Question.py              # 题目记录表
│   └── question_schemas.py      # 题目 Pydantic 模型
│
├── schemas/                     # Pydantic 请求/响应模型
│   ├── result.py                # 统一响应包装
│   ├── agent_schemas.py         # 聊天相关模型
│   ├── user_schemas.py          # 用户相关模型
│   ├── quesion_schemas.py       # 题目相关模型
│   └── file_schemas.py          # 文件相关模型
│
├── middleware/
│   └── jwtMiddleware.py         # JWT 认证中间件
│
├── utils/                       # 工具函数
│   ├── dbUtils.py               # 异步 SQLAlchemy 引擎
│   ├── configUtils.py           # YAML 配置加载
│   ├── envUtils.py              # 环境变量加载
│   ├── jwtUtils.py              # JWT 编解码
│   ├── file_handler.py          # PDF/TXT/DOCX 文件解析
│   └── ...
│
├── properties/                  # 配置文件
│   ├── database.yml             # PostgreSQL + Redis 连接配置
│   └── chroma.yml               # ChromaDB 向量库配置
│
├── frontend/                    # Vue 3 + TypeScript 前端
│   ├── src/
│   │   ├── main.ts              # 应用入口
│   │   ├── App.vue
│   │   ├── router/index.ts      # 路由配置 (/login → /chat)
│   │   ├── views/
│   │   │   ├── LoginView.vue    # 登录页
│   │   │   └── ChatView.vue     # 聊天主界面
│   │   └── components/
│   │       └── KnowledgeBase.vue # 知识库管理组件
│   └── package.json
│
└── chroma_db/                   # ChromaDB 持久化数据 (生成)
```

---

## 快速开始

### 前置依赖

- Python 3.10+
- PostgreSQL
- Redis
- Node.js 18+ (前端)

### 1. 配置环境变量

复制 `.env.example` 为 `.env` 并填写：

```bash
# 通义千问 (用于 Embedding)
QWEN_API_KEY=your_qwen_api_key
QWEN_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL_NAME=qwen3.5-plus-2026-04-20

# 智谱 AI (用于联网搜索)
ZHI_PU_API_KEY=your_zhipu_api_key

# 主模型 (DeepSeek / 其他 OpenAI 兼容接口)
MODEL_NAME=deepseek-v4-flash
MODEL_API=your_deepseek_api_key
MODEL_URL=https://api.deepseek.com

# JWT 密钥
JWT_SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
```

### 2. 配置数据库

编辑 `properties/database.yml`：

```yaml
pg_host: localhost
pg_port: 5432
pg_db: agentdb
pg_user: postgres
pg_password: 123321

redis_host: localhost
redis_port: 6379
redis_db: 0
```

### 3. 启动后端

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 进入应用。

---

## API 参考

### 聊天相关 `/agent`

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/agent/question/invoke` | 非流式问答 |
| POST | `/agent/question/stream` | SSE 流式问答 |
| GET | `/agent/question/get_new_session_id` | 获取新会话 ID |
| GET | `/agent/question/get_chat_sessions` | 获取会话列表 |
| GET | `/agent/question/get_chat_history/{session_id}` | 获取会话历史 |
| POST | `/agent/question/delete_chat_history` | 软删除聊天记录 |
| DELETE | `/agent/question/delete_chat_session/{session_id}` | 删除会话 |
| POST | `/agent/question/generate_question` | 智能出题 |
| GET | `/agent/question/get_user_generated_questions` | 获取已出题目 |

### 用户相关 `/user`

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/user/login` | 手机号+密码登录，返回 JWT |

### 知识库相关 `/vector`

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/vector/add_documents` | 上传文件 (PDF/TXT/DOCX) |
| GET | `/vector/get_all_files` | 获取已上传文件列表 |
| DELETE | `/vector/delete_file/{file_id}` | 删除文件 |

---

## 核心配置

### 向量数据库 (`properties/chroma.yml`)

```yaml
embedding_model: text-embedding-v1    # Embedding 模型
collection_name: agent                 # ChromaDB 集合名
k: 3                                   # 检索 Top-K
chunk_size: 800                        # 文本分块大小
chunk_overlap: 100                     # 分块重叠
```

### RAG 参数

- 查询扩展数：3 个变体
- 重排序：RRF（Reciprocal Rank Fusion）
- 检索来源：ChromaDB + 联网搜索

### 支持的文档格式

`txt`, `pdf`, `docx`

---

## 技术栈

| 层面 | 技术 |
|------|------|
| **后端框架** | FastAPI + Uvicorn |
| **AI Agent** | LangChain + LangGraph |
| **向量数据库** | ChromaDB |
| **关系数据库** | PostgreSQL (asyncpg) |
| **缓存** | Redis |
| **LLM 提供商** | DeepSeek / OpenAI 兼容接口 |
| **Embedding** | 通义千问 (DashScope) |
| **联网搜索** | 智谱 AI |
| **前端** | Vue 3 + TypeScript + Vite |
| **认证** | JWT (python-jose) |
| **流式** | SSE (Server-Sent Events) |

---

## 贡献

欢迎提交 Issue 和 Pull Request。在添加新功能前，请先阅读 `CLAUDE.md` 了解项目的多智能体架构约定。

---

## 许可

MIT License
