from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
import os
from .document_loader import DocumentManager, DocumentSource
from .vector_store import VectorStoreManager, VectorStoreType
from .config import get_settings, validate_vector_store_config, validate_document_sources_config

class RAGSystem:
    def __init__(self):
        self.settings = get_settings()
        validate_vector_store_config(self.settings)
        validate_document_sources_config(self.settings)
        
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.settings.openai_api_key)
        self.document_manager = DocumentManager()
        self.vector_store_manager = VectorStoreManager(self.embeddings)
        self.qa_chain = None
        
        # Initialize vector store based on configuration
        self._initialize_vector_store()
        
        # Load documents from configured sources
        self._load_configured_documents()
        
        # Setup QA chain
        self._setup_qa_chain()

    def _initialize_vector_store(self):
        """Initialize vector store based on configuration"""
        if self.settings.vector_store_type == VectorStoreType.CHROMA:
            self.vector_store_manager.init_chroma(
                persist_directory=self.settings.chroma_persist_directory
            )
        elif self.settings.vector_store_type == VectorStoreType.PINECONE:
            self.vector_store_manager.init_pinecone(
                index_name=self.settings.pinecone_index_name
            )
        elif self.settings.vector_store_type == VectorStoreType.WEAVIATE:
            self.vector_store_manager.init_weaviate(
                url=self.settings.weaviate_url,
                index_name=self.settings.weaviate_index_name
            )
        elif self.settings.vector_store_type == VectorStoreType.QDRANT:
            self.vector_store_manager.init_qdrant(
                url=self.settings.qdrant_url,
                collection_name=self.settings.qdrant_collection_name
            )
    
    def _load_configured_documents(self):
        """Load documents from configured sources"""
        if "local" in self.settings.document_sources:
            self.load_local_documents(self.settings.local_document_path)
            
        if "s3" in self.settings.document_sources:
            self.load_s3_documents(
                bucket=self.settings.s3_bucket,
                prefix=self.settings.s3_prefix
            )
    
    def _setup_qa_chain(self):
        """Initialize the QA chain with configured parameters"""
        llm = OpenAI(
            temperature=self.settings.temperature,
            openai_api_key=self.settings.openai_api_key
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vector_store_manager.get_retriever(
                search_kwargs={"k": self.settings.retrieval_k}
            )
        )
        
    def load_local_documents(self, data_dir: str):
        """Load documents from local directory"""
        documents = self.document_manager.load_documents(
            source=DocumentSource.LOCAL,
            directory_path=data_dir
        )
        self.vector_store_manager.add_documents(documents)
        
    def load_s3_documents(self, bucket: str, prefix: str = ""):
        """Load documents from S3"""
        documents = self.document_manager.load_documents(
            source=DocumentSource.S3,
            bucket=bucket,
            prefix=prefix
        )
        self.vector_store_manager.add_documents(documents)
        
    def query(self, question: str) -> str:
        """Query the RAG system"""
        if not self.qa_chain:
            raise ValueError("QA Chain not initialized")
        
        response = self.qa_chain.run(question)
        return response 