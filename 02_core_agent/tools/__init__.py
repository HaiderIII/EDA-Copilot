"""
EDA Copilot Tools

This module exports all available tools for the agent.
"""

from .skill_generator import (
    SkillGenerator,
    SKILL_GENERATOR_TOOL,
    handle_tool_call as handle_skill_generator
)

from .circuit_analyzer import (
    CircuitAnalyzer,
    CIRCUIT_ANALYZER_TOOL,
    handle_tool_call as handle_circuit_analyzer
)

from .design_rules import (
    DesignRulesDB,
    QUERY_DESIGN_RULE_TOOL,
    SEARCH_DESIGN_RULES_TOOL,
    LIST_DESIGN_RULES_TOOL,
    handle_query_tool,
    handle_search_tool,
    handle_list_tool
)

# All available tools for the agent
ALL_TOOLS = [
    SKILL_GENERATOR_TOOL,
    CIRCUIT_ANALYZER_TOOL,
    QUERY_DESIGN_RULE_TOOL,
    SEARCH_DESIGN_RULES_TOOL,
    LIST_DESIGN_RULES_TOOL,
]

# Tool handlers mapping
TOOL_HANDLERS = {
    "generate_skill_code": handle_skill_generator,
    "analyze_circuit": handle_circuit_analyzer,
    "query_design_rule": handle_query_tool,
    "search_design_rules": handle_search_tool,
    "list_design_rules": handle_list_tool,
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool by name with the given input.

    Args:
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool

    Returns:
        JSON string with tool results
    """
    if tool_name not in TOOL_HANDLERS:
        import json
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    return TOOL_HANDLERS[tool_name](tool_input)
