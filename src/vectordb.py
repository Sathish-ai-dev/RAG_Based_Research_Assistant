import os
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorDB:
    """
    A simple vector database wrapper using ChromaDB with HuggingFace embeddings.
    """

    def __init__(self, collection_name: str = None, embedding_model: str = None):
        """
        Initialize the vector database.

        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: HuggingFace model name for embeddings
        """
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION_NAME", "rag_documents"
        )
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Load embedding model
        print(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "RAG document collection"},
        )

        print(f"Vector database initialized with collection: {self.collection_name}")

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Text chunking using LangChain's RecursiveCharacterTextSplitter.
        Automatically handles sentence boundaries and preserves context better.

        Args:
            text: Input text to chunk
            chunk_size: Approximate number of characters per chunk

        Returns:
            List of text chunks
        """
        # Use LangChain's RecursiveCharacterTextSplitter
        # This automatically handles sentence boundaries and preserves context better
        if not text.strip():
            return []
        
        # Initialize the text splitter with chunk_size and overlap for better context preservation
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_size // 10,  # 10% overlap to preserve context between chunks
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Try to split on paragraphs, then sentences, then words
        )
        
        # Split the text into chunks
        chunks = text_splitter.split_text(text)
        
        return chunks

    def add_documents(self, documents: List) -> int:
        """
        Add documents to the vector database.

        Args:
            documents: List of documents

        Returns:
            Number of chunks stored in the vector database
        """
        # TODO: Implement document ingestion logic
        # HINT: Loop through each document in the documents list
        # HINT: Extract 'content' and 'metadata' from each document dict
        # HINT: Use self.chunk_text() to split each document into chunks
        # HINT: Create unique IDs for each chunk (e.g., "doc_0_chunk_0")
        # HINT: Use self.embedding_model.encode() to create embeddings for all chunks
        # HINT: Store the embeddings, documents, metadata, and IDs in your vector database
        # HINT: Print progress messages to inform the user

        print(f"Processing {len(documents)} documents...")
        
        # Collect all chunks, IDs, embeddings, and metadata
        all_chunks = []
        all_ids = []
        all_metadatas = []
        
        # Process each document
        for doc_idx, document in enumerate(documents):
            # Extract content and metadata from document dict
            content = document.get("content", "")
            doc_metadata = document.get("metadata", {})
            
            if not content:
                print(f"Warning: Document {doc_idx} has no content, skipping...")
                continue
            
            # Chunk the document content
            chunks = self.chunk_text(content, chunk_size=500)
            
            if not chunks:
                print(f"Warning: Document {doc_idx} produced no chunks, skipping...")
                continue
            
            print(f"  Document {doc_idx + 1}: Created {len(chunks)} chunks")
            
            # Create unique IDs and metadata for each chunk
            for chunk_idx, chunk in enumerate(chunks):
                chunk_id = f"doc_{doc_idx}_chunk_{chunk_idx}"
                all_ids.append(chunk_id)
                all_chunks.append(chunk)
                
                # Preserve original document metadata and add chunk info
                chunk_metadata = {
                    **doc_metadata,
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks),
                    "document_index": doc_idx
                }
                all_metadatas.append(chunk_metadata)
        
        if not all_chunks:
            print("No chunks to add to vector database")
            return 0
        
        # Create embeddings for all chunks at once (more efficient)
        print(f"Creating embeddings for {len(all_chunks)} chunks...")
        embeddings = self.embedding_model.encode(all_chunks).tolist()
        
        # Add all chunks to ChromaDB collection
        print(f"Storing {len(all_chunks)} chunks in vector database...")
        self.collection.add(
            ids=all_ids,
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas
        )
        
        print("Documents added to vector database")
        return len(all_chunks)

    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents in the vector database.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Dictionary containing search results with keys: 'documents', 'metadatas', 'distances', 'ids'
        """
        # Use self.embedding_model.encode([query]) to create query embedding
        # The encode method expects a list, so wrap the query in a list
        query_embedding = self.embedding_model.encode([query])
        
        # Convert the embedding to appropriate format for ChromaDB (list of lists)
        # ChromaDB expects query_embeddings as a list of lists
        query_embeddings = query_embedding.tolist()
        
        # Use your vector database's search/query method with the query embedding and n_results
        # ChromaDB's query method returns results in a specific format
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results
            )
        except Exception as e:
            print(f"Error during search: {e}")
            # Handle the case where results might be empty or error occurs
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": [],
            }
        
        # Handle the case where results might be empty
        if not results or not results.get("ids") or len(results["ids"]) == 0:
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": [],
            }
        
        # Return a dictionary with keys: 'documents', 'metadatas', 'distances', 'ids'
        # ChromaDB returns results as lists of lists, so we need to extract the first element
        # since we're querying with a single query embedding
        return {
            "documents": results.get("documents", [[]])[0] if results.get("documents") else [],
            "metadatas": results.get("metadatas", [[]])[0] if results.get("metadatas") else [],
            "distances": results.get("distances", [[]])[0] if results.get("distances") else [],
            "ids": results.get("ids", [[]])[0] if results.get("ids") else [],
        }
