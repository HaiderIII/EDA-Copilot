# EDA Copilot - Interview Presentation Guide

## Quick Start (30 seconds)

```bash
cd ~/projects/eda-copilot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run demos
cd 02_core_agent
python agent.py --demo
```

---

## Presentation Flow (10-15 minutes)

### 1. Introduction (2 minutes)

**What is EDA Copilot?**

> "I built an LLM-powered assistant that helps analog circuit designers with
> common CAD tasks. It demonstrates how we can integrate AI into the Virtuoso
> workflow without replacing existing tools - instead, making them more accessible."

**Architecture Overview:**

```
┌─────────────────────────────────────────────────────────┐
│                     EDA COPILOT                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Natural Language  ────────────▶  Claude API           │
│                                       │                 │
│                                       ▼                 │
│                              Tool Selection             │
│                                       │                 │
│              ┌────────────────────────┼───────────┐     │
│              ▼            ▼           ▼           ▼     │
│         ┌────────┐  ┌─────────┐  ┌────────┐  ┌──────┐   │
│         │ SKILL  │  │ Circuit │  │ Design │  │ RAG  │   │
│         │ Gen    │  │Analyzer │  │ Rules  │  │Query │   │
│         └────────┘  └─────────┘  └────────┘  └──────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 2. Live Demo (5-7 minutes)

#### Demo 1: Design Rule Query

```python
# In interactive mode
"What is the minimum Metal1 width in ASAP7?"
```

**Highlight:**
- Natural language understanding
- Tool selection (query_design_rule)
- Structured response

#### Demo 2: Code Generation

```python
"Generate SKILL code to count all transistors in a schematic"
```

**Highlight:**
- Correct SKILL syntax
- Error handling included
- Comments for readability

#### Demo 3: Multi-turn Conversation

```python
"I need to check symmetry in a current mirror"
"Generate code to compare two transistor W/L ratios"
"Add error handling if transistors aren't found"
```

**Highlight:**
- Context retention
- Iterative refinement
- Building on previous answers

---

### 3. Technical Deep Dive (3-5 minutes)

#### Key LLM Concepts Used

1. **Function Calling (Tool Use)**
   - Most important feature for CAD integration
   - LLM decides WHICH tool and WHAT parameters
   - Constrained outputs = reliable automation

   ```python
   tools = [{
       "name": "generate_skill_code",
       "description": "...",
       "input_schema": {...}
   }]
   ```

2. **System Prompts**
   - Define agent's expertise and behavior
   - Critical for domain-specific performance

3. **Agentic Loop**
   - Multiple tool calls per query
   - Results feed back to LLM
   - Continues until final answer

#### Production Considerations

| Challenge | Solution |
|-----------|----------|
| Hallucination | Tool validation, code parsing |
| Non-determinism | Low temperature, seed parameter |
| Context limits | RAG for documentation |
| Integration | Simulate tools → Real Virtuoso APIs |

---

### 4. Why This Matters for Apple (2 minutes)

**Direct Value:**

1. **Designer Productivity**
   - Reduce time spent on repetitive automation
   - Lower barrier to SKILL programming
   - Instant access to design rules

2. **Knowledge Capture**
   - Expert knowledge embedded in prompts
   - RAG makes tribal knowledge searchable
   - New engineers ramp up faster

3. **Integration Path**
   - Tools map 1:1 to Virtuoso APIs
   - Can extend to ADE, Calibre, etc.
   - Human-in-the-loop for safety

**Technical Alignment:**

- Python + SKILL (job requirements)
- AI/LLM experience (preferred qualification)
- Automation solutions (core responsibility)

---

## Anticipated Questions & Answers

### Q: "How would you handle production deployment?"

> "Three key considerations:
>
> 1. **Validation** - Parse and syntax-check generated SKILL before execution
> 2. **Sandboxing** - Test environment separate from production designs
> 3. **Audit trail** - Log all tool calls and generated code for review"

### Q: "What about hallucination risks?"

> "The tool-based architecture mitigates this. Instead of free-form text, the
> LLM must call specific functions with defined schemas. Invalid parameters
> get rejected. For code generation, we validate syntax and can run in a
> test environment first."

### Q: "How would you scale this to real PDK documentation?"

> "RAG architecture is already in place. Steps would be:
>
> 1. Parse PDK manuals (PDF extraction)
> 2. Chunk into semantically meaningful sections
> 3. Generate embeddings (sentence-transformers or Voyage)
> 4. Store in vector database (Chroma, Pinecone)
> 5. Retrieve relevant chunks at query time"

### Q: "Why Claude over other LLMs?"

> "For this demo, Claude's strengths are:
> - Strong code generation capabilities
> - Excellent function calling reliability
> - Large context window (200K tokens)
>
> In production, you'd evaluate multiple models based on your specific
> accuracy, latency, and cost requirements."

### Q: "What would you add next?"

> "Top priorities would be:
>
> 1. **ADE Integration** - Simulation setup and results analysis
> 2. **DRC/LVS Helper** - Parse violation reports, suggest fixes
> 3. **Design Migration** - Assist with PDK porting
> 4. **Learning from Usage** - Fine-tune on internal SKILL examples"

---

## Code Walkthrough Points

If asked to explain code, focus on:

### `agent.py` - The Agentic Loop

```python
while True:
    response = self.client.messages.create(...)

    tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

    if tool_use_blocks:
        # Execute tools, add results to conversation
        ...
    else:
        # Final answer
        return final_text
```

**Key insight:** The LLM controls the flow, but we control what tools are available.

### `skill_generator.py` - Structured Output

```python
# Low temperature for consistency
response = self.client.messages.create(
    temperature=0.1,
    ...
)

# Validation before returning
warnings = self._validate_skill_code(code)
```

**Key insight:** Trust but verify - always validate LLM outputs.

---

## Quick Reference Commands

```bash
# Run interactive mode
cd 02_core_agent && python agent.py

# Run demo scenarios
cd 03_demo && python demo_scenarios.py

# Run specific demo (1-5)
python demo_scenarios.py 2

# Run exercises
cd 01_fundamentals/exercises
python 01_first_api_call.py
python 02_function_calling.py
python 03_rag_basics.py
```

---

## Final Tips

1. **Start with the demo** - Show it working before explaining
2. **Emphasize tool-based approach** - This is the key innovation
3. **Connect to job requirements** - SKILL, automation, AI
4. **Be honest about limitations** - Shows maturity
5. **Show enthusiasm** - You built this to prepare!
