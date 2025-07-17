import os
from typing import List, Union
import boto3
from botocore.exceptions import ClientError
from langchain_community.document_loaders import (
    DirectoryLoader,
    S3FileLoader,
    UnstructuredFileLoader,
    PDFMinerLoader,
    TextLoader
)
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentSource:
    LOCAL = "local"
    S3 = "s3"

class DocumentManager:
    def __init__(self):
        self.s3_client = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def _init_s3_client(self):
        """Initialize S3 client if not already initialized"""
        if not self.s3_client:
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            aws_region = os.getenv('AWS_REGION', 'us-east-1')
            if not aws_access_key_id or not aws_secret_access_key:
                raise ValueError("AWS credentials must be set in .env for S3 access")
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )

    def _get_file_loader(self, file_path: str, source: str = DocumentSource.LOCAL) -> Union[UnstructuredFileLoader, PDFMinerLoader, TextLoader]:
        """Get appropriate loader based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return PDFMinerLoader(file_path)
        elif ext in ['.txt', '.md', '.csv']:
            return TextLoader(file_path)
        else:
            return UnstructuredFileLoader(file_path)

    def load_from_local(self, directory_path: str) -> List[Document]:
        """Load documents from local directory"""
        if not os.path.exists(directory_path):
            raise ValueError(f"Directory not found: {directory_path}")

        loader = DirectoryLoader(
            directory_path,
            glob="**/*.*",  # Load all files recursively
            loader_cls=UnstructuredFileLoader,
            show_progress=True
        )
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def load_from_s3(self, bucket: str, prefix: str = "") -> List[Document]:
        """Load documents from S3 bucket"""
        self._init_s3_client()
        if self.s3_client is None:
            raise ValueError("Failed to initialize S3 client")
        documents = []

        try:
            # List all objects in the bucket with the given prefix
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
                if 'Contents' not in page:
                    continue

                for obj in page['Contents']:
                    key = obj['Key']
                    if key.endswith('/'):  # Skip directories
                        continue
                    
                    # Create a temporary file to download the S3 object
                    temp_path = os.path.join(os.getcwd(), "temp", os.path.basename(key))
                    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
                    
                    try:
                        self.s3_client.download_file(bucket, key, temp_path)
                        loader = self._get_file_loader(temp_path)
                        docs = loader.load()
                        documents.extend(docs)
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

        except ClientError as e:
            raise Exception(f"Error accessing S3: {str(e)}")

        return self.text_splitter.split_documents(documents)

    def load_documents(self, source: str, **kwargs) -> List[Document]:
        """
        Load documents from specified source
        Args:
            source: Either DocumentSource.LOCAL or DocumentSource.S3
            **kwargs: 
                For LOCAL: directory_path
                For S3: bucket and prefix
        """
        if source == DocumentSource.LOCAL:
            directory_path = kwargs.get('directory_path')
            if not directory_path:
                raise ValueError('directory_path is required for LOCAL source')
            return self.load_from_local(directory_path)
        elif source == DocumentSource.S3:
            bucket = kwargs.get('bucket')
            if not bucket:
                raise ValueError('bucket is required for S3 source')
            return self.load_from_s3(
                bucket,
                kwargs.get('prefix', '')
            )
        else:
            raise ValueError(f"Unsupported document source: {source}") 