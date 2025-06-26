from typing import List
import chromadb
from sentence_transformers import SentenceTransformer

class ChromaVectorStore:
    def __init__(self, persist_path: str = "./chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        """Initialize ChromaDB vector store."""
        self.model = SentenceTransformer(embedding_model)
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection("rag_collection")
        self.documents = []

    def add_documents(self, documents: List[str]):
        """Add documents to ChromaDB."""
        if not documents:
            return
        embeddings = self.model.encode(documents)
        self.documents.extend(documents)
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            ids=[f"doc_{len(self.documents)-len(documents)+i}" for i in range(len(documents))]
        )

    def search(self, query: str, k: int = 3) -> List[str]:
        """Search for top-k relevant documents."""
        query_embedding = self.model.encode([query])[0]
        results = self.collection.query(query_embeddings=[query_embedding.tolist()], n_results=k)
        return results["documents"][0] if results["documents"] else []