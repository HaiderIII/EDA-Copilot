"""
SKILL Code Generator Tool

Generates SKILL code from natural language descriptions.
This tool demonstrates how LLMs can assist with CAD automation.
"""

import anthropic
from typing import Optional
import json

# SKILL code templates for common patterns
SKILL_TEMPLATES = {
    "iterate_instances": '''procedure({func_name}(libName cellName viewName)
    ; {description}
    let((cv results)
        cv = dbOpenCellViewByType(libName cellName viewName nil "r")
        unless(cv
            error("Could not open cellview %s/%s/%s" libName cellName viewName)
        )
        results = nil

        foreach(inst cv~>instances
            {loop_body}
        )

        dbClose(cv)
        results
    )
)''',

    "create_shapes": '''procedure({func_name}(cv layer coords)
    ; {description}
    let((shape)
        unless(cv
            error("Invalid cellview")
        )
        shape = dbCreateRect(cv layer list({x1}:{y1} {x2}:{y2}))
        when(shape
            printf("Created rectangle on layer %s\\n" layer)
        )
        shape
    )
)''',

    "simulation_setup": '''procedure({func_name}()
    ; {description}
    let((session)
        ; Set simulator
        simulator('spectre)

        ; Configure analysis
        {analysis_code}

        ; Run simulation
        run()

        printf("Simulation complete\\n")
    )
)''',
}


class SkillGenerator:
    """
    Generates SKILL code using Claude with structured prompting.
    """

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-sonnet-4-20250514"

    def generate(
        self,
        task_description: str,
        include_comments: bool = True,
        include_error_handling: bool = True
    ) -> dict:
        """
        Generate SKILL code from natural language description.

        Args:
            task_description: What the code should do
            include_comments: Add explanatory comments
            include_error_handling: Add error handling code

        Returns:
            dict with 'code', 'explanation', 'warnings'
        """

        system_prompt = """You are an expert SKILL programmer for Cadence Virtuoso.
Generate clean, production-ready SKILL code.

SKILL Syntax Rules:
- Comments start with ;
- Use procedure() to define functions
- Use let() for local variables
- Lists use '(a b c) syntax
- Property access uses ~> operator (e.g., cv~>instances)
- Coordinates use x:y syntax

Common API Functions:
- dbOpenCellViewByType(lib cell view mode access) - open cellview
- dbClose(cv) - close cellview
- dbCreateRect(cv layer bBox) - create rectangle
- dbCreatePath(cv layer points width) - create path
- foreach(var list body) - iterate
- printf(format args...) - print

Output ONLY valid SKILL code. Include comments if requested."""

        user_prompt = f"""Generate SKILL code for the following task:

TASK: {task_description}

Requirements:
- Include comments: {include_comments}
- Include error handling: {include_error_handling}
- Follow Cadence coding conventions
- Use proper indentation (2 spaces)

Return ONLY the SKILL code, nothing else."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.1,  # Low temperature for consistent code
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            code = response.content[0].text

            # Basic validation
            warnings = self._validate_skill_code(code)

            return {
                "status": "success",
                "code": code,
                "warnings": warnings,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "code": None,
                "warnings": []
            }

    def _validate_skill_code(self, code: str) -> list[str]:
        """Basic validation of generated SKILL code"""
        warnings = []

        # Check for balanced parentheses
        if code.count('(') != code.count(')'):
            warnings.append("Unbalanced parentheses detected")

        # Check for common issues
        if 'dbOpenCellView' in code and 'dbClose' not in code:
            warnings.append("Cellview opened but not closed - potential memory leak")

        if 'foreach' in code and '~>instances' not in code and '~>nets' not in code:
            warnings.append("foreach without clear iteration target")

        return warnings

    def explain_code(self, code: str) -> str:
        """Generate explanation for existing SKILL code"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Explain this SKILL code concisely:

```skill
{code}
```

Explain:
1. What the code does (1-2 sentences)
2. Key functions used
3. Any potential issues"""
            }]
        )

        return response.content[0].text


# Tool definition for agent integration
SKILL_GENERATOR_TOOL = {
    "name": "generate_skill_code",
    "description": "Generate SKILL code for Cadence Virtuoso automation from a natural language description",
    "input_schema": {
        "type": "object",
        "properties": {
            "task_description": {
                "type": "string",
                "description": "Natural language description of what the SKILL code should do"
            },
            "include_comments": {
                "type": "boolean",
                "description": "Whether to include explanatory comments in the code",
                "default": True
            },
            "include_error_handling": {
                "type": "boolean",
                "description": "Whether to include error handling code",
                "default": True
            }
        },
        "required": ["task_description"]
    }
}


def handle_tool_call(tool_input: dict) -> str:
    """Handler for agent tool calls"""
    generator = SkillGenerator()
    result = generator.generate(
        task_description=tool_input["task_description"],
        include_comments=tool_input.get("include_comments", True),
        include_error_handling=tool_input.get("include_error_handling", True)
    )
    return json.dumps(result, indent=2)


# Demo
if __name__ == "__main__":
    generator = SkillGenerator()

    test_cases = [
        "Count all NMOS and PMOS transistors in a schematic cellview",
        "Create a function to draw a rectangle with parameterized coordinates",
        "List all nets in a schematic and print their names",
    ]

    for task in test_cases:
        print(f"\n{'='*60}")
        print(f"TASK: {task}")
        print('='*60)

        result = generator.generate(task)

        if result["status"] == "success":
            print(f"\nGenerated Code:\n{result['code']}")
            if result["warnings"]:
                print(f"\nWarnings: {result['warnings']}")
        else:
            print(f"\nError: {result['error']}")
