# Quiz 3: RAG (Retrieval-Augmented Generation)

> Complete this quiz BEFORE running `03_rag_basics.py`
> RAG is how you make LLMs answer questions about YOUR specific data

---

## Part 1: The Problem RAG Solves

### Q1. You ask Claude: "What's the minimum M1 width in our company's ASAP7 PDK?"

What's the problem?

- [ ] A) Claude doesn't understand the question
- [X] B) Claude doesn't know YOUR company's specific PDK documentation
- [ ] C) Claude can't process technical questions
- [ ] D) The question is too long

<details>
<summary>Answer</summary>

**B) Claude doesn't know YOUR company's specific PDK documentation**

LLMs are trained on public data. They don't know:
- Your internal PDK variants
- Your company's design rules
- Your proprietary documentation
- Your specific tool configurations

RAG solves this by retrieving YOUR data and adding it to the prompt.

</details>

---

### Q2. What does RAG stand for?
- [ ] A) Rapid Answer Generation
- [X] B) Retrieval-Augmented Generation
- [ ] C) Random Access Generation
- [ ] D) Real-time AI Gateway

<details>
<summary>Answer</summary>

**B) Retrieval-Augmented Generation**

- **Retrieval**: Find relevant documents from your data
- **Augmented**: Add those documents to the prompt
- **Generation**: LLM generates answer using retrieved context

</details>

---

### Q3. What's the RAG workflow?

- [ ] A) User Query → LLM → Answer
- [X] B) User Query → Search Documents → Add to Prompt → LLM → Answer
- [ ] C) User Query → Database → Answer
- [ ] D) User Query → Fine-tune Model → LLM → Answer

<details>
<summary>Answer</summary>

**B) User Query → Search Documents → Add to Prompt → LLM → Answer**

```
┌─────────────────────────────────────────────────────────┐
│                      RAG PIPELINE                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  "What's M1 min width?"                                 │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐    ┌──────────────────────────────┐   │
│  │   SEARCH    │───▶│ Found: "M1.W.1: min width    │   │
│  │  (retrieve) │    │ is 18nm for all shapes..."   │   │
│  └─────────────┘    └──────────────────────────────┘   │
│         │                                               │
│         ▼                                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ AUGMENTED PROMPT:                               │   │
│  │ "Based on this documentation: [retrieved text]  │   │
│  │  Answer: What's M1 min width?"                  │   │
│  └─────────────────────────────────────────────────┘   │
│         │                                               │
│         ▼                                               │
│  ┌─────────────┐                                       │
│  │    LLM      │───▶ "M1 minimum width is 18nm"        │
│  └─────────────┘                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

</details>

---

## Part 2: Embeddings & Vector Search

### Q4. What is an "embedding"?
- [ ] A) A way to embed images in documents
- [X] B) A vector (list of numbers) representing the meaning of text
- [ ] C) A database table
- [ ] D) A type of neural network

<details>
<summary>Answer</summary>

**B) A vector (list of numbers) representing the meaning of text**

Example:
```
"Metal1 spacing rule" → [0.12, -0.45, 0.78, 0.23, ...]  (hundreds of numbers)
"M1 minimum distance" → [0.11, -0.44, 0.79, 0.22, ...]  (similar vector!)
```

Similar meanings = similar vectors. This enables semantic search.

</details>

---

### Q5. Why use embeddings instead of keyword search?

User searches: "M1 gap requirements"
Document contains: "Metal1 spacing rules"

- [ ] A) Keyword search would find it (exact match)
- [X] B) Embedding search finds it (semantic similarity), keyword search might miss it
- [ ] C) Both would fail
- [ ] D) Embeddings are faster

<details>
<summary>Answer</summary>

**B) Embedding search finds it (semantic similarity), keyword search might miss it**

- "gap" ≠ "spacing" (keyword mismatch)
- But embeddings for "gap requirements" and "spacing rules" are similar
- Semantic search understands meaning, not just words

</details>

---

### Q6. What is a "vector database"?
- [ ] A) A database that only stores vectors
- [X] B) A database optimized for similarity search on embeddings
- [ ] C) A traditional SQL database
- [ ] D) A type of graph database

<details>
<summary>Answer</summary>

**B) A database optimized for similarity search on embeddings**

Examples: ChromaDB, Pinecone, Weaviate, FAISS

They efficiently answer: "Find the 5 documents most similar to this query embedding"

</details>

---

## Part 3: Document Processing

### Q7. You have a 500-page PDK manual. How do you use it with RAG?
- [ ] A) Send the entire document with every query
- [X] B) Split into chunks, embed each chunk, search for relevant chunks
- [ ] C) Train a new LLM on the document
- [ ] D) Convert to a different format

<details>
<summary>Answer</summary>

**B) Split into chunks, embed each chunk, search for relevant chunks**

Why chunking?
1. Context limits - can't send 500 pages in one prompt
2. Precision - only retrieve relevant sections
3. Cost - fewer tokens = lower cost

Typical chunk size: 200-1000 tokens

</details>

---

### Q8. What's a good chunking strategy for design rule documents?

- [ ] A) Fixed 500-character chunks
- [X] B) One chunk per rule/section (semantic chunking)
- [ ] C) One chunk per page
- [ ] D) Random splitting

<details>
<summary>Answer</summary>

**B) One chunk per rule/section (semantic chunking)**

Design rules have natural boundaries:
```
Chunk 1: "M1.W.1 - Minimum Width: 18nm for all Metal1 shapes..."
Chunk 2: "M1.S.1 - Minimum Spacing: 18nm between Metal1..."
Chunk 3: "M1.A.1 - Minimum Area: 0.00202um² required..."
```

Each chunk is self-contained and meaningful.

</details>

---

### Q9. What metadata should you store with each chunk?

- [ ] A) Nothing, just the text
- [X] B) Source document, section, page number, rule ID
- [ ] C) Only the embedding vector
- [ ] D) The user who created it

<details>
<summary>Answer</summary>

**B) Source document, section, page number, rule ID**

Metadata enables:
- Filtering: "Only search M1 rules"
- Citation: "According to DRM page 45..."
- Debugging: "Why did it retrieve this chunk?"

```python
{
    "text": "M1.W.1 - Minimum Width: 18nm...",
    "metadata": {
        "source": "ASAP7_DRM_v1.0.pdf",
        "section": "Metal1 Rules",
        "page": 45,
        "rule_id": "M1.W.1"
    }
}
```

</details>

---

## Part 4: Retrieval Quality

### Q10. Your RAG system retrieves wrong documents. What's the FIRST thing to check?
- [ ] A) Change the LLM model
- [X] B) Check embedding quality and chunk boundaries
- [ ] C) Add more documents
- [ ] D) Increase temperature

<details>
<summary>Answer</summary>

**B) Check embedding quality and chunk boundaries**

Common issues:
1. Chunks too large → irrelevant content mixed in
2. Chunks too small → missing context
3. Poor embedding model → bad similarity matching
4. Missing metadata → can't filter properly

Debug retrieval BEFORE blaming the LLM.

</details>

---

### Q11. User asks: "What's the M1 width?" but gets chunks about M2.

What might be wrong?

- [ ] A) The LLM is hallucinating
- [X] B) "M1" and "M2" embed to similar vectors; need metadata filtering
- [ ] C) The database is corrupted
- [ ] D) The question is ambiguous

<details>
<summary>Answer</summary>

**B) "M1" and "M2" embed to similar vectors; need metadata filtering**

Both are metal layers, so semantically similar. Solutions:
1. Add metadata filter: `layer="M1"`
2. Include layer in chunk text prominently
3. Use hybrid search (keywords + embeddings)

</details>

---

### Q12. How many chunks should you retrieve per query?
- [ ] A) Always 1
- [ ] B) Always 10
- [X] C) Depends on query complexity and context limits
- [ ] D) All of them

<details>
<summary>Answer</summary>

**C) Depends on query complexity and context limits**

Trade-offs:
- Too few → might miss relevant info
- Too many → noise, higher cost, context limits

Typical: 3-5 chunks for simple queries, more for complex ones.

</details>

---

## Part 5: RAG vs Fine-tuning

### Q13. When should you use RAG vs fine-tuning?

| Scenario | Best Approach |
|----------|---------------|
| Answer questions about current PDK docs | ??? |
| Change the LLM's writing style permanently | ??? |
| Add new design rules that update frequently | ??? |

- [X] A) RAG, Fine-tune, RAG
- [ ] B) Fine-tune, Fine-tune, Fine-tune
- [ ] C) RAG, RAG, RAG
- [ ] D) Fine-tune, RAG, Fine-tune

<details>
<summary>Answer</summary>

**A) RAG, Fine-tune, RAG**

- **PDK docs** → RAG (document-based, can update easily)
- **Writing style** → Fine-tune (behavioral change)
- **Updating rules** → RAG (just update the documents, no retraining)

RAG is preferred when:
- Data changes frequently
- You need citations/sources
- You don't want to retrain models

</details>

---

### Q14. What's the main advantage of RAG over fine-tuning for EDA?
- [ ] A) RAG is always more accurate
- [X] B) RAG allows updating documentation without retraining
- [ ] C) RAG is free
- [ ] D) RAG doesn't require an LLM

<details>
<summary>Answer</summary>

**B) RAG allows updating documentation without retraining**

PDK versions change. Design rules update. New processes arrive.

With RAG: Update the document database → immediate effect
With fine-tuning: Collect new data → retrain → deploy → expensive!

</details>

---

## Part 6: Interview Application

### Q15. Interviewer: "How would you help designers find information in our 1000-page DRM?"

Best answer:

- [ ] A) "Train a custom LLM on the document"
- [X] B) "Build a RAG system: chunk the DRM, embed chunks, enable natural language queries"
- [ ] C) "Use better keyword search"
- [ ] D) "That's not possible with current AI"

<details>
<summary>Answer</summary>

**B) "Build a RAG system: chunk the DRM, embed chunks, enable natural language queries"**

Interview-ready explanation:
> "I'd build a RAG pipeline:
> 1. Parse the DRM into semantic chunks (one per rule)
> 2. Generate embeddings for each chunk
> 3. Store in a vector database with metadata (rule ID, layer, page)
> 4. When a designer asks a question, find similar chunks and include them in the prompt
> 5. The LLM answers using the retrieved context
>
> This lets designers ask 'What's the via enclosure for M3?' instead of searching through pages."

</details>

---

## Score Yourself

| Score | Level |
|-------|-------|
| 15/15 | Expert - You understand production RAG |
| 12-14 | Strong - Review edge cases |
| 9-11 | Good foundation - Focus on retrieval quality |
| <9 | Need more study - RAG is crucial for EDA |

---

## Now Run the Code!

```bash
cd ~/projects/eda-copilot
source venv/bin/activate
python 01_fundamentals/exercises/03_rag_basics.py
```

Watch:
1. How documents are indexed
2. How search finds relevant chunks
3. How retrieved context is added to the prompt
4. How the LLM uses that context to answer
