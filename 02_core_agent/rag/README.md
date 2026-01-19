# RAG System for EDA Copilot

## Project Progression

This document traces the steps of building a RAG (Retrieval-Augmented Generation) system to query ASAP7 design rules.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAG System Architecture                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   User Query                                                                │
│       │                                                                     │
│       ▼                                                                     │
│   ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐   │
│   │   Retriever     │──────│  Vector Store   │──────│   ChromaDB      │   │
│   │  (retriever.py) │      │(vector_store.py)│      │   (Database)    │   │
│   └─────────────────┘      └─────────────────┘      └─────────────────┘   │
│           │                        ▲                                        │
│           │                        │                                        │
│           ▼                        │                                        │
│   ┌─────────────────┐      ┌─────────────────┐                             │
│   │  Formatted      │      │ Document Loader │                             │
│   │  Context        │      │(document_loader)│                             │
│   └─────────────────┘      └─────────────────┘                             │
│           │                        ▲                                        │
│           ▼                        │                                        │
│       LLM Agent              design_rules.txt                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Data (design_rules.txt) ✅

**Goal**: Create a design rules file in a structured format.

**File**: `data/design_rules.txt`

### Rule Format

```
M1.W.1 - Minimum Width
Layer: Metal1
Value: 18nm
Description: All Metal1 shapes must have a minimum width of 18nm.

---

M1.S.1 - Minimum Spacing
Layer: Metal1
Value: 18nm
Description: Minimum spacing between two Metal1 shapes is 18nm.
```

### Rules Created

| Category | Number of Rules | Examples |
|----------|-----------------|----------|
| Metal1 (M1) | 5 | Width, Spacing, Area, Extension |
| Metal2 (M2) | 5 | Width, Spacing, Area, Extension |
| VIA1 | 4 | Size, Spacing, Array, Enclosure |
| Poly | 5 | Width, Spacing, Gate Extension |
| Active | 4 | Width, Spacing, Area |
| NWELL | 3 | Width, Spacing, Enclosure |
| Contact | 5 | Size, Spacing, Enclosures |
| **Total** | **31 rules** | |

---

## Step 2: Document Loader (document_loader.py) ✅

**Goal**: Parse the rules file and create chunks with metadata.

### Concept: Semantic Chunking

```
┌──────────────────────────────────────────────────────────────┐
│                    design_rules.txt                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │  Rule M1.W │  │  Rule M1.S │  │  Rule M2.W │  ...        │
│  └────────────┘  └────────────┘  └────────────┘             │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼ split("---")
┌──────────────────────────────────────────────────────────────┐
│                     DocumentChunks                           │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ Chunk 1         │  │ Chunk 2         │                   │
│  │ text: "M1.W..." │  │ text: "M1.S..." │  ...              │
│  │ metadata: {     │  │ metadata: {     │                   │
│  │   rule_id,      │  │   rule_id,      │                   │
│  │   layer,        │  │   layer,        │                   │
│  │   value         │  │   value         │                   │
│  │ }               │  │ }               │                   │
│  └─────────────────┘  └─────────────────┘                   │
└──────────────────────────────────────────────────────────────┘
```

### Implemented Code

```python
@dataclass
class DocumentChunk:
    text: str           # Raw text of the rule
    metadata: dict      # rule_id, layer, value, description, source

def load_design_rules(file_path: str) -> list[DocumentChunk]:
    content = Path(file_path).read_text()
    sections = content.split("---")           # Split by rule
    chunks = []
    for section in sections:
        chunk = parse_rule(section)           # Extract metadata
        if chunk:
            chunks.append(chunk)
    return chunks

def parse_rule(rule_text: str) -> DocumentChunk:
    # Extract with regex
    rule_id = re.search(r'^([A-Z0-9.]+)\s*-', rule_text)
    layer = re.search(r'Layer:\s*(.+)', rule_text)
    value = re.search(r'Value:\s*(.+)', rule_text)
    # ... build metadata dict
```

### Test

```bash
cd ~/projects/eda-copilot/02_core_agent/rag
python document_loader.py
```

**Expected output**: `Loaded 31 design rules`

---

## Step 3: Vector Store (vector_store.py) ✅

**Goal**: Store embeddings and enable similarity search.

### Concept: Embeddings and Vector Search

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            How does it work?                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. INDEXING (once)                                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  "M1 minimum width is 18nm"  ──► Embedding Model ──► [0.2, 0.8, ...]│  │
│   │  "M2 spacing rule is 18nm"   ──► Embedding Model ──► [0.3, 0.7, ...]│  │
│   │  "Via size is 18nm x 18nm"   ──► Embedding Model ──► [0.1, 0.4, ...]│  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                        │                                    │
│                                        ▼                                    │
│                               ┌─────────────────┐                          │
│                               │    ChromaDB     │                          │
│                               │  (Vector Store) │                          │
│                               └─────────────────┘                          │
│                                                                             │
│   2. SEARCH (on each query)                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Query: "What's M1 width?"                                          │  │
│   │           │                                                          │  │
│   │           ▼                                                          │  │
│   │  Embedding Model ──► [0.2, 0.8, ...] ◄── Similar!                   │  │
│   │           │                                                          │  │
│   │           ▼                                                          │  │
│   │  Find nearest vectors (cosine similarity)                           │  │
│   │           │                                                          │  │
│   │           ▼                                                          │  │
│   │  Result: "M1 minimum width is 18nm" (distance: 0.23)                │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ChromaDB - What is it?

ChromaDB is a vector database that:
- Stores embeddings (vectors of numbers)
- Performs semantic similarity searches
- Supports metadata filtering (e.g., `layer="Metal1"`)
- Can be persistent (on disk) or in-memory

### Implemented Code

```python
class VectorStore:
    def __init__(self, collection_name: str = "design_rules"):
        # Persistent client (data saved to disk)
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks: list[DocumentChunk]) -> None:
        documents = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [chunk.metadata.get("rule_id") for chunk in chunks]
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def search(self, query: str, n_results: int = 3, layer_filter: str = None):
        where = {"layer": layer_filter} if layer_filter else None
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        return [{"text": t, "metadata": m, "distance": d} for t, m, d in zip(...)]
```

### Test

```bash
cd ~/projects/eda-copilot/02_core_agent/rag
python vector_store.py
```

**Expected output**:
```
=== Search Test ===

Query: What is the minimum metal1 width?

Result 1:
  Rule: M1.W.1
  Distance: 0.4523

Result 2:
  Rule: M2.W.1
  Distance: 0.5012
...
```

---

## Step 4: Retriever (retriever.py) 🔄 IN PROGRESS

**Goal**: High-level interface for the RAG system.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DesignRuleRetriever                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Agent                                                         │
│     │                                                           │
│     │  retriever.query("What's M1 width?")                     │
│     ▼                                                           │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │  DesignRuleRetriever                                    │  │
│   │  ┌───────────────────────────────────────────────────┐  │  │
│   │  │ 1. Search in VectorStore                          │  │  │
│   │  │ 2. Format results for LLM                         │  │  │
│   │  └───────────────────────────────────────────────────┘  │  │
│   └─────────────────────────────────────────────────────────┘  │
│     │                                                           │
│     ▼                                                           │
│   """                                                           │
│   Relevant Design Rules:                                        │
│                                                                 │
│   [Rule M1.W.1 - Metal1]                                       │
│   Value: 18nm                                                   │
│   All Metal1 shapes must have minimum width of 18nm.           │
│   """                                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### TODOs to Implement

```python
class DesignRuleRetriever:
    def __init__(self, data_path: str = None):
        # TODO 1: Set default data path
        # TODO 2: Initialize vector store
        # TODO 3: Load documents and add to vector store

    def query(self, question: str, n_results: int = 3, layer: str = None) -> str:
        # TODO 4: Search the vector store
        # TODO 5: Format results as context string

    def get_rule(self, rule_id: str) -> dict | None:
        # TODO 6: Search with exact rule_id
```

---

## File Structure

```
02_core_agent/rag/
├── __init__.py           # Module initialization
├── README.md             # This file
├── data/
│   └── design_rules.txt  # ✅ 31 ASAP7 rules
├── document_loader.py    # ✅ Parse and chunk documents
├── vector_store.py       # ✅ ChromaDB vector store
└── retriever.py          # 🔄 High-level interface (TODO)
```

---

## Quiz Completed ✅

The quiz `01_fundamentals/exercises/03_quiz_rag.md` was completed successfully.

### Key Concepts Validated:

| Concept | Understood |
|---------|------------|
| RAG = Retrieval-Augmented Generation | ✅ |
| Embeddings = vectors representing meaning | ✅ |
| Semantic chunking (1 chunk = 1 rule) | ✅ |
| Metadata for filtering | ✅ |
| Similarity search vs keyword search | ✅ |
| RAG vs Fine-tuning | ✅ |

---

## Next Steps

1. **Implement `retriever.py`** - TODOs 1-6
2. **Test the complete pipeline** - Query → Search → Format → Return
3. **Integrate with the agent** - Add as a tool
4. **Implement `clear()`** - Missing method in vector_store.py

---

## Useful Commands

```bash
# Test the document loader
python document_loader.py

# Test the vector store
python vector_store.py

# Test the retriever (after implementation)
python retriever.py

# Delete ChromaDB database (reset)
rm -rf chroma_db/
```

---

## Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
