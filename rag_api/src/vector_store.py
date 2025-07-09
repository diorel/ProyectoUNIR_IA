from typing import List, Optional, Dict
import os
from langchain.docstore.document import Document
from langchain.vectorstores import (
    Chroma,
    Pinecone,
    Weaviate,
    Qdrant
)
from langchain.embeddings.base import Embeddings
import pinecone
import weaviate
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

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
        environment = os.getenv('PINECONE_ENVIRONMENT')
        
        if not api_key or not environment:
            raise ValueError("Pinecone API key and environment must be set in .env")
        
        pinecone.init(api_key=api_key, environment=environment)
        
        # Create index if it doesn't exist
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=1536,  # OpenAI embeddings dimension
                metric='cosine'
            )
        
        self.vector_store = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=self.embeddings
        )
        self.store_type = VectorStoreType.PINECONE
        return self.vector_store

    def init_weaviate(self, url: str, index_name: str):
        """Initialize Weaviate"""
        auth_config = None
        if os.getenv('WEAVIATE_API_KEY'):
            auth_config = weaviate.auth.AuthApiKey(api_key=os.getenv('WEAVIATE_API_KEY'))
        
        client = weaviate.Client(
            url=url,
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
            embedding_function=self.embeddings
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