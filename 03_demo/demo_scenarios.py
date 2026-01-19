"""
Demo Scenarios for Interview

Run these scenarios to demonstrate the EDA Copilot capabilities.
Each scenario showcases different aspects of LLM integration with EDA.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_core_agent'))

from agent import EdaCopilot


def print_banner(title: str):
    """Print a formatted banner"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def scenario_1_design_rules():
    """
    Scenario 1: Design Rule Query
    Shows: Tool calling, structured data retrieval
    """
    print_banner("SCENARIO 1: Design Rule Query")

    print("""
    CONTEXT: A designer needs to know Metal1 design rules for layout.

    WHAT THIS DEMONSTRATES:
    - Natural language understanding
    - Tool selection (query_design_rule)
    - Structured response from PDK database
    """)

    copilot = EdaCopilot()

    queries = [
        "What are the Metal1 design rules I should know about?",
        "What's the minimum spacing between different nets on M1?",
    ]

    for query in queries:
        copilot.chat(query, verbose=True)

    return copilot


def scenario_2_skill_generation():
    """
    Scenario 2: SKILL Code Generation
    Shows: Code generation, prompt engineering
    """
    print_banner("SCENARIO 2: SKILL Code Generation")

    print("""
    CONTEXT: A designer wants to automate a repetitive task.

    WHAT THIS DEMONSTRATES:
    - Natural language to code translation
    - SKILL syntax generation
    - Code validation and warnings
    """)

    copilot = EdaCopilot()

    queries = [
        "Generate SKILL code to find all transistors in a schematic and report their W/L ratios",
        "Can you also add a function to calculate the total area of all transistors?",
    ]

    for query in queries:
        copilot.chat(query, verbose=True)

    return copilot


def scenario_3_circuit_analysis():
    """
    Scenario 3: Circuit Analysis
    Shows: Multi-tool workflow, analysis capabilities
    """
    print_banner("SCENARIO 3: Circuit Analysis")

    print("""
    CONTEXT: A designer wants to understand a circuit netlist.

    WHAT THIS DEMONSTRATES:
    - Netlist parsing
    - Topology detection
    - Simulation recommendations
    """)

    copilot = EdaCopilot()

    netlist = """
    * Differential OTA
    M1 out1 inp tail vss nmos w=1u l=100n
    M2 out2 inn tail vss nmos w=1u l=100n
    M3 out1 out1 vdd vdd pmos w=2u l=100n
    M4 out2 out1 vdd vdd pmos w=2u l=100n
    M5 tail bias vss vss nmos w=500n l=100n
    C1 out2 0 1p
    """

    query = f"Analyze this circuit netlist and tell me what simulations I should run:\n{netlist}"
    copilot.chat(query, verbose=True)

    return copilot


def scenario_4_multi_turn():
    """
    Scenario 4: Multi-turn Conversation
    Shows: Context retention, iterative refinement
    """
    print_banner("SCENARIO 4: Multi-turn Conversation")

    print("""
    CONTEXT: A designer has a complex request that evolves.

    WHAT THIS DEMONSTRATES:
    - Conversation context retention
    - Iterative refinement of requests
    - Building on previous responses
    """)

    copilot = EdaCopilot()

    conversation = [
        "I'm designing a current mirror in ASAP7. What spacing rules apply to the transistors?",
        "Generate SKILL code to check if two transistors in my schematic have matching W and L",
        "Modify the code to also check that they're on the same net",
    ]

    for query in conversation:
        copilot.chat(query, verbose=True)
        print("\n" + "-" * 50)

    return copilot


def scenario_5_error_handling():
    """
    Scenario 5: Error Handling
    Shows: Graceful handling of edge cases
    """
    print_banner("SCENARIO 5: Error Handling")

    print("""
    CONTEXT: Testing robustness with unusual queries.

    WHAT THIS DEMONSTRATES:
    - Handling unknown layers/rules
    - Graceful error messages
    - Helpful suggestions
    """)

    copilot = EdaCopilot()

    queries = [
        "What's the minimum width for Metal99?",  # Invalid layer
        "Generate SKILL code for quantum tunneling simulation",  # Out of scope
    ]

    for query in queries:
        copilot.chat(query, verbose=True)

    return copilot


def run_all_scenarios():
    """Run all demo scenarios"""
    scenarios = [
        ("Design Rule Query", scenario_1_design_rules),
        ("SKILL Code Generation", scenario_2_skill_generation),
        ("Circuit Analysis", scenario_3_circuit_analysis),
        ("Multi-turn Conversation", scenario_4_multi_turn),
        ("Error Handling", scenario_5_error_handling),
    ]

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                    EDA COPILOT - DEMO SCENARIOS                       ║
║                                                                       ║
║  These scenarios demonstrate LLM capabilities for EDA automation.     ║
║  Use these during your Apple interview to showcase the project.       ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)

    for i, (name, func) in enumerate(scenarios, 1):
        print(f"\n\n{'#' * 70}")
        print(f"#  SCENARIO {i}/{len(scenarios)}: {name.upper()}")
        print(f"{'#' * 70}")

        func()

        if i < len(scenarios):
            input("\n\n[Press Enter for next scenario...]")

    print("\n\n" + "=" * 70)
    print("  ALL DEMOS COMPLETE!")
    print("=" * 70)
    print("""
KEY TALKING POINTS FOR INTERVIEW:

1. ARCHITECTURE
   - Tool-based approach for reliability
   - Separation of LLM reasoning from tool execution
   - Conversation context for multi-turn interactions

2. EDA INTEGRATION
   - Simulated tools mirror real Cadence APIs
   - Easy to connect to actual Virtuoso environment
   - Design rules database could be populated from real PDK

3. SCALABILITY
   - RAG for documentation queries
   - Caching for repeated design rule lookups
   - Modular tool design for easy extension

4. PRODUCTION CONSIDERATIONS
   - Code validation before execution
   - Human-in-the-loop for critical operations
   - Logging and audit trails
    """)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        scenario_num = int(sys.argv[1])
        scenarios = [
            scenario_1_design_rules,
            scenario_2_skill_generation,
            scenario_3_circuit_analysis,
            scenario_4_multi_turn,
            scenario_5_error_handling,
        ]
        if 1 <= scenario_num <= len(scenarios):
            scenarios[scenario_num - 1]()
        else:
            print(f"Invalid scenario number. Choose 1-{len(scenarios)}")
    else:
        run_all_scenarios()
