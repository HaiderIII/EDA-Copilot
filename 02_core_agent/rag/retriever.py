"""
Retriever for RAG System
High-level interface for searching design rules.
"""

from pathlib import Path

try:
    from .document_loader import load_design_rules
    from .vector_store import VectorStore
except ImportError:
    from document_loader import load_design_rules
    from vector_store import VectorStore


class DesignRuleRetriever:
    """
    Retriever that combines document loading and vector search.
    This is the main interface for the RAG system.
    """

    def __init__(self, data_path: str = None):
        """
        Initialize the retriever with design rules.

        Args:
            data_path: Path to design_rules.txt (optional, uses default if not provided)
        """
        # TODO 1: Set default data path if not provided
        # Hint: Path(__file__).parent / "data" / "design_rules.txt"
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "design_rules.txt"
        

        # TODO 2: Initialize vector store
        self.store = VectorStore()


        # TODO 3: Load documents and add to vector store
        # Hint: chunks = load_design_rules(data_path)
        # Hint: self.store.add_documents(chunks)
        chunks = load_design_rules(str(data_path))
        self.store.add_documents(chunks)


    def query(self, question: str, n_results: int = 3, layer: str = None) -> str:
        """
        Query the design rules and return formatted context.

        Args:
            question: Natural language question
            n_results: Number of rules to retrieve
            layer: Optional layer filter (e.g., "Metal1", "Poly")

        Returns:
            Formatted string with relevant design rules for LLM context
        """
        # TODO 4: Search the vector store
        # Hint: results = self.store.search(question, n_results, layer_filter=layer)
        results = self.store.search(question, n_results, layer_filter=layer)


        # TODO 5: Format results as context string for LLM
        # Example format:
        # """
        # Relevant Design Rules:
        #
        # [Rule M1.W.1 - Metal1]
        # Value: 18nm
        # <full rule text>
        #
        # [Rule M1.S.1 - Metal1]
        # ...
        # """

        context_lines = ["Relevant Design Rules:\n"]
        for res in results:
            metadata = res["metadata"]
            context_lines.append(f"[Rule {metadata.get('rule_id', 'N/A')} - {metadata.get('layer', 'N/A')}]")
            context_lines.append(f"Value: {metadata.get('value', 'N/A')}")
            context_lines.append(res["text"])
            context_lines.append("")  # Blank line for separation

        return "\n".join(context_lines)

    def get_rule(self, rule_id: str) -> dict | None:
        """
        Get a specific rule by ID.

        Args:
            rule_id: Rule identifier (e.g., "M1.W.1")

        Returns:
            Rule data or None if not found
        """
        # TODO 6: Search with the exact rule_id
        # This is a simple keyword search for now
        results = self.store.search(rule_id, n_results=1)

        return results[0] if results else None


# Tool handler for integration with agent
def handle_query_documentation(inputs: dict) -> str:
    """
    Tool handler for the agent.

    Args:
        inputs: {"query": "...", "layer": "..." (optional)}

    Returns:
        JSON string with search results
    """
    import json


    # TODO 7: Create retriever instance (consider caching)
    retriever = DesignRuleRetriever()

    # TODO 8: Extract query and optional layer from inputs
    query = inputs.get("query", "")
    layer = inputs.get("layer")

    # TODO 9: Call retriever.query() and return result

    result = retriever.query(query, layer=layer)
    return json.dumps({"context": result})      


# Test function
if __name__ == "__main__":
    print("=== Design Rule Retriever Test ===\n")

    # Initialize retriever
    retriever = DesignRuleRetriever()

    # Test queries
    test_queries = [
        "What is the minimum width for Metal1?",
        "What is the via spacing requirement?",
        "How much must poly extend past active?",
    ]

    for query in test_queries:
        print(f"Q: {query}")
        print("-" * 50)
        context = retriever.query(query, n_results=2)
        print(context)
        print("\n")
