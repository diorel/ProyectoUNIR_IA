from typing import List, Optional, Dict
import os
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_community.vectorstores import (
    Pinecone,
    Weaviate,
    Qdrant
)
from langchain.embeddings.base import Embeddings
import pinecone
import weaviate
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from pinecone import Pinecone as PineconeClient
from weaviate import Client as WeaviateClient
from weaviate.auth import AuthApiKey
from weaviate.connect import ConnectionParams

class VectorStoreType:
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"

class VectorStoreManager:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        self.vector_store = None
        self.store_type = None

    def init_chroma(self, persist_directory: str = "./data/chroma_db"):
        """Initialize ChromaDB locally"""
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        self.store_type = VectorStoreType.CHROMA
        return self.vector_store

    def init_pinecone(self, index_name: str):
        """Initialize Pinecone"""
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            raise ValueError("Pinecone API key must be set in .env")
        
        pc = pinecone.Pinecone(api_key=api_key)
        index = pc.Index(index_name)
        # Create index if it doesn't exist - but for simplicity, assume it exists or handle creation
        self.vector_store = Pinecone(
            index=index,
            embedding=self.embeddings,
            text_key="text"
        )
        self.store_type = VectorStoreType.PINECONE
        return self.vector_store

    def init_weaviate(self, url: str, index_name: str):
        """Initialize Weaviate"""
        api_key = os.getenv('WEAVIATE_API_KEY')
        if api_key:
            auth_config = AuthApiKey(api_key=api_key)
        else:
            auth_config = None
        
        client = WeaviateClient(
            connection_params=ConnectionParams.from_url(url, grpc_port=50051),
            auth_client_secret=auth_config
        )
        self.vector_store = Weaviate(
            client=client,
            index_name=index_name,
            text_key="text",
            embedding=self.embeddings
        )
        self.store_type = VectorStoreType.WEAVIATE
        return self.vector_store

    def init_qdrant(self, url: Optional[str] = None, collection_name: str = "documents"):
        """Initialize Qdrant (local or remote)"""
        if url:
            # Remote Qdrant
            api_key = os.getenv('QDRANT_API_KEY')
            client = QdrantClient(url=url, api_key=api_key)
        else:
            # Local Qdrant
            client = QdrantClient(path="./data/qdrant_db")
        
        # Create collection if it doesn't exist
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        if collection_name not in collection_names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
        
        self.vector_store = Qdrant(
            client=client,
            collection_name=collection_name,
            embeddings=self.embeddings
        )
        self.store_type = VectorStoreType.QDRANT
        return self.vector_store

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call init_* first.")
        
        if self.store_type == VectorStoreType.CHROMA:
            self.vector_store.add_documents(documents)
        elif self.store_type == VectorStoreType.PINECONE:
            self.vector_store.add_documents(documents)
        elif self.store_type == VectorStoreType.WEAVIATE:
            self.vector_store.add_documents(documents)
        elif self.store_type == VectorStoreType.QDRANT:
            self.vector_store.add_documents(documents)

    def get_retriever(self, **kwargs):
        """Get retriever with optional configuration"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call init_* first.")
        return self.vector_store.as_retriever(**kwargs) 