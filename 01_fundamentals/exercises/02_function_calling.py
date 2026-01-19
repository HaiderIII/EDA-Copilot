"""
Exercise 2: Function Calling (Tool Use)
=======================================

GOAL: Learn how LLMs can call external functions/tools

This is THE most important concept for the Apple role!
Function calling allows you to:
- Constrain LLM outputs to specific schemas
- Integrate with existing EDA tools
- Build reliable automation pipelines

WHAT YOU'LL LEARN:
- How to define tools for Claude
- How to handle tool use responses
- Building an EDA tool interaction loop
"""

import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()


# =============================================================================
# STEP 1: Define EDA Tools
# =============================================================================

EDA_TOOLS = [
    {
        "name": "run_drc",
        "description": "Run Design Rule Check on a layout cellview. Returns list of violations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "library": {
                    "type": "string",
                    "description": "Library name containing the cell"
                },
                "cell": {
                    "type": "string",
                    "description": "Cell name to check"
                },
                "view": {
                    "type": "string",
                    "description": "View name (usually 'layout')",
                    "default": "layout"
                }
            },
            "required": ["library", "cell"]
        }
    },
    {
        "name": "generate_skill_code",
        "description": "Generate SKILL code for a specific automation task",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "Natural language description of what the code should do"
                },
                "include_comments": {
                    "type": "boolean",
                    "description": "Whether to include explanatory comments",
                    "default": True
                }
            },
            "required": ["task_description"]
        }
    },
    {
        "name": "query_design_rules",
        "description": "Query the design rule manual for specific rules",
        "input_schema": {
            "type": "object",
            "properties": {
                "layer": {
                    "type": "string",
                    "description": "Metal or diffusion layer (e.g., 'M1', 'M2', 'POLY')"
                },
                "rule_type": {
                    "type": "string",
                    "enum": ["min_width", "min_spacing", "min_enclosure", "min_area"],
                    "description": "Type of design rule to query"
                }
            },
            "required": ["layer", "rule_type"]
        }
    },
    {
        "name": "list_cell_instances",
        "description": "List all instances in a schematic or layout cellview",
        "input_schema": {
            "type": "object",
            "properties": {
                "library": {"type": "string"},
                "cell": {"type": "string"},
                "view": {"type": "string", "default": "schematic"},
                "filter_by_cell": {
                    "type": "string",
                    "description": "Optional: filter to show only instances of this cell type"
                }
            },
            "required": ["library", "cell"]
        }
    }
]


# =============================================================================
# STEP 2: Simulated Tool Implementations
# =============================================================================

def run_drc(library: str, cell: str, view: str = "layout") -> dict:
    """Simulated DRC run - in real life this would call Calibre/Assura"""
    # Simulated results
    return {
        "status": "completed",
        "total_violations": 3,
        "violations": [
            {"rule": "M1.W.1", "description": "Metal1 minimum width violation", "count": 2},
            {"rule": "M1.S.1", "description": "Metal1 minimum spacing violation", "count": 1}
        ],
        "runtime_seconds": 12.5
    }


def generate_skill_code(task_description: str, include_comments: bool = True) -> dict:
    """
    Simulated SKILL code generation
    In real implementation, this would call another LLM or template system
    """
    # For demo, return a template based on common patterns
    code = '''procedure(countTransistors(libName cellName)
    ; Opens schematic and counts NMOS/PMOS transistors
    let((cv count)
        cv = dbOpenCellViewByType(libName cellName "schematic")
        count = 0
        foreach(inst cv~>instances
            when(member(inst~>cellName '("nmos" "pmos" "nch" "pch"))
                count = count + 1
            )
        )
        printf("Total transistors: %d\\n" count)
        dbClose(cv)
        count
    )
)'''
    return {
        "status": "generated",
        "code": code,
        "language": "SKILL",
        "warnings": []
    }


def query_design_rules(layer: str, rule_type: str) -> dict:
    """Simulated design rule query - would normally query PDK database"""
    rules_db = {
        "M1": {"min_width": "0.028um", "min_spacing": "0.028um", "min_area": "0.00202um²"},
        "M2": {"min_width": "0.028um", "min_spacing": "0.028um", "min_area": "0.00202um²"},
        "POLY": {"min_width": "0.020um", "min_spacing": "0.054um", "min_area": "N/A"},
    }

    layer_upper = layer.upper()
    if layer_upper in rules_db:
        value = rules_db[layer_upper].get(rule_type, "Rule not found")
        return {
            "layer": layer_upper,
            "rule_type": rule_type,
            "value": value,
            "source": "ASAP7 PDK Design Rule Manual v1.0"
        }
    return {"error": f"Layer {layer} not found in rules database"}


def list_cell_instances(library: str, cell: str, view: str = "schematic", filter_by_cell: str = None) -> dict:
    """Simulated instance listing"""
    instances = [
        {"name": "M0", "cell": "nmos", "library": "analogLib"},
        {"name": "M1", "cell": "nmos", "library": "analogLib"},
        {"name": "M2", "cell": "pmos", "library": "analogLib"},
        {"name": "M3", "cell": "pmos", "library": "analogLib"},
        {"name": "R0", "cell": "resistor", "library": "analogLib"},
        {"name": "C0", "cell": "capacitor", "library": "analogLib"},
    ]

    if filter_by_cell:
        instances = [i for i in instances if i["cell"] == filter_by_cell]

    return {
        "library": library,
        "cell": cell,
        "view": view,
        "instance_count": len(instances),
        "instances": instances
    }


# Tool dispatch function
def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return JSON result"""
    tool_functions = {
        "run_drc": run_drc,
        "generate_skill_code": generate_skill_code,
        "query_design_rules": query_design_rules,
        "list_cell_instances": list_cell_instances
    }

    if tool_name in tool_functions:
        result = tool_functions[tool_name](**tool_input)
        return json.dumps(result, indent=2)
    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


# =============================================================================
# STEP 3: Agent Loop with Tool Use
# =============================================================================

def run_eda_agent(user_query: str):
    """
    Complete agent loop:
    1. Send query with available tools
    2. Check if Claude wants to use a tool
    3. Execute tool and return results
    4. Repeat until Claude gives final answer
    """
    client = anthropic.Anthropic()

    system_prompt = """You are an expert EDA CAD assistant for analog circuit design.
You have access to tools for:
- Running DRC checks
- Generating SKILL automation code
- Querying design rules
- Listing cell instances

When users ask questions, use the appropriate tools to help them.
Be concise and provide actionable information."""

    messages = [{"role": "user", "content": user_query}]

    print(f"\n{'=' * 60}")
    print(f"USER QUERY: {user_query}")
    print('=' * 60)

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            tools=EDA_TOOLS,
            messages=messages
        )

        # Check if Claude wants to use tools
        tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

        if tool_use_blocks:
            # Claude wants to use one or more tools
            print(f"\n[AGENT] Calling {len(tool_use_blocks)} tool(s)...")

            # Add Claude's response to messages
            messages.append({"role": "assistant", "content": response.content})

            # Process each tool call
            tool_results = []
            for tool_use in tool_use_blocks:
                print(f"  -> {tool_use.name}({json.dumps(tool_use.input)})")

                # Execute the tool
                result = execute_tool(tool_use.name, tool_use.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result
                })

            # Add tool results to messages
            messages.append({"role": "user", "content": tool_results})

        else:
            # Claude gave a final answer (no tool use)
            print(f"\n[AGENT] Final response:")
            for block in response.content:
                if hasattr(block, 'text'):
                    print(block.text)
            break

        # Safety: prevent infinite loops
        if len(messages) > 10:
            print("[AGENT] Maximum iterations reached")
            break

    return response


# =============================================================================
# STEP 4: Demo Scenarios
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("EXERCISE 2: FUNCTION CALLING (TOOL USE)")
    print("=" * 60)

    # Demo 1: Simple tool call
    print("\n\n" + "-" * 60)
    print("DEMO 1: Query Design Rules")
    print("-" * 60)
    run_eda_agent("What is the minimum width for Metal1 in ASAP7?")

    # Demo 2: Multiple tools
    print("\n\n" + "-" * 60)
    print("DEMO 2: Multi-step Task")
    print("-" * 60)
    run_eda_agent("List all the transistors in myLib/amplifier schematic, then run DRC on its layout")

    # Demo 3: Code generation
    print("\n\n" + "-" * 60)
    print("DEMO 3: Code Generation")
    print("-" * 60)
    run_eda_agent("Generate SKILL code to count all transistors in a schematic")

    print("\n" + "=" * 60)
    print("EXERCISE COMPLETE!")
    print("=" * 60)
    print("""
KEY TAKEAWAYS:
1. Tools are defined with JSON schemas - Claude follows them precisely
2. The agent loop handles multi-step interactions automatically
3. Tool results become part of the conversation history
4. This pattern is EXACTLY what Apple wants for CAD automation!

INTERVIEW TIP: Be ready to discuss:
- How would you validate tool outputs before execution?
- How would you handle errors from real EDA tools?
- What tools would be most valuable for analog designers?

NEXT: Run 03_rag_basics.py to learn about RAG
""")


if __name__ == "__main__":
    main()
