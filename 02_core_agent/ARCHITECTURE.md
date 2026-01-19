# EDA Copilot - Architecture Explained

> This document explains how the EDA Copilot agent works step by step.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EDA COPILOT                                    │
│                                                                             │
│  ┌─────────┐      ┌─────────────┐      ┌─────────┐      ┌───────────────┐  │
│  │  USER   │ ───▶ │   AGENT     │ ───▶ │ CLAUDE  │ ───▶ │    TOOLS      │  │
│  │         │      │  (agent.py) │      │   API   │      │               │  │
│  └─────────┘      └─────────────┘      └─────────┘      └───────────────┘  │
│       ▲                                                        │           │
│       │                                                        │           │
│       └────────────────────────────────────────────────────────┘           │
│                           Final Response                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The 4 Main Components

### 1. Agent (`agent.py`)
The orchestrator that manages the entire flow.

### 2. Claude API
The "brain" that decides what to do.

### 3. Tools (`tools/`)
The concrete actions the agent can perform.

### 4. Prompts (`prompts/`)
The instructions that define Claude's behavior.

---

## The Detailed Flow

### Step 1: User asks a question

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 1                                │
│                                                              │
│   User: "What is the minimum Metal1 spacing?"                │
│                           │                                  │
│                           ▼                                  │
│              ┌─────────────────────┐                         │
│              │  conversation_      │                         │
│              │  history.append()   │                         │
│              └─────────────────────┘                         │
│                           │                                  │
│                           ▼                                  │
│   conversation_history = [                                   │
│     {"role": "user", "content": "What is the minimum..."}    │
│   ]                                                          │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~150
self.conversation_history.append({
    "role": "user",
    "content": user_message
})
```

---

### Step 2: Send to Claude with available Tools

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 2                                │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              REQUEST TO CLAUDE API                  │    │
│   ├─────────────────────────────────────────────────────┤    │
│   │                                                     │    │
│   │  model: "claude-sonnet-4-20250514"                      │    │
│   │                                                     │    │
│   │  system: "You are EDA Copilot, an AI assistant..." │    │
│   │                                                     │    │
│   │  tools: [                                           │    │
│   │    {name: "query_design_rule", ...},                │    │
│   │    {name: "generate_skill_code", ...},              │    │
│   │    {name: "analyze_circuit", ...},                  │    │
│   │  ]                                                  │    │
│   │                                                     │    │
│   │  messages: [                                        │    │
│   │    {role: "user", content: "What is the min..."}    │    │
│   │  ]                                                  │    │
│   │                                                     │    │
│   └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│                           ▼                                  │
│                    CLAUDE API                                │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~165
response = self.client.messages.create(
    model=self.model,
    max_tokens=4096,
    system=self.system_prompt,
    tools=ALL_TOOLS,           # ← Available tools
    messages=self.conversation_history
)
```

---

### Step 3: Claude decides to use a Tool

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 3                                │
│                                                              │
│   Claude analyzes the question and decides:                  │
│   "To answer about Metal1 spacing, I need to use             │
│    the query_design_rule tool"                               │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              CLAUDE'S RESPONSE                      │    │
│   ├─────────────────────────────────────────────────────┤    │
│   │                                                     │    │
│   │  content: [                                         │    │
│   │    {                                                │    │
│   │      "type": "tool_use",          ← Tool call!      │    │
│   │      "id": "toolu_abc123",                          │    │
│   │      "name": "query_design_rule",                   │    │
│   │      "input": {                                     │    │
│   │        "layer": "M1",                               │    │
│   │        "rule_type": "min_spacing"                   │    │
│   │      }                                              │    │
│   │    }                                                │    │
│   │  ]                                                  │    │
│   │                                                     │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~172
tool_use_blocks = [
    block for block in response.content
    if block.type == "tool_use"
]

if tool_use_blocks:
    # Claude wants to use a tool!
```

---

### Step 4: The Agent executes the Tool

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 4                                │
│                                                              │
│   THE AGENT (not Claude!) executes the tool                  │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │  for tool_use in tool_use_blocks:                   │    │
│   │      │                                              │    │
│   │      ▼                                              │    │
│   │  tool_name = "query_design_rule"                    │    │
│   │  tool_input = {"layer": "M1", "rule_type": "..."}   │    │
│   │      │                                              │    │
│   │      ▼                                              │    │
│   │  ┌────────────────────────────────────────────┐     │    │
│   │  │         execute_tool()                     │     │    │
│   │  │                                            │     │    │
│   │  │  → Looks up in TOOL_HANDLERS               │     │    │
│   │  │  → Finds handle_query_tool()               │     │    │
│   │  │  → Executes with the inputs                │     │    │
│   │  │                                            │     │    │
│   │  └────────────────────────────────────────────┘     │    │
│   │      │                                              │    │
│   │      ▼                                              │    │
│   │  result = {                                         │    │
│   │    "status": "success",                             │    │
│   │    "layer": "M1",                                   │    │
│   │    "rule_type": "min_spacing",                      │    │
│   │    "value": "18nm",                                 │    │
│   │    "rule_id": "M1.S.1"                              │    │
│   │  }                                                  │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~185
for tool_use in tool_use_blocks:
    result = execute_tool(tool_use.name, tool_use.input)

    tool_results.append({
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": result
    })
```

---

### Step 5: Result is sent back to Claude

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 5                                │
│                                                              │
│   The tool result is added to the history                    │
│                                                              │
│   conversation_history = [                                   │
│     {"role": "user", "content": "What is the minimum..."},   │
│     {"role": "assistant", "content": [tool_use block]},      │
│     {"role": "user", "content": [                  ← NEW     │
│       {                                                      │
│         "type": "tool_result",                               │
│         "tool_use_id": "toolu_abc123",                       │
│         "content": '{"value": "18nm", ...}'                  │
│       }                                                      │
│     ]}                                                       │
│   ]                                                          │
│                                                              │
│                           │                                  │
│                           ▼                                  │
│                                                              │
│              LOOP: Back to step 2                            │
│              (send everything to Claude again)               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~195
self.conversation_history.append({
    "role": "user",
    "content": tool_results
})
# Then the while loop continues...
```

---

### Step 6: Claude generates the final response

```
┌──────────────────────────────────────────────────────────────┐
│                        STEP 6                                │
│                                                              │
│   Claude sees the tool result and generates a response       │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐    │
│   │              CLAUDE'S FINAL RESPONSE                │    │
│   ├─────────────────────────────────────────────────────┤    │
│   │                                                     │    │
│   │  content: [                                         │    │
│   │    {                                                │    │
│   │      "type": "text",          ← No tool_use!        │    │
│   │      "text": "The minimum spacing for Metal1 is     │    │
│   │               18nm (rule M1.S.1). For different     │    │
│   │               nets, it's 21nm (rule M1.S.2)."       │    │
│   │    }                                                │    │
│   │  ]                                                  │    │
│   │                                                     │    │
│   └─────────────────────────────────────────────────────┘    │
│                                                              │
│   No tool_use → Exit the loop!                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Corresponding code:**
```python
# agent.py line ~200
else:
    # No tool_use = final response
    final_text = ""
    for block in response.content:
        if hasattr(block, 'text'):
            final_text += block.text
    return final_text
```

---

## The Complete Agentic Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENTIC LOOP                                        │
│                                                                             │
│                                                                             │
│     ┌──────────────┐                                                        │
│     │  User Query  │                                                        │
│     └──────┬───────┘                                                        │
│            │                                                                │
│            ▼                                                                │
│     ┌──────────────┐                                                        │
│     │ Add to       │                                                        │
│     │ history      │                                                        │
│     └──────┬───────┘                                                        │
│            │                                                                │
│            ▼                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         WHILE LOOP                                  │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                                                              │   │    │
│  │  │     ┌─────────────┐      ┌─────────────────────────────┐     │   │    │
│  │  │     │ Call Claude │ ───▶ │ Claude returns response     │     │   │    │
│  │  │     │ with tools  │      └─────────────┬───────────────┘     │   │    │
│  │  │     └─────────────┘                    │                     │   │    │
│  │  │                                        ▼                     │   │    │
│  │  │                              ┌─────────────────────┐         │   │    │
│  │  │                              │  Has tool_use?      │         │   │    │
│  │  │                              └─────────┬───────────┘         │   │    │
│  │  │                                        │                     │   │    │
│  │  │                          ┌─────────────┴─────────────┐       │   │    │
│  │  │                          │                           │       │   │    │
│  │  │                         YES                          NO      │   │    │
│  │  │                          │                           │       │   │    │
│  │  │                          ▼                           │       │   │    │
│  │  │               ┌─────────────────────┐                │       │   │    │
│  │  │               │  Execute tool(s)    │                │       │   │    │
│  │  │               │  Add results to     │                │       │   │    │
│  │  │               │  history            │                │       │   │    │
│  │  │               └──────────┬──────────┘                │       │   │    │
│  │  │                          │                           │       │   │    │
│  │  │                          └───── CONTINUE ────────────┘       │   │    │
│  │  │                                   │                          │   │    │
│  │  │                                   │ (NO = BREAK)             │   │    │
│  │  └───────────────────────────────────┼──────────────────────────┘   │    │
│  │                                      │                              │    │
│  └──────────────────────────────────────┼──────────────────────────────┘    │
│                                         │                                   │
│                                         ▼                                   │
│                              ┌─────────────────────┐                        │
│                              │  Return final       │                        │
│                              │  text response      │                        │
│                              └─────────────────────┘                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
02_core_agent/
│
├── agent.py                 ← The orchestrator
│   │
│   ├── class EdaCopilot
│   │   ├── __init__()       → Initialize API client + history
│   │   ├── chat()           → The main agentic loop
│   │   └── reset()          → Clear history
│   │
│   └── interactive_mode()   → CLI interface
│
├── tools/
│   │
│   ├── __init__.py          ← Registry of all tools
│   │   ├── ALL_TOOLS        → List of tool definitions
│   │   ├── TOOL_HANDLERS    → Dict {name: function}
│   │   └── execute_tool()   → Dispatch to correct handler
│   │
│   ├── skill_generator.py   ← Generates SKILL code
│   │   ├── SkillGenerator class
│   │   ├── SKILL_GENERATOR_TOOL (schema)
│   │   └── handle_tool_call()
│   │
│   ├── circuit_analyzer.py  ← Analyzes netlists
│   │   ├── CircuitAnalyzer class
│   │   ├── CIRCUIT_ANALYZER_TOOL (schema)
│   │   └── handle_tool_call()
│   │
│   └── design_rules.py      ← Query design rules
│       ├── DesignRulesDB class
│       ├── QUERY_DESIGN_RULE_TOOL (schema)
│       └── handle_query_tool()
│
└── prompts/
    └── system_prompt.py     ← Defines the agent's personality
        └── SYSTEM_PROMPT    → "You are EDA Copilot..."
```

---

## Concrete Example: Multi-Tool

When the user asks something complex:

```
User: "List transistors in myLib/amp schematic, then run DRC on its layout"
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MULTI-TOOL SCENARIO                                 │
│                                                                             │
│  Turn 1:                                                                    │
│  ────────                                                                   │
│  User: "List transistors... then run DRC..."                                │
│            │                                                                │
│            ▼                                                                │
│  Claude decides: "I need to list first, then DRC"                           │
│            │                                                                │
│            ▼                                                                │
│  Response: tool_use "list_cell_instances"                                   │
│            {library: "myLib", cell: "amp", filter: "transistor"}            │
│            │                                                                │
│            ▼                                                                │
│  Agent executes → Result: [{M1: nmos}, {M2: pmos}, ...]                     │
│                                                                             │
│  Turn 2:                                                                    │
│  ────────                                                                   │
│  Claude sees the results                                                    │
│            │                                                                │
│            ▼                                                                │
│  Response: tool_use "run_drc"                                               │
│            {library: "myLib", cell: "amp", view: "layout"}                  │
│            │                                                                │
│            ▼                                                                │
│  Agent executes → Result: {violations: 3, ...}                              │
│                                                                             │
│  Turn 3:                                                                    │
│  ────────                                                                   │
│  Claude sees all results                                                    │
│            │                                                                │
│            ▼                                                                │
│  Response: text (no tool_use)                                               │
│  "Found 4 transistors (2 NMOS, 2 PMOS). DRC found 3 violations..."          │
│                                                                             │
│  → DONE!                                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Points to Remember

### 1. Separation of Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **Claude** | Decides WHICH tool to use and with WHAT parameters |
| **Agent** | Executes the tools and manages the flow |
| **Tools** | Implement the concrete actions |

### 2. History is Crucial

```python
conversation_history = [
    {"role": "user", "content": "..."},           # Question
    {"role": "assistant", "content": [tool_use]}, # Claude wants a tool
    {"role": "user", "content": [tool_result]},   # Tool result
    {"role": "assistant", "content": "..."}       # Final response
]
```

### 3. The while loop is the heart

```python
while True:
    response = call_claude()

    if has_tool_use(response):
        execute_tools()
        continue  # ← Loop again!
    else:
        return final_answer  # ← Exit!
```

### 4. Tools are contracts

```python
{
    "name": "query_design_rule",           # Unique identifier
    "description": "...",                   # Claude reads this to decide
    "input_schema": {                       # Strict contract
        "properties": {...},
        "required": [...]
    }
}
```

---

## Quick Quiz

**Q1**: Who executes the `query_design_rule` tool?
<details>
<summary>Answer</summary>
The Agent (your Python code), NOT Claude.
</details>

**Q2**: What happens if Claude returns `tool_use`?
<details>
<summary>Answer</summary>
The loop continues (`continue`), we execute the tool and send the result back to Claude.
</details>

**Q3**: What happens if Claude returns text without `tool_use`?
<details>
<summary>Answer</summary>
We exit the loop (`break`/`return`) and return the response to the user.
</details>

**Q4**: Why does the history contain `tool_result`?
<details>
<summary>Answer</summary>
So Claude can see the tool results and generate an informed response.
</details>
