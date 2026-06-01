# 🧠 Azure RAG Microservice

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern-009688)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-purple)

A production-ready REST API microservice for AI-powered Document Analysis, utilizing **Retrieval-Augmented Generation (RAG)**. 

Built with modern Python async capabilities, this microservice allows users to ingest PDF documents, vectorizes them, and provides a semantic search and Q&A interface using LLMs.

## 🚀 Tech Stack

- **Backend Framework:** FastAPI (Asynchronous, Pydantic for data validation)
- **AI / LLM Orchestration:** LangChain (using modern LCEL syntax)
- **Vector Database:** ChromaDB (Local persistence)
- **Testing:** Pytest with Unit Mocking
- **CI/CD:** GitHub Actions (Automated testing and Docker builds)
- **Infrastructure:** Docker containerized, ready for Azure App Service / Azure Container Apps deployment.

## 🏗️ Architecture & Features

1. **`/api/v1/upload` (Ingestion):** Accepts PDF files, processes them using `RecursiveCharacterTextSplitter`, generates OpenAI embeddings, and stores the vectors in ChromaDB.
2. **`/api/v1/query` (Retrieval & Generation):** Accepts user queries, retrieves the top-K relevant chunks from the vector store, and uses `gpt-5.4-mini` to generate highly contextual answers while preventing hallucinations.
3. **Health Checks & Monitoring:** Built-in endpoints for Azure load balancers and CI/CD pipelines.

## 💻 Local Execution (Docker)

To run this microservice locally without installing Python dependencies, simply use Docker:


# 1. Clone the repository
    git clone https://github.com/BGN26/azure-rag-microservice
    cd azure-rag-microservice

# 2. Add your OpenAI API Key
    echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 3. Build and run the container
    docker build -t azure-rag-api .
    docker run -p 8000:8000 --env-file .env azure-rag-api

# 🛣️ Roadmap & Next Steps (Event-Driven Scaling)
To fully scale this architecture for enterprise use, the next iterations will include:

Implementing an Event-Driven Architecture (RabbitMQ / Kafka) to decouple heavy PDF processing tasks into background workers.

Upgrading from local ChromaDB to a managed vector store (e.g., FAISS or Azure AI Search).

Implementing robust Auth (OAuth2/JWT).