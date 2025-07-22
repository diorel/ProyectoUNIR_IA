# UNIR AI Project

This repository contains a collection of AI-powered applications developed as part of the UNIR Master's program in Artificial Intelligence. The project demonstrates the implementation of various AI technologies and architectures.

## Project Structure

The repository is organized into the following main components:

### RAG API (`/rag_api`)

A Retrieval Augmented Generation (RAG) system that enhances Large Language Model responses by grounding them in specific document collections. This implementation supports:

- Multiple vector stores (ChromaDB, Pinecone, Weaviate, Qdrant)
- Document loading from local and S3 sources
- Environment-based configuration
- RESTful API interface

[Learn more about the RAG API](./rag_api/README.md)

### Chat Application (`/chat_app`)

A web-based chat interface that demonstrates:

- Real-time communication
- Modern UI/UX design
- Integration with AI services
- Responsive layout

[Learn more about the Chat Application](./chat_app/README.md)

## Getting Started

Each component has its own setup instructions and requirements. Please refer to the individual README files in each directory for specific setup and usage instructions.

## Development

The project uses modern development practices and tools:

- Git for version control
- Environment-based configuration
- Modular architecture
- Comprehensive documentation

## License

This project is licensed under the MIT License - see the individual component directories for specific license information.

## Authors

- Raul Diorelyon Cortes
- Carlos Eduardo Ramirez
- Juan Pablo Corona

## Acknowledgments

- UNIR Master's Program in Artificial Intelligence
- OpenAI for API services
- Various open-source projects and their contributors
