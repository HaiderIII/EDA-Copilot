# LLM Fundamentals for EDA Applications

> **Goal**: Understand LLM concepts well enough to discuss them confidently in your Apple interview.

---

## 1. What is an LLM?

A **Large Language Model** is a neural network trained on massive text data to predict the next token (word/subword) in a sequence.

### Key Architecture: Transformer

```
Input Text → Tokenization → Embeddings → Transformer Layers → Output Probabilities
```

**Interview-ready explanation:**
> "An LLM like Claude uses a transformer architecture with attention mechanisms.
> The key innovation is self-attention, which allows the model to weigh the
> relevance of different parts of the input when generating each output token."

### Important Concepts to Know:

| Concept | Definition | EDA Relevance |
|---------|------------|---------------|
| **Tokens** | Text chunks (words/subwords) the model processes | Longer SKILL code = more tokens = higher cost |
| **Context Window** | Maximum tokens the model can process at once | Limits how much documentation/code we can include |
| **Temperature** | Randomness in output (0=deterministic, 1=creative) | Use low temp (0.1-0.3) for code generation |
| **Embedding** | Vector representation of text | Used for semantic search in RAG |

---

## 2. How LLMs Generate Text

### Autoregressive Generation
```
Prompt: "Write a SKILL function to"
Step 1: Model predicts "create" (most likely next token)
Step 2: Model predicts "a"
Step 3: Model predicts "rectangle"
...continues until stop condition
```

### Why This Matters for EDA:
- LLMs don't "understand" circuits - they predict likely text patterns
- Quality depends heavily on **prompt engineering** and **context**
- For reliable code generation, we need structured outputs (JSON, function calling)

---

## 3. Key LLM Capabilities for CAD

### 3.1 Prompt Engineering

**Basic prompt:**
```
Write a SKILL function to create a rectangle.
```

**Engineered prompt (much better):**
```
You are an expert Cadence SKILL programmer. Generate a SKILL function that:
- Creates a rectangle in the current cellview
- Takes parameters: layer, x1, y1, x2, y2
- Includes error handling for invalid coordinates
- Follows Cadence coding conventions

Output only the code, no explanations.
```

### 3.2 Function Calling (Tool Use)

This is **critical** for the Apple role. Instead of free-form text, the LLM can call predefined functions:

```python
# Define tools the LLM can use
tools = [
    {
        "name": "run_simulation",
        "description": "Run a circuit simulation in Spectre",
        "parameters": {
            "netlist": "Path to the netlist file",
            "analysis": "Type of analysis (dc, ac, tran)",
            "options": "Simulation options"
        }
    },
    {
        "name": "generate_skill_code",
        "description": "Generate SKILL code for Virtuoso automation",
        "parameters": {
            "task": "Description of what the code should do",
            "context": "Current design context"
        }
    }
]
```

**Why Apple cares:** This lets you build reliable automation where the LLM acts as an intelligent router to your existing CAD tools.

### 3.3 RAG (Retrieval-Augmented Generation)

**Problem:** LLMs don't know your specific PDK, design rules, or internal documentation.

**Solution:** RAG = Retrieve relevant docs → Add to prompt → Generate

```
User Query: "What's the minimum metal1 width in our process?"

Step 1: RETRIEVE - Search your DRM documentation
Step 2: AUGMENT  - Add found text to the prompt
Step 3: GENERATE - LLM answers using the retrieved context

Result: "According to the ASAP7 DRM section 4.2, minimum M1 width is 18nm."
```

---

## 4. Claude API Specifics

### Basic API Call
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a SKILL function to create a via"}
    ]
)

print(response.content[0].text)
```

### With System Prompt (Important!)
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="""You are an expert EDA CAD engineer at Apple.
    You help analog/RF designers with:
    - SKILL programming for Virtuoso automation
    - Simulation setup and analysis
    - Design rule checks and LVS debugging

    Always provide code that is production-ready and well-documented.""",
    messages=[
        {"role": "user", "content": "Create a function to extract all transistors from a schematic"}
    ]
)
```

### Tool Use with Claude
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[
        {
            "name": "run_drc",
            "description": "Run Design Rule Check on current layout",
            "input_schema": {
                "type": "object",
                "properties": {
                    "cellname": {"type": "string", "description": "Cell to check"},
                    "ruleset": {"type": "string", "description": "DRC ruleset to use"}
                },
                "required": ["cellname"]
            }
        }
    ],
    messages=[
        {"role": "user", "content": "Check the DRC for my amplifier layout"}
    ]
)

# Claude will return a tool_use block if it wants to call the tool
```

---

## 5. LLM Limitations (Know These for Interview!)

| Limitation | Impact on EDA | Mitigation |
|------------|---------------|------------|
| **Hallucination** | May generate invalid SKILL syntax or wrong API calls | Validate outputs, use function calling |
| **No real-time data** | Doesn't know your current design state | Pass context explicitly |
| **Context limits** | Can't read entire codebase at once | Use RAG, selective context |
| **Non-deterministic** | Same prompt may give different results | Use temperature=0, seed parameter |
| **No execution** | Can't actually run simulations | Tool calling to external systems |

---

## 6. Interview Talking Points

### "Why use LLMs for CAD automation?"

> "LLMs excel at understanding natural language intent and mapping it to
> structured actions. For CAD, this means designers can describe what they
> want in plain English - 'check all metal spacing violations in the power
> grid' - and the LLM translates this to the appropriate SKILL commands or
> tool invocations. This reduces the barrier to automation and makes existing
> CAD infrastructure more accessible."

### "How would you ensure reliability?"

> "Three key strategies:
> 1. **Function calling** - constrain outputs to predefined tool schemas
> 2. **Validation** - parse and syntax-check generated code before execution
> 3. **Human-in-the-loop** - for critical operations, show the plan before executing"

### "What are the risks?"

> "The main risks are hallucination and non-determinism. An LLM might generate
> SKILL code that looks correct but has subtle bugs. Mitigation includes
> extensive testing, sandboxed execution environments, and using the LLM as
> an assistant rather than autonomous agent for critical paths."

---

## Exercises

Complete these in `01_fundamentals/exercises/`:

1. **Exercise 1**: Make your first Claude API call
2. **Exercise 2**: Compare outputs at different temperatures
3. **Exercise 3**: Implement a simple function calling example
4. **Exercise 4**: Build a basic RAG retriever

---

## Next: [EDA Concepts](./eda_concepts.md)
