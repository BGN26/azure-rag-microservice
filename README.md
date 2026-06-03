# 🚀 Enterprise Asynchronous RAG Microservice: Event-Driven Architecture & BI Analytics Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-purple)
![Celery](https://img.shields.io/badge/Celery-Distributed-green)
![Redis](https://img.shields.io/badge/Redis-In--Memory-red)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458)

An enterprise-grade, production-ready microservice built to handle intensive Retrieval-Augmented Generation (RAG) workloads. By pivoting from a traditional synchronous API pattern to a decoupled, **event-driven architecture**, this system eliminates main-thread I/O blocking during heavy document processing while exposing granular operational and financial KPIs optimized for Business Intelligence (BI) integrations.

---

## 🏛️ Core Architectural Pillars

### 1. Asynchronous Event-Driven Ingestion Pipeline (FastAPI + Redis + Celery)
* **Non-Blocking I/O Gateway:** The `/upload` endpoint acts purely as a validation and ingestion gate. It validates the HTTP request protocol, safely streams the binary payload to a protected temporary storage volume using efficient buffered chunking (`shutil`), fires an execution task event to the message broker, and immediately yields an **HTTP 202 Accepted** status code back to the client along with a unique `task_id`.
* **Distributed Task Execution:** A background cluster of **Celery workers** backed by an in-memory **Redis** broker consumes the tasks independently. This insulates the API from web timeouts and isolates faults during resource-heavy computations.
* **Automated Ephemeral Garbage Collection:** Post-processing hooks trigger a secure cleanup sequence (`os.remove()`) that wipes temporary files from disk immediately after vector index synchronization, enforcing a strict data-minimization policy and protecting host storage capacity.
* **Exponential Backoff & Fault Tolerance:** Tasks are configured with deterministic retry limits (`max_retries=3`) and custom countdown backoffs to resiliently withstand transient third-party API or rate-limiting thresholds.

### 2. Cognitive RAG Orchestration Engine (LangChain + Vector DB)
* **Semantic Document Extraction:** Implements specialized document loaders to ingest complex PDF binaries, maintaining high semantic fidelity and layout positioning metadata.
* **Optimized Token Chunking:** Employs advanced text-splitting strategies to slice raw corpora into highly cohesive context blocks, striking the perfect balance between token utility and contextual density.
* **High-Dimensional Vector Ingestion:** Generates text embeddings using cutting-edge models and indexes them directly into a persistent **ChromaDB** deployment for sub-millisecond similarity searches during live retrieval loops.

### 3. Vectorized Financial Analytics & BI Engine (Pandas Engine)
* **Algorithmic Infrastructure Costing:** Integrates an analytical ledger module that intercepts internal operational records to track total OpenAI/Azure token consumption, applying vectorized mathematical functions to calculate exact, real-time infrastructure expenditures in **Euros (€)**.
* **Operational Bottleneck Profiling:** Utilizes advanced **Pandas** groupings to isolate average processing times stratified by internal corporate departments and document schemas, computing aggregate success-to-failure distributions.
* **BI Data Ingestion Gateway:** Exposes an optimized, low-latency `/analytics/kpi` endpoint. The structured JSON output serves as a native, plug-and-play semantic layer for business intelligence platforms like **PowerBI**, **Tableau**, or **Grafana** dashboards.

---

## 📊 System Topology & Sequence Flow

    
    [ Client Application / BI Platform ]
                │
                ├── (1) POST /upload (PDF Binary) ──────► [ FastAPI Gateway ] ────► (2) HTTP 202 Accepted (Returns task_id)
                │                                                │
                │                                    (Buffer Stream & Enqueue)
                │                                                ▼
                │                                        [ Redis Broker ]
                │                                                │
                │                                        (Worker Pick-up)
                │                                                ▼
                │                                        [ Celery Worker ] ────► [ LangChain Pipeline ] ──► [ LLM Embeddings ]
                │                                                │                                                  │
                │                                         (Disk Cleanup)                                            ▼
                │                                                └───────────────────────────────────────────► [ ChromaDB ]
                │
                ├── (3) POST /query (Natural Language) ──────────────────────────────────────────────────────► [ RAG Query Engine ]
                │
                └── (4) GET /analytics/kpi ─────────────► [ Pandas Data Engine ] ──► Evaluates Infrastructure ROI in Euros (€)
   
# 🚦 API Gateway Reference Specification


| Método | Endpoint | Estado HTTP | Contexto / Alcance | Esquema de Carga (Payload) / Respuesta |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/upload` | `202 Accepted` | Async PDF Ingestion | `{"message": "...", "task_id": "uuid", "status": "Processing"}` |
| `POST` | `/api/v1/query` | `200 OK` | RAG Live Query | `{"question": "String", "answer": "Synthesized Context Output"}` |
| `GET` | `/api/v1/analytics/kpi` | `200 OK` | Business Intelligence | `{"overview": {"estimated_ai_cost_eur": 4.2048}, "performance": {...}}` |

# 🧪 Enterprise CI/CD & Test Automation Suite
The codebase enforces absolute regressions control via a dedicated testing infrastructure executed automatically through GitHub Actions CI/CD pipelines on every push and Pull Request.

Deterministic Mocking Architecture: Network external dependencies, Redis connections, and Celery broker event-loops are completely isolated using advanced unittest.mock.patch configurations and MagicMock constraints. This ensures that the test suite runs fully decoupled from active servers, executing under 2 seconds while maintaining 100% environment independence.

Strict Type & Schema Enforcement: Outbound analytical records are validated at the property level, ensuring mathematical precision and datatype stability for down-stream BI dashboards.

# Execute Test Harness Locally:

    pytest -v

