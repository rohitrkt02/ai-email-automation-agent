# AI Email Automation Agent (Semantic Kernel + MCP + PostgreSQL + FastAPI)

A production-grade, asynchronous AI Email Automation Agent built using **Microsoft Semantic Kernel**, **Google Gemini 2.5 Flash**, **Model Context Protocol (MCP)** principles, and **FastAPI**. The system securely connects to the Gmail API, automatically fetches unread emails, classifies urgency, extracts structured summaries/deadlines, and drafts context-aware professional responses using customized local prompt templates.

---

## 🚀 Key Framework Features
- **Live Gmail Integration:** Authenticated via secure OAuth 2.0 and token rotation mechanisms.
- **Urgency Classification:** Multi-class classification matrices (`Urgent`, `High`, `Medium`, `Low`) returned as raw structural JSON models.
- **Deep Email Summarization:** Contextual mining of text to extract core overviews, actionable items, and deadlocks.
- **Semantic Kernel Native Plugins:** Modular components encapsulated under native kernel registries using functional call-handling hooks.
- **Custom MCP Layer:** Isolated filesystem orchestration for prompt isolation, file tracking, and transaction logging.
- **Industrial DB Persistence:** Upgraded memory backend leveraging relational pooling with **PostgreSQL** instead of SQLite.
- **Interactive OpenAPI Gateway:** REST APIs built with FastAPI equipped with a dedicated interactive **Swagger UI Dashboard**.
- **Microservices Containerization:** Fully multi-container production build orchestrated via Docker and Docker Compose clusters.

---

## 📁 System Core Architecture
```text
Email Agent/
│
├── app/
│   ├── mcp/
│   │   └── mcp_server.py          # Local Filesystem MCP Tool Server
│   ├── plugins/
│   │   ├── gmail_plugin.py        # Native Kernel Wrapper for Gmail API
│   │   └── processing_plugin.py   # Native Kernel Wrapper for AI Workflows
│   ├── services/
│   │   ├── gmail_service.py       # Core OAuth & Gmail Core Client Engine
│   │   ├── classifier_service.py  # Email Priority Matrix Pipeline
│   │   ├── summarizer_service.py  # Structuring and Extractions Core
│   │   ├── reply_service.py       # Non-hallucinatory Text Generator Engine
│   │   └── db_service.py          # PostgreSQL Pooling & SQLAlchemy Models
│   ├── utils/
│   │   └── logger.py              # Rotating File Async Logging Engine
│   ├── kernel.py                  # Core Semantic Kernel Orchestrator Setup
│   └── main_api.py                # FastAPI Engine App Definitions
│
├── prompts/                       # MCP Prompt Template Storage Files
│   ├── priority.txt
│   ├── summary.txt
│   └── reply.txt
│
├── logs/                          # Live Production Telemetry Stream
│   └── agent_pipeline.log
│
├── Dockerfile                     # Continuous App Build Image Schema
├── docker-compose.yml             # App-DB Multi-Container Orchestration Cluster
├── .env                           # Local Security Key Infrastructure Setup
├── requirements.txt               # Complete Python Project Dependencies Scheme
├── run_api.py                     # API Bootstrapping Gateway Launch Script
└── test_postgres.py               # Database Sync Integration Verification File