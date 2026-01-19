"""
Vector Store using ChromaDB
Stores document embeddings and enables similarity search.
"""

import chromadb
from chromadb.config import Settings

try:
    from .document_loader import DocumentChunk
except ImportError:
    from document_loader import DocumentChunk


class VectorStore:
    """ChromaDB-based vector store for design rule documents."""

    def __init__(self, collection_name: str = "design_rules"):
        """
        Initialize the vector store.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        # TODO 1: Initialize ChromaDB client (persistent or in-memory)
        # Hint: chromadb.Client() for in-memory
        # Hint: chromadb.PersistentClient(path="./chroma_db") for persistent
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # TODO 2: Get or create collection
        # Hint: self.client.get_or_create_collection(name=collection_name)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks: list[DocumentChunk]) -> None:
        """
        Add document chunks to the vector store.

        Args:
            chunks: List of DocumentChunk objects to add
        """
        # TODO 3: Prepare data for ChromaDB
        # - documents: list of chunk texts
        # - metadatas: list of metadata dicts
        # - ids: list of unique IDs (use rule_id or generate)
        documents = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [chunk.metadata.get("rule_id") for chunk in chunks]   


        # TODO 4: Add to collection
        # Hint: self.collection.add(documents=..., metadatas=..., ids=...)
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)


    def search(self, query: str, n_results: int = 3, layer_filter: str = None) -> list[dict]:
        """
        Search for similar documents.

        Args:
            query: Natural language query
            n_results: Number of results to return
            layer_filter: Optional filter by layer (e.g., "Metal1")

        Returns:
            List of results with text, metadata, and distance
        """
        # TODO 5: Build where filter if layer_filter is provided
        # Hint: where={"layer": layer_filter} if layer_filter else None

        where = {"layer": layer_filter} if layer_filter else None

        # TODO 6: Query the collection
        # Hint: self.collection.query(query_texts=[query], n_results=n_results, where=where)
        results = self.collection.query(query_texts=[query], n_results=n_results, where=where)

        # TODO 7: Format and return results
        # Return list of dicts with: text, metadata, distance

        return [
            {
                "text": text,
                "metadata": metadata,
                "distance": distance
            }
            for text, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    def clear(self) -> None:
        """Clear all documents from the collection."""
        # TODO 8: Delete the collection and recreate it
        # Hint: self.client.delete_collection(self.collection.name)

        pass  # Remove this when you implement


# Test function
if __name__ == "__main__":
    from pathlib import Path
    # Use absolute import for direct execution
    from document_loader import load_design_rules, DocumentChunk

    # Load documents
    data_path = Path(__file__).parent / "data" / "design_rules.txt"
    chunks = load_design_rules(str(data_path))

    # Create vector store and add documents
    store = VectorStore()
    store.add_documents(chunks)

    # Test search
    print("=== Search Test ===\n")

    query = "What is the minimum metal1 width?"
    results = store.search(query, n_results=3)

    print(f"Query: {query}\n")
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(f"  Rule: {result['metadata'].get('rule_id')}")
        print(f"  Distance: {result['distance']:.4f}")
        print()
