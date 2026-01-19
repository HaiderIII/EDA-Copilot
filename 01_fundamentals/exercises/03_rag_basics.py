"""
Exercise 3: RAG (Retrieval-Augmented Generation)
================================================

GOAL: Build a simple RAG system for EDA documentation

RAG allows LLMs to answer questions about YOUR specific data:
- PDK documentation
- Design rule manuals
- Internal wikis/guides
- Company-specific processes

WHAT YOU'LL LEARN:
- Document chunking strategies
- Embedding and vector search
- Integrating retrieval with generation
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# =============================================================================
# STEP 1: Sample EDA Documentation
# =============================================================================

# In real life, this would be loaded from PDFs/docs
# We'll simulate with sample design rule content

SAMPLE_DOCUMENTS = [
    {
        "id": "drm_m1_rules",
        "title": "ASAP7 Metal1 Design Rules",
        "content": """
Metal1 (M1) Design Rules for ASAP7 PDK

1. Minimum Width (M1.W.1)
   - Minimum width: 18nm
   - This applies to all Metal1 shapes
   - Violation severity: Critical

2. Minimum Spacing (M1.S.1)
   - Minimum spacing: 18nm (same net)
   - Minimum spacing: 21nm (different net)
   - Measured edge-to-edge

3. Minimum Area (M1.A.1)
   - Minimum area: 0.00202 um²
   - Small shapes may cause reliability issues

4. Via Enclosure (M1.E.1)
   - Minimum enclosure of V0: 5nm on two opposite sides
   - Minimum enclosure of V0: 1nm on remaining sides
"""
    },
    {
        "id": "drm_m2_rules",
        "title": "ASAP7 Metal2 Design Rules",
        "content": """
Metal2 (M2) Design Rules for ASAP7 PDK

1. Minimum Width (M2.W.1)
   - Minimum width: 18nm
   - Preferred direction: Horizontal

2. Minimum Spacing (M2.S.1)
   - Minimum spacing: 18nm (same net)
   - Minimum spacing: 21nm (different net)

3. Via1 Enclosure (M2.E.1)
   - Minimum enclosure of V1: 5nm on two opposite sides
   - Critical for signal integrity
"""
    },
    {
        "id": "skill_best_practices",
        "title": "SKILL Programming Best Practices",
        "content": """
SKILL Programming Best Practices for Virtuoso Automation

1. Variable Naming
   - Use camelCase for local variables
   - Use descriptive names (cellView, not cv)
   - Prefix global variables with g_

2. Error Handling
   - Always check dbOpenCellViewByType return value
   - Use errset/errsetstring for graceful failures
   - Close cellviews in finally blocks

3. Performance Tips
   - Avoid repeated db queries in loops
   - Cache frequently accessed properties
   - Use foreach instead of for when possible

4. Common Patterns
   - Opening cellviews: dbOpenCellViewByType(lib cell view nil "r")
   - Iterating instances: foreach(inst cv~>instances ...)
   - Creating shapes: dbCreateRect(cv layer list(x1:y1 x2:y2))
"""
    },
    {
        "id": "simulation_guide",
        "title": "Spectre Simulation Setup Guide",
        "content": """
Spectre Simulation Setup for Analog Circuits

1. DC Analysis
   - Purpose: Find operating point
   - Key options: saveOppoint=yes for detailed bias info
   - Common issues: Convergence failures with large circuits

2. AC Analysis
   - Purpose: Small-signal frequency response
   - Setup: Specify start/stop frequency, sweep type (dec/lin)
   - Output: Magnitude and phase plots

3. Transient Analysis
   - Purpose: Time-domain behavior
   - Key settings: Stop time, max timestep
   - Memory considerations: Long simulations need more RAM

4. Monte Carlo
   - Purpose: Statistical analysis
   - Types: Process variation, mismatch
   - Typical runs: 100-1000 iterations
"""
    },
    {
        "id": "lvs_debugging",
        "title": "LVS Debugging Guide",
        "content": """
Common LVS Issues and Solutions

1. Device Count Mismatch
   - Symptom: More/fewer devices in layout than schematic
   - Common cause: Merged devices, missing connections
   - Debug: Use LVS report to identify specific devices

2. Net Short
   - Symptom: Two schematic nets connected in layout
   - Common cause: Overlapping metals on different nets
   - Debug: Highlight shorted nets in layout

3. Net Open
   - Symptom: One schematic net split in layout
   - Common cause: Missing via, broken path
   - Debug: Trace the net path manually

4. Property Mismatch
   - Symptom: Device exists but properties differ
   - Common cause: Wrong W/L, finger count
   - Debug: Compare extracted vs schematic properties
"""
    }
]


# =============================================================================
# STEP 2: Simple In-Memory Vector Store
# =============================================================================

def simple_embedding(text: str) -> list[float]:
    """
    SIMPLIFIED embedding for demonstration.

    In production, use:
    - sentence-transformers (free, local)
    - OpenAI embeddings API
    - Voyage AI embeddings

    This demo uses keyword matching instead of real embeddings.
    """
    # Keywords for each topic (simplified semantic matching)
    keywords = {
        "metal": 0.0, "width": 0.1, "spacing": 0.2, "via": 0.3, "enclosure": 0.4,
        "skill": 0.5, "procedure": 0.6, "function": 0.7, "code": 0.8,
        "simulation": 0.9, "dc": 1.0, "ac": 1.1, "transient": 1.2, "spectre": 1.3,
        "lvs": 1.4, "drc": 1.5, "layout": 1.6, "schematic": 1.7,
        "error": 1.8, "debug": 1.9, "violation": 2.0
    }

    text_lower = text.lower()
    embedding = []

    for keyword, value in keywords.items():
        if keyword in text_lower:
            embedding.append(value)
        else:
            embedding.append(-1)

    return embedding


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2) if a >= 0 and b >= 0)
    mag1 = sum(a * a for a in vec1 if a >= 0) ** 0.5
    mag2 = sum(b * b for b in vec2 if b >= 0) ** 0.5

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot_product / (mag1 * mag2)


class SimpleVectorStore:
    """In-memory vector store for demonstration"""

    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_document(self, doc_id: str, title: str, content: str):
        self.documents.append({
            "id": doc_id,
            "title": title,
            "content": content
        })
        self.embeddings.append(simple_embedding(content))

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        query_embedding = simple_embedding(query)

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            sim = cosine_similarity(query_embedding, doc_embedding)
            similarities.append((sim, i))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Return top_k results
        results = []
        for sim, idx in similarities[:top_k]:
            results.append({
                "document": self.documents[idx],
                "score": sim
            })

        return results


# =============================================================================
# STEP 3: RAG Pipeline
# =============================================================================

def build_vector_store() -> SimpleVectorStore:
    """Build vector store from sample documents"""
    store = SimpleVectorStore()

    for doc in SAMPLE_DOCUMENTS:
        store.add_document(doc["id"], doc["title"], doc["content"])
        print(f"  Indexed: {doc['title']}")

    return store


def rag_query(store: SimpleVectorStore, query: str) -> str:
    """
    Complete RAG pipeline:
    1. Retrieve relevant documents
    2. Build augmented prompt
    3. Generate response
    """
    client = anthropic.Anthropic()

    # Step 1: Retrieve relevant documents
    print(f"\n[RAG] Searching for: '{query}'")
    results = store.search(query, top_k=2)

    print(f"[RAG] Found {len(results)} relevant documents:")
    for r in results:
        print(f"  - {r['document']['title']} (score: {r['score']:.2f})")

    # Step 2: Build context from retrieved documents
    context = "\n\n---\n\n".join([
        f"Document: {r['document']['title']}\n{r['document']['content']}"
        for r in results
    ])

    # Step 3: Build augmented prompt
    augmented_prompt = f"""Based on the following documentation, answer the user's question.
If the answer is not in the documentation, say so.

DOCUMENTATION:
{context}

USER QUESTION: {query}

Provide a concise, accurate answer based on the documentation above."""

    # Step 4: Generate response
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": augmented_prompt}]
    )

    return response.content[0].text


# =============================================================================
# STEP 4: Demo
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("EXERCISE 3: RAG (RETRIEVAL-AUGMENTED GENERATION)")
    print("=" * 60)

    # Build the vector store
    print("\n[SETUP] Building vector store...")
    store = build_vector_store()

    # Test queries
    test_queries = [
        "What is the minimum width for Metal1?",
        "How do I debug an LVS net short error?",
        "What are the best practices for SKILL variable naming?",
        "How do I set up a transient simulation?"
    ]

    for query in test_queries:
        print("\n" + "-" * 60)
        answer = rag_query(store, query)
        print(f"\n[ANSWER]\n{answer}")

    print("\n" + "=" * 60)
    print("EXERCISE COMPLETE!")
    print("=" * 60)
    print("""
KEY TAKEAWAYS:
1. RAG = Retrieve + Augment + Generate
2. Embedding quality matters - use production embeddings (sentence-transformers)
3. Chunk size affects retrieval quality - experiment with different sizes
4. This pattern lets LLMs answer questions about YOUR specific documentation!

FOR PRODUCTION:
- Use chromadb or similar vector database
- Use sentence-transformers for embeddings (free, local)
- Implement proper document chunking
- Add metadata filtering

INTERVIEW TIP: Discuss how RAG could help with:
- PDK documentation Q&A
- Design rule lookups
- Searching internal wikis
- Finding similar past designs

NEXT: Let's build the full EDA Copilot agent!
""")


if __name__ == "__main__":
    main()
