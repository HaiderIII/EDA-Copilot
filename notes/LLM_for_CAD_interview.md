# LLM & AI for CAD - Interview Notes

## Why Apple Asks About LLM/AI

From the job posting:
> "Fundamentals and experience in AI/LLM algorithms and architectures"

Apple wants CAD engineers who can integrate AI into EDA workflows for automation.

---

## 1. What is an LLM?

**Large Language Model** = Neural network trained on massive text data to understand and generate language.

```
Input: "Write a SKILL script to export netlists"
  ↓
LLM (billions of parameters)
  ↓
Output: Working SKILL code
```

### Key Examples
| Model | Company | Use Case |
|-------|---------|----------|
| GPT-4 | OpenAI | General purpose |
| Claude | Anthropic | Code generation |
| Gemini | Google | Multimodal |
| Llama | Meta | Open source |
| Copilot | GitHub | Code completion |

---

## 2. LLM Architecture Basics

### Transformer Architecture (know this!)

```
┌─────────────────────────────────────┐
│           TRANSFORMER               │
│                                     │
│  Input: "Generate testbench for"    │
│            ↓                        │
│  ┌─────────────────────┐            │
│  │   Tokenization      │            │
│  │   "Generate" → 1234 │            │
│  └─────────────────────┘            │
│            ↓                        │
│  ┌─────────────────────┐            │
│  │   Embedding Layer   │            │
│  │   Token → Vector    │            │
│  └─────────────────────┘            │
│            ↓                        │
│  ┌─────────────────────┐            │
│  │   Self-Attention    │  ← KEY!    │
│  │   (context aware)   │            │
│  └─────────────────────┘            │
│            ↓                        │
│  ┌─────────────────────┐            │
│  │   Feed Forward      │            │
│  └─────────────────────┘            │
│            ↓                        │
│  Output: Next token prediction      │
└─────────────────────────────────────┘
```

### Key Concepts to Know

| Term | Meaning | Interview Answer |
|------|---------|------------------|
| **Token** | Word or subword unit | "LLMs process text as tokens, not characters" |
| **Embedding** | Vector representation of token | "Converts words to numbers the model understands" |
| **Attention** | Mechanism to focus on relevant context | "Allows model to understand relationships between words" |
| **Context Window** | Max tokens model can process | "GPT-4 has 128K, Claude has 200K tokens" |
| **Temperature** | Randomness in output | "0 = deterministic, 1 = creative" |
| **Fine-tuning** | Training on specific data | "Adapt general model to CAD-specific tasks" |

---

## 3. LLM Applications in CAD/EDA

### Use Cases for Apple CAD Team

```
┌─────────────────────────────────────────────────────┐
│  LLM USE CASES IN CUSTOM DESIGN                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. CODE GENERATION                                 │
│     - SKILL scripts for Virtuoso                    │
│     - Python automation scripts                     │
│     - Testbench generation                          │
│                                                     │
│  2. DOCUMENTATION                                   │
│     - Auto-generate design docs                     │
│     - Explain legacy code                           │
│     - Create user guides                            │
│                                                     │
│  3. LOG ANALYSIS                                    │
│     - Parse simulation logs                         │
│     - Identify errors/warnings                      │
│     - Suggest fixes                                 │
│                                                     │
│  4. DESIGN ASSISTANCE                               │
│     - Circuit topology suggestions                  │
│     - Parameter optimization                        │
│     - DRC/LVS error explanation                     │
│                                                     │
│  5. KNOWLEDGE BASE                                  │
│     - Query internal docs                           │
│     - Answer methodology questions                  │
│     - Onboard new engineers faster                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Example: LLM for SKILL Code Generation

```python
# Prompt to LLM
prompt = """
Generate a SKILL script that:
1. Opens a cellview
2. Exports the netlist to a file
3. Runs DRC check
"""

# LLM Output
skill_code = """
procedure(exportAndCheck(libName cellName)
  let((cv)
    cv = dbOpenCellViewByType(libName cellName "schematic")
    nlExport(cv "/tmp/netlist.sp")
    drc(cv)
    dbClose(cv)
  )
)
"""
```

---

## 4. How to Integrate LLM in CAD Workflow

### Architecture Example

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Engineer   │────▶│  LLM API    │────▶│  CAD Tool   │
│  Request    │     │  (Claude/   │     │  (Virtuoso) │
│             │     │   GPT)      │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   ▼                   │
       │         ┌─────────────────┐           │
       │         │  Generated      │           │
       │         │  SKILL/Python   │───────────┘
       │         │  Code           │
       │         └─────────────────┘
       │                   │
       ▼                   ▼
┌─────────────────────────────────────┐
│  Validation & Review                │
│  (Human in the loop)                │
└─────────────────────────────────────┘
```

### Python Integration Example

```python
import openai  # or anthropic for Claude

def generate_skill_script(task_description: str) -> str:
    """Use LLM to generate SKILL code for CAD automation."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Cadence SKILL expert."},
            {"role": "user", "content": task_description}
        ],
        temperature=0.2  # Low for code generation
    )

    return response.choices[0].message.content


def analyze_simulation_log(log_path: str) -> dict:
    """Use LLM to analyze simulation errors."""

    with open(log_path) as f:
        log_content = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyze this simulation log and identify errors."},
            {"role": "user", "content": log_content}
        ]
    )

    return {"analysis": response.choices[0].message.content}
```

---

## 5. Key Terms for Interview

| Term | Definition | CAD Context |
|------|------------|-------------|
| **Prompt Engineering** | Crafting inputs for best output | Write prompts for SKILL generation |
| **RAG** (Retrieval Augmented Generation) | LLM + document search | Query internal CAD documentation |
| **Fine-tuning** | Train on specific data | Train on Apple's SKILL codebase |
| **Hallucination** | LLM makes up false info | Always validate generated code |
| **Few-shot Learning** | Give examples in prompt | Show examples of good SKILL code |
| **Chain of Thought** | Step-by-step reasoning | Debug complex simulation issues |
| **Embeddings** | Vector representation | Search similar design patterns |
| **Vector Database** | Store embeddings | Index all internal CAD scripts |

---

## 6. Challenges & Limitations

### What to Mention in Interview

```
┌─────────────────────────────────────────────────────┐
│  CHALLENGES                                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. HALLUCINATION                                   │
│     "LLMs can generate plausible but wrong code"    │
│     → Solution: Human review, testing               │
│                                                     │
│  2. SECURITY                                        │
│     "Can't send proprietary designs to external AI" │
│     → Solution: On-premise models, private API      │
│                                                     │
│  3. CONTEXT LIMITS                                  │
│     "Large netlists exceed context window"          │
│     → Solution: Chunking, summarization             │
│                                                     │
│  4. DOMAIN KNOWLEDGE                                │
│     "Generic LLMs don't know SKILL well"            │
│     → Solution: Fine-tuning, RAG with docs          │
│                                                     │
│  5. REPRODUCIBILITY                                 │
│     "Same prompt can give different outputs"        │
│     → Solution: temperature=0, seed parameter       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 7. Interview Questions & Answers

### Q: "How would you use LLM in CAD automation?"

**Answer:**
> "I would use LLMs for code generation and log analysis. For example, engineers could describe a task in natural language, and the LLM generates SKILL or Python code. For simulation logs, the LLM can quickly identify errors and suggest fixes. I would implement RAG to query internal documentation, so engineers get answers based on Apple's specific methodologies. Of course, all generated code needs human review before execution."

---

### Q: "What is the Transformer architecture?"

**Answer:**
> "Transformer is the neural network architecture behind modern LLMs. The key innovation is the self-attention mechanism, which allows the model to understand relationships between all words in the input simultaneously. This is more efficient than previous RNN/LSTM approaches that processed words sequentially. It consists of tokenization, embedding layers, multiple attention heads, and feed-forward networks."

---

### Q: "How would you handle security concerns with LLMs?"

**Answer:**
> "For proprietary designs, I would never send data to external APIs. Options include: running open-source models like Llama on-premise, using private cloud deployments, or fine-tuning smaller models on internal data. For less sensitive tasks, we can use anonymized or synthetic examples. The key is classifying what data can and cannot be exposed."

---

### Q: "What is RAG and why is it useful?"

**Answer:**
> "RAG stands for Retrieval Augmented Generation. Instead of relying only on the LLM's training data, we first search a knowledge base for relevant documents, then provide those as context to the LLM. For CAD, this means indexing all internal SKILL scripts, methodology docs, and design guides. When an engineer asks a question, the system retrieves relevant docs and the LLM answers based on that context. This reduces hallucination and keeps answers up-to-date."

---

## 8. Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│  LLM QUICK REFERENCE FOR INTERVIEW                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Architecture: Transformer (attention mechanism)    │
│  Key models: GPT-4, Claude, Llama, Gemini          │
│                                                     │
│  CAD Uses:                                          │
│    - SKILL/Python code generation                   │
│    - Log analysis and debugging                     │
│    - Documentation search (RAG)                     │
│    - Design assistance                              │
│                                                     │
│  Key techniques:                                    │
│    - Prompt engineering                             │
│    - Fine-tuning for domain                         │
│    - RAG for knowledge base                         │
│    - Temperature=0 for consistency                  │
│                                                     │
│  Challenges:                                        │
│    - Hallucination → validate output                │
│    - Security → on-premise models                   │
│    - Context limits → chunking                      │
│                                                     │
│  Python libraries:                                  │
│    - openai, anthropic, langchain, llamaindex       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Keywords for Interview

- "Transformer architecture with self-attention"
- "Prompt engineering for code generation"
- "RAG for internal documentation"
- "Fine-tuning on domain-specific data"
- "Human-in-the-loop validation"
- "On-premise deployment for security"
- "Temperature control for reproducibility"
