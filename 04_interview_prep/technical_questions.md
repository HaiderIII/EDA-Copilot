# Technical Interview Questions - Apple CAD Position

## LLM/AI Questions

### Q1: "Explain how large language models work"

**Your Answer:**

> "LLMs are neural networks trained on massive text corpora to predict the
> next token in a sequence. The key architecture is the Transformer, which
> uses self-attention to weigh the relevance of different input tokens when
> generating each output.
>
> The training process involves:
> 1. Tokenization - breaking text into subwords
> 2. Embedding - converting tokens to vectors
> 3. Attention layers - learning relationships between tokens
> 4. Pre-training - predicting masked/next tokens on billions of examples
> 5. Fine-tuning - adapting to specific tasks
>
> For CAD applications, the key insight is that LLMs are excellent at pattern
> matching and can translate natural language to structured outputs like code."

### Q2: "What are the risks of using LLMs in production?"

**Your Answer:**

| Risk | Mitigation |
|------|------------|
| **Hallucination** | Tool-based approach constrains outputs; validate generated code |
| **Non-determinism** | Use temperature=0; seed parameter for reproducibility |
| **Prompt injection** | Sanitize user inputs; principle of least privilege for tools |
| **Data leakage** | On-premise deployment options; enterprise API agreements |
| **Cost** | Caching, model selection (smaller for simple tasks) |

### Q3: "How would you fine-tune an LLM for EDA tasks?"

**Your Answer:**

> "Three approaches, from simplest to most involved:
>
> 1. **Prompt Engineering** (no training)
>    - Craft system prompts with domain knowledge
>    - Include few-shot examples of good SKILL code
>    - Most practical for quick iteration
>
> 2. **RAG (Retrieval-Augmented Generation)**
>    - Index internal documentation and code examples
>    - Retrieve relevant context at query time
>    - No model modification needed
>
> 3. **Fine-tuning** (model modification)
>    - Collect examples of (prompt, ideal_response) pairs
>    - Use supervised fine-tuning on base model
>    - Requires significant data curation effort
>
> For most CAD applications, RAG + prompt engineering gives 80% of the value
> with 20% of the effort."

### Q4: "Explain function calling / tool use"

**Your Answer:**

> "Function calling allows LLMs to output structured requests to external
> tools rather than just text. Here's how it works:
>
> 1. **Define tools** with name, description, and JSON schema for parameters
> 2. **Send query** with available tools to the LLM
> 3. **LLM decides** whether to use a tool and what parameters to pass
> 4. **Execute tool** in your code (LLM doesn't run it)
> 5. **Return results** to LLM for final response
>
> For CAD, this is powerful because:
> - We define tools that map to Virtuoso APIs
> - LLM decides WHICH tool based on user intent
> - We control what actually executes
> - Outputs are constrained to valid schemas"

**Code Example:**
```python
tools = [{
    "name": "run_drc",
    "description": "Run Design Rule Check on layout",
    "input_schema": {
        "type": "object",
        "properties": {
            "cellname": {"type": "string"},
            "ruleset": {"type": "string"}
        }
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    tools=tools,
    messages=[{"role": "user", "content": "Check DRC for my amplifier"}]
)
# Claude returns: tool_use with name="run_drc", input={"cellname": "amplifier", ...}
```

---

## SKILL/Cadence Questions

### Q5: "What is SKILL and why is it important?"

**Your Answer:**

> "SKILL is Cadence's built-in Lisp-like scripting language for Virtuoso
> automation. It's important because:
>
> 1. **Deep integration** - Direct access to database, schematic, layout objects
> 2. **Full automation** - Can script entire design flows
> 3. **Customization** - Extend Virtuoso with custom menus, forms, checks
> 4. **Interoperability** - Interface with external tools and data
>
> Key patterns I know:
> - `dbOpenCellViewByType` for accessing cellviews
> - `~>` operator for property access (e.g., `cv~>instances`)
> - `foreach` for iteration
> - `let` for local variable scoping"

### Q6: "Describe the analog design flow"

**Your Answer:**

```
Specifications → Schematic → Simulation → Layout → DRC/LVS/PEX → Post-Layout Sim
        ↑                        ↓           ↓
        └────────────────────────────────────┘ (iterate until specs met)
```

> "Unlike digital design which is largely automated (synthesis, P&R), analog
> design is iterative and manual:
>
> 1. **Specifications** - Define gain, bandwidth, noise, power targets
> 2. **Schematic entry** - Draw circuit topology, size devices
> 3. **Simulation** - DC (bias), AC (frequency response), Transient, Noise
> 4. **Layout** - Manual placement/routing, parasitic-sensitive
> 5. **Verification** - DRC (design rules), LVS (layout vs schematic)
> 6. **Extraction** - PEX extracts parasitic R/L/C
> 7. **Post-layout simulation** - Verify with real parasitics
> 8. **Iterate** - Often many loops to meet specs"

### Q7: "How would you debug an LVS error?"

**Your Answer:**

> "Common LVS issues and debugging approaches:
>
> | Error | Cause | Debug Approach |
> |-------|-------|----------------|
> | Device count mismatch | Merged/missing devices | Check extraction rules, merged fingers |
> | Net short | Overlapping metals | Highlight nets in layout, check layers |
> | Net open | Missing via/connection | Trace net path, check via coverage |
> | Property mismatch | Wrong W/L | Compare extracted vs schematic values |
>
> For each, the process is:
> 1. Parse the LVS report
> 2. Identify the specific mismatch location
> 3. Cross-probe between schematic and layout
> 4. Find the root cause
> 5. Fix and re-run"

---

## Python/Programming Questions

### Q8: "How would you structure a large automation project?"

**Your Answer:**

```
project/
├── src/
│   ├── core/           # Main logic
│   ├── tools/          # Individual tools/handlers
│   ├── prompts/        # LLM prompts (separated for iteration)
│   └── utils/          # Common utilities
├── tests/              # Unit and integration tests
├── config/             # Configuration files
├── docs/               # Documentation
└── scripts/            # CLI entry points
```

> "Key principles:
> - **Separation of concerns** - Tools, prompts, core logic in different modules
> - **Configuration over hardcoding** - Environment variables, config files
> - **Testability** - Mock external services, unit test individual components
> - **Logging** - Comprehensive logging for debugging production issues"

### Q9: "How do you handle errors in production code?"

**Your Answer:**

```python
def safe_tool_execution(tool_name: str, inputs: dict) -> dict:
    """Example of defensive coding"""
    try:
        # Validate inputs first
        if not validate_schema(tool_name, inputs):
            return {"status": "error", "message": "Invalid inputs"}

        # Execute with timeout
        result = execute_with_timeout(tool_name, inputs, timeout=30)

        # Validate output
        if not validate_result(result):
            return {"status": "error", "message": "Invalid tool output"}

        return {"status": "success", "result": result}

    except TimeoutError:
        logger.error(f"Tool {tool_name} timed out")
        return {"status": "error", "message": "Operation timed out"}

    except Exception as e:
        logger.exception(f"Unexpected error in {tool_name}")
        return {"status": "error", "message": str(e)}
```

---

## System/Infrastructure Questions

### Q10: "How would you deploy this to serve multiple users?"

**Your Answer:**

```
┌──────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT ARCHITECTURE                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   Users ──────▶ Load Balancer ──────▶ API Servers           │
│                                           │                  │
│                                           ▼                  │
│                    ┌──────────────────────────────────┐      │
│                    │         Service Layer           │      │
│                    │  ┌──────┐ ┌──────┐ ┌──────┐     │      │
│                    │  │Agent │ │ RAG  │ │Cache │     │      │
│                    │  │Pool  │ │Index │ │Layer │     │      │
│                    │  └──────┘ └──────┘ └──────┘     │      │
│                    └──────────────────────────────────┘      │
│                                   │                          │
│                                   ▼                          │
│                          Claude API (external)               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

> "Key considerations:
> 1. **Stateless API servers** - Scale horizontally
> 2. **Session management** - Store conversation state externally (Redis)
> 3. **Rate limiting** - Protect API costs
> 4. **Caching** - Cache design rule queries, repeated patterns
> 5. **Monitoring** - Track latency, token usage, error rates
> 6. **Authentication** - Integrate with internal auth systems"

### Q11: "How would you integrate with real Cadence tools?"

**Your Answer:**

> "The tool architecture is designed for this. Current simulated tools would
> be replaced with real implementations:
>
> ```python
> # Current (simulated)
> def run_drc(cellname: str) -> dict:
>     return simulated_results()
>
> # Production
> def run_drc(cellname: str) -> dict:
>     # Option 1: SKILL IPC
>     skill_cmd = f'calibreDRC(\"{cellname}\")'
>     result = send_skill_command(skill_cmd)
>
>     # Option 2: Command line
>     result = subprocess.run(['calibre', '-drc', cellname])
>
>     # Option 3: REST API (if Cadence provides)
>     result = requests.post(virtuoso_api, json={...})
>
>     return parse_result(result)
> ```
>
> Key challenges:
> - **Session management** - Keep Virtuoso session open
> - **Error handling** - Parse tool-specific errors
> - **Performance** - Some operations are slow
> - **Licensing** - Respect license limits"

---

## Behavioral / Situation Questions

### Q12: "Tell me about a challenging technical problem you solved"

**Structure your answer:**

1. **Situation** - What was the context?
2. **Task** - What needed to be accomplished?
3. **Action** - What specific steps did you take?
4. **Result** - What was the outcome?

**Example answer (adapt to your experience):**

> "In my Physical-Design project, I implemented a complete RISC-V synthesis
> and place-and-route flow using open-source tools (Yosys, OpenROAD) with
> the ASAP7 PDK.
>
> The challenge was that documentation was sparse and the tools had
> compatibility issues with the PDK. I solved this by:
>
> 1. Reading source code to understand expected formats
> 2. Writing conversion scripts for technology files
> 3. Iterating on constraints to achieve timing closure
> 4. Documenting the entire flow for future reference
>
> Result: Successfully completed synthesis through routing, learning both
> digital design flow and debugging skills."

### Q13: "Why are you interested in this role?"

**Key points to hit:**

> "Three reasons:
>
> 1. **Technical alignment** - The combination of CAD automation and AI/LLM
>    is exactly what I've been learning. I can contribute immediately while
>    growing my skills in both areas.
>
> 2. **Impact** - At Apple, CAD tools directly enable chip design for products
>    used by billions. Improving designer productivity has multiplicative effect.
>
> 3. **Learning opportunity** - Working with EDA vendors, analog designers,
>    and internal teams would expose me to the full custom IC design ecosystem."

---

## Questions to Ask Them

1. "What are the biggest pain points for analog designers that you're hoping AI can address?"

2. "How does the CAD team collaborate with circuit designers? Is it more reactive (support tickets) or proactive (new tool development)?"

3. "What's the current adoption of automation vs. manual workflows in your design flow?"

4. "Are there specific EDA vendor tools you're looking to integrate AI with?"

5. "What does success look like for someone in this role after 6 months? 1 year?"
