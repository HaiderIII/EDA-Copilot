# EDA Copilot - Project Deep Dive

This document explains every architectural decision in the project.
Use this to prepare for detailed technical questions.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          EDA COPILOT                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                                   │
│  │   User       │                                                   │
│  │   Query      │                                                   │
│  └──────┬───────┘                                                   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     AGENT LAYER                              │   │
│  │  ┌────────────┐  ┌─────────────┐  ┌────────────────────┐     │   │
│  │  │ System     │  │ Conversation│  │ Agentic Loop       │     │   │
│  │  │ Prompt     │  │ History     │  │ (tool orchestration│     │   │
│  │  └────────────┘  └─────────────┘  └────────────────────┘     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     CLAUDE API                               │   │
│  │  • Model: claude-sonnet-4-20250514                                │   │
│  │  • Temperature: 0.1 (for code) / 0.7 (for explanations)      │   │
│  │  • Tools: Defined schemas for each capability                │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼ (tool_use response)                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     TOOLS LAYER                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │   │
│  │  │ SKILL        │  │ Circuit      │  │ Design       │        │   │
│  │  │ Generator    │  │ Analyzer     │  │ Rules DB     │        │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │   │
│  │  ┌──────────────┐                                            │   │
│  │  │ RAG Query    │                                            │   │
│  │  │ (future)     │                                            │   │
│  │  └──────────────┘                                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     DATA LAYER                               │   │
│  │  • Design Rules Database (in-memory, simulated)              │   │
│  │  • Vector Store for RAG (future: ChromaDB)                   │   │
│  │  • Netlist Parser                                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Agent Layer (`agent.py`)

**Purpose:** Orchestrate the conversation and tool execution loop.

**Key Design Decisions:**

```python
class EdaCopilot:
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.conversation_history: list[dict] = []
        self.system_prompt = SYSTEM_PROMPT
```

**Why these choices?**

| Decision | Reasoning |
|----------|-----------|
| Sonnet model | Best balance of capability/cost for code generation |
| Conversation history list | Simple, allows full context for multi-turn |
| System prompt separate | Easy to iterate without code changes |

**The Agentic Loop:**

```python
while True:
    response = self.client.messages.create(...)

    if has_tool_use(response):
        execute_tools()
        add_results_to_history()
        continue  # Let Claude respond to results
    else:
        return final_answer
```

**Why a loop?**
- Claude may need multiple tool calls to answer
- Each tool result informs the next decision
- Allows complex multi-step reasoning

---

### 2. SKILL Generator (`tools/skill_generator.py`)

**Purpose:** Generate valid SKILL code from natural language.

**Key Design Decisions:**

```python
response = self.client.messages.create(
    model=self.model,
    max_tokens=2048,
    temperature=0.1,  # Low temperature for code
    system=system_prompt,
    messages=[{"role": "user", "content": user_prompt}]
)
```

**Why low temperature?**
- Code needs to be deterministic
- High temperature = creative variations = bugs
- 0.1 allows slight variation while staying consistent

**Validation:**

```python
def _validate_skill_code(self, code: str) -> list[str]:
    warnings = []
    if code.count('(') != code.count(')'):
        warnings.append("Unbalanced parentheses")
    if 'dbOpenCellView' in code and 'dbClose' not in code:
        warnings.append("Cellview not closed")
    return warnings
```

**Why basic validation?**
- Catches obvious errors before execution
- Full parsing would require SKILL interpreter
- Provides user with actionable warnings

---

### 3. Circuit Analyzer (`tools/circuit_analyzer.py`)

**Purpose:** Extract insights from SPICE netlists.

**Design Pattern:**

```python
@dataclass
class Device:
    name: str
    device_type: str
    terminals: list[str]
    parameters: dict

@dataclass
class CircuitAnalysis:
    device_count: dict
    topology_hints: list[str]
    potential_issues: list[str]
    recommended_simulations: list[str]
```

**Why dataclasses?**
- Clean, typed data structures
- Easy serialization to JSON for tool responses
- Self-documenting code

**Topology Detection:**

```python
def _detect_topologies(self, devices, counts):
    hints = []
    if counts.get("nmos", 0) >= 2:
        hints.append("Possible differential pair")
    # ...
```

**Why heuristics?**
- Exact topology detection requires full simulation
- Heuristics give useful hints quickly
- Good enough for guiding simulation recommendations

---

### 4. Design Rules Database (`tools/design_rules.py`)

**Purpose:** Provide structured access to PDK design rules.

**Data Structure:**

```python
DESIGN_RULES = {
    "M1": {
        "layer_name": "Metal1",
        "rules": {
            "min_width": {
                "value": "18nm",
                "rule_id": "M1.W.1",
                "description": "..."
            }
        }
    }
}
```

**Why this structure?**
- Mirrors how design rules are organized in DRMs
- Easy to query by layer + rule type
- Includes metadata (rule_id, description) for context

**Production Path:**
```python
# Current: Hardcoded dictionary
DESIGN_RULES = {...}

# Future: Load from files
DESIGN_RULES = load_from_pdk("/path/to/asap7/tech/design_rules.json")

# Or: Query database
DESIGN_RULES = query_pdk_database("asap7", "v1.0")
```

---

### 5. Tool Definitions

**Example Tool Schema:**

```python
SKILL_GENERATOR_TOOL = {
    "name": "generate_skill_code",
    "description": "Generate SKILL code for Cadence Virtuoso automation",
    "input_schema": {
        "type": "object",
        "properties": {
            "task_description": {
                "type": "string",
                "description": "What the code should do"
            },
            "include_comments": {
                "type": "boolean",
                "default": True
            }
        },
        "required": ["task_description"]
    }
}
```

**Why JSON Schema?**
- Claude API requires this format
- Self-documenting parameter types
- Enables validation of LLM outputs

**Description Matters:**
- LLM uses description to decide when to use tool
- Be specific: "Generate SKILL code" vs "Generate code"
- Include context: "for Cadence Virtuoso automation"

---

### 6. System Prompt Design

```python
SYSTEM_PROMPT = """You are EDA Copilot, an AI assistant for analog designers.

## Your Expertise
- Cadence Virtuoso schematic and layout design
- SKILL programming for automation
...

## Tool Usage
Use tools proactively. Always explain what you're doing.
"""
```

**Prompt Engineering Principles:**

| Principle | Application |
|-----------|-------------|
| Define persona | "EDA Copilot for analog designers" |
| List capabilities | Explicit list of what agent can do |
| Set communication style | "Be concise and actionable" |
| Guide tool usage | "Use tools proactively" |

---

## Data Flow Example

**User Query:** "What's the minimum Metal1 spacing?"

```
1. USER INPUT
   "What's the minimum Metal1 spacing?"
         │
         ▼
2. AGENT receives, adds to history
   conversation_history.append({"role": "user", "content": "..."})
         │
         ▼
3. CLAUDE API called with tools
   response = client.messages.create(
       tools=[QUERY_DESIGN_RULE_TOOL, ...],
       messages=conversation_history
   )
         │
         ▼
4. CLAUDE returns tool_use
   {
     "type": "tool_use",
     "name": "query_design_rule",
     "input": {"layer": "M1", "rule_type": "min_spacing"}
   }
         │
         ▼
5. AGENT executes tool
   result = execute_tool("query_design_rule", {...})
   # Returns: {"value": "18nm", "rule_id": "M1.S.1", ...}
         │
         ▼
6. AGENT adds result to history
   conversation_history.append({"role": "user", "content": [tool_result]})
         │
         ▼
7. CLAUDE API called again
   # Claude now sees the tool result
         │
         ▼
8. CLAUDE returns final text
   "The minimum spacing for Metal1 is 18nm (rule M1.S.1)."
         │
         ▼
9. AGENT returns to user
```

---

## Extension Points

### Adding a New Tool

1. **Define the tool schema:**
```python
NEW_TOOL = {
    "name": "new_tool_name",
    "description": "What this tool does",
    "input_schema": {...}
}
```

2. **Implement the handler:**
```python
def handle_new_tool(input: dict) -> str:
    # Execute logic
    return json.dumps(result)
```

3. **Register in `__init__.py`:**
```python
ALL_TOOLS.append(NEW_TOOL)
TOOL_HANDLERS["new_tool_name"] = handle_new_tool
```

### Connecting to Real Virtuoso

```python
# Replace simulated handler with real implementation
def handle_run_drc_real(input: dict) -> str:
    # Send SKILL command via IPC
    skill_cmd = f'calibreDRC("{input["cellname"]}")'
    result = virtuoso_ipc.send(skill_cmd)
    return json.dumps(parse_drc_result(result))
```

### Adding RAG for Documentation

```python
from chromadb import Client

# Build index
client = Client()
collection = client.create_collection("pdk_docs")

# Add documents (chunked PDK manual)
for chunk in chunk_pdk_manual("asap7_drm.pdf"):
    collection.add(
        documents=[chunk.text],
        metadatas=[{"source": chunk.source}],
        ids=[chunk.id]
    )

# Query at runtime
def query_documentation(query: str) -> list[str]:
    results = collection.query(query_texts=[query], n_results=3)
    return results["documents"]
```

---

## Testing Strategy

### Unit Tests

```python
def test_skill_generator_produces_valid_code():
    generator = SkillGenerator()
    result = generator.generate("Count transistors in schematic")

    assert result["status"] == "success"
    assert "procedure" in result["code"]
    assert result["code"].count('(') == result["code"].count(')')

def test_design_rules_returns_valid_data():
    db = DesignRulesDB()
    result = db.query_rule("M1", "min_width")

    assert result["status"] == "success"
    assert result["value"] == "18nm"
```

### Integration Tests

```python
def test_agent_can_answer_design_rule_question():
    copilot = EdaCopilot()
    response = copilot.chat("What is M1 minimum width?")

    assert "18nm" in response
    assert "M1" in response
```

### Manual Testing

```bash
# Run demo scenarios
python 03_demo/demo_scenarios.py

# Interactive testing
python 02_core_agent/agent.py
```

---

## Performance Considerations

| Aspect | Current | Production |
|--------|---------|------------|
| LLM calls | Sequential | Could parallelize independent tool calls |
| Design rules | In-memory dict | Redis cache / database |
| Code generation | Per-request | Cache common patterns |
| Conversation | In-memory | Persist to database |

---

## Security Considerations

1. **API Key Management**
   - Never commit `.env` file
   - Use environment variables in production

2. **Code Execution**
   - Generated SKILL runs in Virtuoso sandbox
   - Validate before execution
   - Log all generated code

3. **Input Sanitization**
   - Tool inputs validated against schema
   - No direct shell execution from user input

4. **Data Privacy**
   - Design data stays local
   - Only send queries to Claude API
   - Consider on-premise LLM for sensitive data
