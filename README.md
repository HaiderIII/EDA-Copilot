# EDA Copilot

An LLM-powered assistant for analog and RF circuit designers. Built to demonstrate AI integration with Cadence Virtuoso workflows.

## Project Structure

```
eda-copilot/
├── 01_fundamentals/          # Learning materials
│   ├── llm_basics.md         # LLM concepts (must read)
│   ├── eda_concepts.md       # Cadence/SKILL basics
│   └── exercises/            # Hands-on exercises
│       ├── 01_first_api_call.py
│       ├── 02_function_calling.py
│       └── 03_rag_basics.py
│
├── 02_core_agent/            # Main application
│   ├── agent.py              # Core agent with tool orchestration
│   ├── tools/                # EDA tools
│   │   ├── skill_generator.py
│   │   ├── circuit_analyzer.py
│   │   └── design_rules.py
│   └── prompts/              # System prompts
│
├── 03_demo/                  # Interview demos
│   ├── demo_scenarios.py     # Pre-built demo flows
│   └── presentation_guide.md # How to present
│
└── 04_interview_prep/        # Q&A preparation
    ├── technical_questions.md
    └── project_deep_dive.md
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the agent
cd 02_core_agent
python agent.py

# Or run demo scenarios
cd 03_demo
python demo_scenarios.py
```

## Features

### 1. SKILL Code Generation
Generate Cadence SKILL code from natural language descriptions.

```
> Generate code to count transistors in a schematic

[COPILOT] Generated SKILL code:
procedure(countTransistors(libName cellName)
    let((cv count)
        cv = dbOpenCellViewByType(libName cellName "schematic" nil "r")
        count = 0
        foreach(inst cv~>instances
            when(member(inst~>cellName '("nmos" "pmos"))
                count = count + 1
            )
        )
        dbClose(cv)
        count
    )
)
```

### 2. Design Rule Queries
Query PDK design rules using natural language.

```
> What's the minimum Metal1 spacing?

[COPILOT] The minimum spacing for Metal1 is 18nm (rule M1.S.1).
For different nets, the minimum spacing is 21nm (rule M1.S.2).
```

### 3. Circuit Analysis
Analyze SPICE netlists and get topology insights.

```
> Analyze this circuit: M1 out in vss vss nmos w=1u l=100n

[COPILOT] Analysis:
- Device count: 1 NMOS
- Topology hints: Single transistor stage
- Recommended simulations: DC operating point, AC analysis
```

## Learning Path

1. **Day 1-2**: Read `01_fundamentals/llm_basics.md` and `eda_concepts.md`
2. **Day 3-4**: Complete exercises in `01_fundamentals/exercises/`
3. **Day 5-7**: Study `02_core_agent/` code and run demos
4. **Day 8-10**: Review `04_interview_prep/` materials
5. **Day 11-14**: Practice demo and Q&A

## Key Concepts

### Function Calling (Tool Use)
The core innovation enabling reliable LLM-CAD integration:

```python
tools = [{
    "name": "generate_skill_code",
    "description": "Generate SKILL code for Virtuoso automation",
    "input_schema": {...}
}]

# LLM decides which tool to use based on user intent
# We control what tools are available
# Outputs constrained to valid schemas
```

### Agentic Loop
Multi-step reasoning with tool execution:

```
User Query → LLM → Tool Selection → Tool Execution → Results → LLM → Final Answer
                        ↑                                        ↓
                        └────────────────────────────────────────┘
```

## Interview Demo

```bash
# Run all demos
cd 03_demo && python demo_scenarios.py

# Run specific scenario (1-5)
python demo_scenarios.py 2
```

## Technologies

- **LLM**: Claude API (Anthropic)
- **Language**: Python 3.10+
- **Key Libraries**: anthropic, chromadb (optional for RAG)

## Production Considerations

| Aspect | Demo | Production |
|--------|------|------------|
| Design Rules | Hardcoded | Parse from PDK |
| SKILL Execution | Simulated | Virtuoso IPC |
| Documentation | Sample | RAG on real docs |
| Authentication | None | SSO integration |

## License

Educational project for interview preparation.
