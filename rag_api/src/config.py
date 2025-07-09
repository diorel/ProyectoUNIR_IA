from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str

    # Vector Store Configuration
    vector_store_type: str = "chroma"  # chroma, pinecone, weaviate, qdrant
    
    # ChromaDB Configuration (Local)
    chroma_persist_directory: str = "./data/chroma_db"
    
    # Pinecone Configuration
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "rag-index"
    
    # Weaviate Configuration
    weaviate_url: Optional[str] = None
    weaviate_api_key: Optional[str] = None
    weaviate_index_name: str = "RAG"
    
    # Qdrant Configuration
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "documents"
    
    # Document Sources Configuration
    document_sources: list = ["local"]  # local, s3
    
    # Local Documents Configuration
    local_document_path: str = "./data"
    
    # S3 Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket: Optional[str] = None
    s3_prefix: str = ""

    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_k: int = 4
    temperature: float = 0

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Validate vector store configuration
def validate_vector_store_config(settings: Settings):
    if settings.vector_store_type == "pinecone":
        if not settings.pinecone_api_key or not settings.pinecone_environment:
            raise ValueError("Pinecone API key and environment must be set for Pinecone vector store")
    elif settings.vector_store_type == "weaviate":
        if not settings.weaviate_url:
            raise ValueError("Weaviate URL must be set for Weaviate vector store")
    elif settings.vector_store_type == "qdrant":
        if settings.qdrant_url and not settings.qdrant_api_key:
            raise ValueError("Qdrant API key must be set for remote Qdrant vector store")

# Validate document sources configuration
def validate_document_sources_config(settings: Settings):
    if "s3" in settings.document_sources:
        if not all([settings.aws_access_key_id, settings.aws_secret_access_key, settings.s3_bucket]):
            raise ValueError("AWS credentials and S3 bucket must be set for S3 document source") 