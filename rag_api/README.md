# RAG (Retrieval Augmented Generation) System

A production-ready implementation of a RAG system built with [LangChain](https://www.langchain.com/), supporting multiple vector stores and document sources. This system enhances Large Language Model responses by grounding them in your specific document collection.

## Features

- **Multiple Vector Store Support**:
  - Local: [ChromaDB](https://www.trychroma.com/) - Embedded vector database
  - Cloud: [Pinecone](https://www.pinecone.io/) - Managed vector database service
  - Self-hosted/Cloud: [Weaviate](https://weaviate.io/) - Vector search engine
  - Self-hosted/Cloud: [Qdrant](https://qdrant.tech/) - Vector database with extended filtering

- **Flexible Document Sources**:
  - Local file system
  - [Amazon S3](https://aws.amazon.com/s3/) cloud storage

- **Document Processing**:
  - Automatic chunking with configurable size and overlap
  - Support for multiple file formats (PDF, TXT, MD, CSV)
  - Intelligent text splitting for optimal context retention

- **Environment-based Configuration**:
  - All settings managed through environment variables
  - No runtime configuration changes required
  - Secure credentials management

## Architecture

The system consists of several key components:

1. **Document Manager**: Handles document loading and preprocessing from various sources
2. **Vector Store Manager**: Manages different vector database backends
3. **RAG System**: Coordinates document processing, embedding, and query answering
4. **API Layer**: Provides RESTful access to the RAG system

## Prerequisites

- Python 3.8+
- OpenAI API key
- Additional credentials based on chosen vector store and document sources

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Unix/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

## Configuration

The system is configured entirely through environment variables. Here are the key configuration options:

### Vector Store Configuration

```env
# Choose your vector store backend
VECTOR_STORE_TYPE=chroma  # Options: chroma, pinecone, weaviate, qdrant

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=rag-index

# Weaviate Configuration
WEAVIATE_URL=your_weaviate_url
WEAVIATE_API_KEY=your_weaviate_api_key
WEAVIATE_INDEX_NAME=RAG

# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=documents
```

### Document Sources Configuration

```env
# Configure document sources
DOCUMENT_SOURCES=["local"]  # Options: ["local"] or ["local", "s3"]

# Local Documents
LOCAL_DOCUMENT_PATH=./data

# S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
S3_BUCKET=your_bucket_name
S3_PREFIX=
```

### RAG System Configuration

```env
# OpenAI
OPENAI_API_KEY=your_api_key_here

# Processing Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_K=4
TEMPERATURE=0
```

## Usage

1. Start the server:
```bash
python run.py
```

2. The API will be available at `http://localhost:8000`

3. Make queries using the `/query` endpoint:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "your question here"}'
```

## Adding Documents

Documents are loaded automatically when the server starts, based on your .env configuration. There is no dynamic upload endpoint; add files statically and restart the server.

### Local Files
1. Place your documents (PDF, TXT, etc.) in the configured directory (default: `./data`).
2. Ensure `DOCUMENT_SOURCES` includes "local" in .env.
3. Restart the server with `python run.py` to load and process the new documents.

### Amazon S3
1. Upload files to your S3 bucket using AWS CLI (e.g., `aws s3 cp file.pdf s3://your-bucket/path/`).
2. Ensure `DOCUMENT_SOURCES` includes "s3" and configure AWS credentials/S3 details in .env.
3. Restart the server with `python run.py` to load from S3.

Note: For dynamic uploads, consider extending the API with a new endpoint.

## API Reference

### POST /query

Makes a query to the RAG system.

**Request Body**:
```json
{
    "question": "string"
}
```

**Response**:
```json
{
    "response": "string"
}
```

## Vector Store Selection Guide

### ChromaDB
- Best for: Development, testing, and small to medium-sized document collections
- Advantages: No external dependencies, embedded database
- Limitations: Limited by local storage and RAM

### Pinecone
- Best for: Production deployments, large-scale applications
- Advantages: Fully managed, highly available, scalable
- Limitations: Paid service, higher latency than local options

### Weaviate
- Best for: Complex semantic search requirements
- Advantages: Rich query capabilities, self-hosted option
- Limitations: More complex setup, requires more resources

### Qdrant
- Best for: Advanced filtering and custom distance functions
- Advantages: High performance, flexible deployment options
- Limitations: Newer in the market, smaller community

## Document Processing

The system processes documents in the following steps:

1. **Loading**: Documents are loaded from configured sources
2. **Chunking**: Documents are split into smaller pieces using RecursiveCharacterTextSplitter
3. **Embedding**: Text chunks are converted to vector embeddings
4. **Storage**: Embeddings are stored in the configured vector store

## Performance Considerations

- Vector store choice significantly impacts query performance
- Local vector stores provide lower latency but limited scalability
- Cloud-based solutions offer better scalability but higher latency
- Chunk size affects both storage requirements and retrieval quality

## Security Considerations

- Store all credentials in environment variables
- Use appropriate access controls for vector stores
- Implement rate limiting for production deployments
- Monitor API usage and implement appropriate authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)

## Acknowledgments

- [LangChain](https://www.langchain.com/) for the foundation framework
- [OpenAI](https://openai.com/) for embedding and LLM capabilities
- Vector store providers for their respective services 