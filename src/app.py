import os
from typing import List, Dict, Any, Union
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.vectordb import VectorDB
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()


def load_documents() -> List[Dict[str, Any]]:
    """
    Load documents for demonstration.

    Returns:
        List of document dictionaries with 'content' and 'metadata' keys
    """
    results = []
    # TODO: Implement document loading
    # HINT: Read the documents from the data directory
    # HINT: Return a list of documents
    # HINT: Your implementation depends on the type of documents you are using (.txt, .pdf, etc.)

    # Get the path to the data directory (one level up from src/)
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent / "data"
    
    # Check if data directory exists
    if not data_dir.exists():
        print(f"Warning: Data directory not found at {data_dir}")
        return results
    
    # Read all .txt files from the data directory
    txt_files = list(data_dir.glob("*.txt"))
    
    for file_path in txt_files:
        try:
            # Read file content with UTF-8 encoding
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create document dictionary with content and metadata
            document = {
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    "file_path": str(file_path)
                }
            }
            results.append(document)
            print(f"Loaded: {file_path.name}")
        except Exception as e:
            print(f"Error loading {file_path.name}: {e}")
    
    return results


class RAGAssistant:
    """
    A simple RAG-based AI assistant using ChromaDB and multiple LLM providers.
    Supports OpenAI, Groq, and Google Gemini APIs.
    """

    def __init__(self):
        """Initialize the RAG assistant."""
        # Initialize LLM - check for available API keys in order of preference
        self.llm = self._initialize_llm()
        if not self.llm:
            raise ValueError(
                "No valid API key found. Please set one of: "
                "OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

        # Initialize vector database
        self.vector_db = VectorDB()

        # Create RAG prompt template
        # TODO: Implement your RAG prompt template
        # HINT: Use ChatPromptTemplate.from_template() with a template string
        # HINT: Your template should include placeholders for {context} and {question}
        # HINT: Design your prompt to effectively use retrieved context to answer questions
        self.prompt_template = ChatPromptTemplate.from_template(
            "You are a helpful AI assistant. Use the following context to answer the question. "
            "If the context doesn't contain enough information to answer the question, "
            "say that you don't have enough information in the provided context.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        # Create the chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()

        print("RAG Assistant initialized successfully")

    def _initialize_llm(self):
        """
        Initialize the LLM by checking for available API keys.
        Tries OpenAI, Groq, and Google Gemini in that order.
        """
        # Check for OpenAI API key
        if os.getenv("OPENAI_API_KEY"):
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            print(f"Using OpenAI model: {model_name}")
            return ChatOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GROQ_API_KEY"):
            model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            print(f"Using Groq model: {model_name}")
            return ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"), model=model_name, temperature=0.0
            )

        elif os.getenv("GOOGLE_API_KEY"):
            model_name = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
            print(f"Using Google Gemini model: {model_name}")
            return ChatGoogleGenerativeAI(
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                model=model_name,
                temperature=0.0,
            )

        else:
            raise ValueError(
                "No valid API key found. Please set one of: OPENAI_API_KEY, GROQ_API_KEY, or GOOGLE_API_KEY in your .env file"
            )

    def add_documents(self, documents: List) -> int:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of documents
        """
        return self.vector_db.add_documents(documents)

    def invoke(self, input: str, n_results: int = 3, include_context: bool = False) -> Union[str, Dict[str, Any]]:
        """
        Query the RAG assistant.

        Args:
            input: User's input
            n_results: Number of relevant chunks to retrieve

        Returns:
            Dictionary containing the answer and retrieved context
        """
        # Use self.vector_db.search() to retrieve relevant context chunks
        search_results = self.vector_db.search(input, n_results=n_results)

        # Extract documents from search results
        retrieved_documents = search_results.get("documents", [])
        retrieved_metadatas = search_results.get("metadatas", [])
        retrieved_distances = search_results.get("distances", [])

        # Handle nested list structure (ChromaDB may return documents as list of lists)
        if retrieved_documents and isinstance(retrieved_documents[0], list):
            retrieved_documents = [doc for sublist in retrieved_documents for doc in sublist]
        if retrieved_metadatas and isinstance(retrieved_metadatas[0], list):
            retrieved_metadatas = [meta for sublist in retrieved_metadatas for meta in sublist]
        if retrieved_distances and isinstance(retrieved_distances[0], list):
            retrieved_distances = [dist for sublist in retrieved_distances for dist in sublist]

        # Combine the retrieved document chunks into a single context string
        if retrieved_documents:
            context = "\n\n".join(retrieved_documents)
        else:
            context = "No relevant context found in the knowledge base."
        
        # Use self.chain.invoke() with context and question to generate the response
        # The chain expects a dictionary with keys matching the prompt template placeholders
        llm_answer = self.chain.invoke({
            "context": context,
            "question": input
        })
        
        if include_context:
            sources = []
            for idx, document in enumerate(retrieved_documents):
                snippet = (document or "").strip()
                metadata = retrieved_metadatas[idx] if idx < len(retrieved_metadatas) else {}
                distance = retrieved_distances[idx] if idx < len(retrieved_distances) else None
                sources.append(
                    {
                        "source": metadata.get("source", f"Document {metadata.get('document_index', idx)}"),
                        "file_path": metadata.get("file_path"),
                        "chunk_index": metadata.get("chunk_index"),
                        "distance": float(distance) if distance is not None else None,
                        "excerpt": snippet[:500],
                    }
                )

            return {"answer": llm_answer, "context": context, "sources": sources}

        return llm_answer

    def query(
        self, question: str, n_results: int = 3, include_context: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Alias for invoke method for backward compatibility.
        
        Args:
            question: User's question
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            Either a string answer or a dictionary with answer/context metadata
        """
        return self.invoke(question, n_results, include_context)


def main():
    """Main function to demonstrate the RAG assistant."""
    try:
        # Initialize the RAG assistant
        print("Initializing RAG Assistant...")
        assistant = RAGAssistant()

        # Load sample documents
        print("\nLoading documents...")
        sample_docs = load_documents()
        print(f"Loaded {len(sample_docs)} sample documents")

        assistant.add_documents(sample_docs)

        done = False

        while not done:
            question = input("Enter a question or 'quit' to exit: ")
            if question.lower() == "quit":
                done = True
            else:
                result = assistant.query(question)
                print(result)

    except Exception as e:
        print(f"Error running RAG assistant: {e}")
        print("Make sure you have set up your .env file with at least one API key:")
        print("- OPENAI_API_KEY (OpenAI GPT models)")
        print("- GROQ_API_KEY (Groq Llama models)")
        print("- GOOGLE_API_KEY (Google Gemini models)")


if __name__ == "__main__":
    main()
