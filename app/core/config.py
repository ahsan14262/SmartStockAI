from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV","development")
    secret_key: str = os.getenv("APP_SECRET_KEY","dev-only-change-me")
    database_url: str = os.getenv("DATABASE_URL","sqlite:///smart_stock.db")
    groq_api_key: str = os.getenv("GROQ_API_KEY","")
    groq_model: str = os.getenv("GROQ_MODEL","llama-3.1-8b-instant")
    embedding_model: str = os.getenv("EMBEDDING_MODEL","sentence-transformers/all-MiniLM-L6-v2")
    reranker_model: str = os.getenv("RERANKER_MODEL","cross-encoder/ms-marco-MiniLM-L-6-v2")
    vectorstore_root: str = os.getenv("VECTORSTORE_ROOT","storage/vectorstores")
    upload_root: str = os.getenv("UPLOAD_ROOT","storage/uploads")
    default_tenant_id: str = os.getenv("DEFAULT_TENANT_ID","demo-store")
settings = Settings()
