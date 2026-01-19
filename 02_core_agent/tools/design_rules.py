"""
Design Rules Query Tool

Provides access to PDK design rules.
Demonstrates RAG-like retrieval for EDA documentation.
"""

import json
from typing import Optional


# Simulated ASAP7 Design Rules Database
# In production, this would be loaded from PDK files or parsed from DRM PDFs
DESIGN_RULES = {
    "M1": {
        "layer_name": "Metal1",
        "description": "First metal layer, typically used for local routing",
        "rules": {
            "min_width": {
                "value": "18nm",
                "rule_id": "M1.W.1",
                "description": "Minimum width for Metal1 shapes"
            },
            "min_spacing": {
                "value": "18nm",
                "rule_id": "M1.S.1",
                "description": "Minimum spacing between Metal1 shapes (same net)"
            },
            "min_spacing_diffnet": {
                "value": "21nm",
                "rule_id": "M1.S.2",
                "description": "Minimum spacing between Metal1 shapes (different nets)"
            },
            "min_area": {
                "value": "0.00202um²",
                "rule_id": "M1.A.1",
                "description": "Minimum area for Metal1 shapes"
            },
            "min_enclosure_v0": {
                "value": "5nm/1nm",
                "rule_id": "M1.E.1",
                "description": "Minimum enclosure of Via0 by Metal1 (5nm on two sides, 1nm on others)"
            }
        }
    },
    "M2": {
        "layer_name": "Metal2",
        "description": "Second metal layer, preferred horizontal routing",
        "rules": {
            "min_width": {
                "value": "18nm",
                "rule_id": "M2.W.1",
                "description": "Minimum width for Metal2 shapes"
            },
            "min_spacing": {
                "value": "18nm",
                "rule_id": "M2.S.1",
                "description": "Minimum spacing between Metal2 shapes"
            },
            "min_enclosure_v1": {
                "value": "5nm/1nm",
                "rule_id": "M2.E.1",
                "description": "Minimum enclosure of Via1 by Metal2"
            }
        }
    },
    "M3": {
        "layer_name": "Metal3",
        "description": "Third metal layer, preferred vertical routing",
        "rules": {
            "min_width": {
                "value": "18nm",
                "rule_id": "M3.W.1",
                "description": "Minimum width for Metal3 shapes"
            },
            "min_spacing": {
                "value": "18nm",
                "rule_id": "M3.S.1",
                "description": "Minimum spacing between Metal3 shapes"
            }
        }
    },
    "POLY": {
        "layer_name": "Polysilicon",
        "description": "Gate layer for transistors",
        "rules": {
            "min_width": {
                "value": "20nm",
                "rule_id": "PO.W.1",
                "description": "Minimum poly width (gate length)"
            },
            "min_spacing": {
                "value": "54nm",
                "rule_id": "PO.S.1",
                "description": "Minimum spacing between poly shapes"
            },
            "min_extension": {
                "value": "10nm",
                "rule_id": "PO.EX.1",
                "description": "Minimum poly extension beyond active"
            }
        }
    },
    "ACTIVE": {
        "layer_name": "Active/Diffusion",
        "description": "Source/drain regions for transistors",
        "rules": {
            "min_width": {
                "value": "27nm",
                "rule_id": "ACT.W.1",
                "description": "Minimum active width"
            },
            "min_spacing": {
                "value": "27nm",
                "rule_id": "ACT.S.1",
                "description": "Minimum spacing between active regions"
            }
        }
    },
    "V0": {
        "layer_name": "Via0",
        "description": "Via between Metal1 and lower layers",
        "rules": {
            "size": {
                "value": "18nm x 18nm",
                "rule_id": "V0.SZ.1",
                "description": "Via0 size"
            },
            "min_spacing": {
                "value": "20nm",
                "rule_id": "V0.S.1",
                "description": "Minimum spacing between Via0 cuts"
            }
        }
    }
}


class DesignRulesDB:
    """
    Database for PDK design rules.
    Provides query interface for the agent.
    """

    def __init__(self):
        self.rules = DESIGN_RULES

    def get_layer_info(self, layer: str) -> Optional[dict]:
        """Get all information for a specific layer"""
        layer_upper = layer.upper()
        if layer_upper in self.rules:
            return self.rules[layer_upper]
        return None

    def query_rule(self, layer: str, rule_type: str) -> dict:
        """
        Query a specific design rule.

        Args:
            layer: Layer name (M1, M2, POLY, etc.)
            rule_type: Type of rule (min_width, min_spacing, etc.)

        Returns:
            dict with rule information or error
        """
        layer_upper = layer.upper()

        if layer_upper not in self.rules:
            return {
                "status": "error",
                "error": f"Unknown layer: {layer}",
                "available_layers": list(self.rules.keys())
            }

        layer_info = self.rules[layer_upper]

        if rule_type not in layer_info["rules"]:
            return {
                "status": "error",
                "error": f"Unknown rule type '{rule_type}' for layer {layer}",
                "available_rules": list(layer_info["rules"].keys())
            }

        rule = layer_info["rules"][rule_type]
        return {
            "status": "success",
            "layer": layer_upper,
            "layer_name": layer_info["layer_name"],
            "rule_type": rule_type,
            "rule_id": rule["rule_id"],
            "value": rule["value"],
            "description": rule["description"],
            "source": "ASAP7 PDK Design Rule Manual"
        }

    def search_rules(self, query: str) -> list[dict]:
        """
        Search for rules matching a query string.
        Simple keyword matching for demonstration.
        """
        results = []
        query_lower = query.lower()

        for layer_name, layer_info in self.rules.items():
            for rule_type, rule in layer_info["rules"].items():
                # Check if query matches rule description or type
                if (query_lower in rule["description"].lower() or
                    query_lower in rule_type.lower() or
                    query_lower in layer_name.lower()):

                    results.append({
                        "layer": layer_name,
                        "rule_type": rule_type,
                        "rule_id": rule["rule_id"],
                        "value": rule["value"],
                        "description": rule["description"]
                    })

        return results

    def list_all_rules(self) -> dict:
        """List all available layers and their rules"""
        summary = {}
        for layer_name, layer_info in self.rules.items():
            summary[layer_name] = {
                "description": layer_info["description"],
                "rules": list(layer_info["rules"].keys())
            }
        return summary


# Tool definitions for agent integration
QUERY_DESIGN_RULE_TOOL = {
    "name": "query_design_rule",
    "description": "Query a specific design rule from the PDK. Returns the rule value and description.",
    "input_schema": {
        "type": "object",
        "properties": {
            "layer": {
                "type": "string",
                "description": "Layer name (e.g., M1, M2, POLY, ACTIVE, V0)"
            },
            "rule_type": {
                "type": "string",
                "description": "Type of rule (e.g., min_width, min_spacing, min_area, min_enclosure)"
            }
        },
        "required": ["layer", "rule_type"]
    }
}

SEARCH_DESIGN_RULES_TOOL = {
    "name": "search_design_rules",
    "description": "Search for design rules matching a keyword or phrase",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (e.g., 'spacing', 'metal width', 'via enclosure')"
            }
        },
        "required": ["query"]
    }
}

LIST_DESIGN_RULES_TOOL = {
    "name": "list_design_rules",
    "description": "List all available layers and their design rules",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}


def handle_query_tool(tool_input: dict) -> str:
    """Handler for query_design_rule tool"""
    db = DesignRulesDB()
    result = db.query_rule(tool_input["layer"], tool_input["rule_type"])
    return json.dumps(result, indent=2)


def handle_search_tool(tool_input: dict) -> str:
    """Handler for search_design_rules tool"""
    db = DesignRulesDB()
    results = db.search_rules(tool_input["query"])
    return json.dumps({"results": results, "count": len(results)}, indent=2)


def handle_list_tool(tool_input: dict) -> str:
    """Handler for list_design_rules tool"""
    db = DesignRulesDB()
    summary = db.list_all_rules()
    return json.dumps(summary, indent=2)


# Demo
if __name__ == "__main__":
    db = DesignRulesDB()

    print("=" * 60)
    print("DESIGN RULES DATABASE DEMO")
    print("=" * 60)

    # Query specific rule
    print("\n1. Query M1 minimum width:")
    result = db.query_rule("M1", "min_width")
    print(json.dumps(result, indent=2))

    # Search rules
    print("\n2. Search for 'spacing' rules:")
    results = db.search_rules("spacing")
    for r in results:
        print(f"  {r['layer']}.{r['rule_type']}: {r['value']}")

    # List all
    print("\n3. Available layers:")
    summary = db.list_all_rules()
    for layer, info in summary.items():
        print(f"  {layer}: {info['description']}")
