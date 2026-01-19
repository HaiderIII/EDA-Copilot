"""
EDA Copilot Agent

Main agent that orchestrates all tools and provides
an intelligent interface for analog circuit designers.

This is the core of your interview demo!
"""

import os
import json
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import anthropic

from tools import ALL_TOOLS, execute_tool
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation"""
    role: str
    content: str
    tool_calls: Optional[list] = None
    tool_results: Optional[list] = None


class EdaCopilot:
    """
    EDA Copilot - An AI assistant for analog circuit design.

    Features:
    - Natural language interface for CAD automation
    - SKILL code generation
    - Circuit analysis
    - Design rule queries
    - Multi-turn conversation with context

    Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │                     EDA COPILOT                         │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │   User Query ──────────────────────────────────────┐    │
    │                                                    ▼    │
    │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐│
    │   │   Claude    │───▶│    Tool     │───▶│   Tool      ││
    │   │    API      │    │  Selection  │    │  Execution  ││
    │   └─────────────┘    └─────────────┘    └─────────────┘│
    │         │                                      │        │
    │         │            ┌─────────────┐           │        │
    │         └───────────▶│  Response   │◀──────────┘        │
    │                      │ Generation  │                    │
    │                      └─────────────┘                    │
    │                            │                            │
    │                            ▼                            │
    │                      Final Answer                       │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the EDA Copilot agent.

        Args:
            model: Claude model to use
        """
        self.client = anthropic.Anthropic()
        self.model = model
        self.conversation_history: list[dict] = []
        self.system_prompt = SYSTEM_PROMPT

    def chat(self, user_message: str, verbose: bool = True) -> str:
        """
        Send a message to the agent and get a response.

        This implements the agentic loop:
        1. Send message with available tools
        2. If Claude wants to use tools, execute them
        3. Send tool results back
        4. Repeat until Claude gives final answer

        Args:
            user_message: User's input message
            verbose: Print intermediate steps

        Returns:
            Agent's final response text
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        if verbose:
            print(f"\n{'='*60}")
            print(f"USER: {user_message}")
            print('='*60)

        # Agentic loop
        while True:
            # Call Claude with tools
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=ALL_TOOLS,
                messages=self.conversation_history
            )

            # Check for tool use
            tool_use_blocks = [
                block for block in response.content
                if block.type == "tool_use"
            ]

            if tool_use_blocks:
                # Claude wants to use tools
                if verbose:
                    print(f"\n[COPILOT] Using {len(tool_use_blocks)} tool(s)...")

                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })

                # Execute each tool
                tool_results = []
                for tool_use in tool_use_blocks:
                    if verbose:
                        print(f"  → {tool_use.name}({json.dumps(tool_use.input)[:100]}...)")

                    # Execute tool
                    result = execute_tool(tool_use.name, tool_use.input)

                    if verbose:
                        # Print truncated result
                        preview = result[:200] + "..." if len(result) > 200 else result
                        print(f"    Result: {preview}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    })

                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

            else:
                # Claude gave final answer
                final_text = ""
                for block in response.content:
                    if hasattr(block, 'text'):
                        final_text += block.text

                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_text
                })

                if verbose:
                    print(f"\n[COPILOT RESPONSE]\n{final_text}")

                return final_text

            # Safety limit
            if len(self.conversation_history) > 20:
                return "Maximum conversation length reached. Please start a new conversation."

    def reset(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        turns = len([m for m in self.conversation_history if m["role"] == "user"])
        return f"Conversation with {turns} user messages"


def interactive_mode():
    """Run the agent in interactive mode"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                         EDA COPILOT                               ║
║            AI Assistant for Analog Circuit Design                 ║
╠═══════════════════════════════════════════════════════════════════╣
║  Commands:                                                        ║
║    - Type your question to get help                               ║
║    - 'reset' - Clear conversation history                         ║
║    - 'quit' or 'exit' - Exit the program                          ║
║                                                                   ║
║  Example queries:                                                 ║
║    - "What is the minimum Metal1 spacing?"                        ║
║    - "Generate SKILL code to count transistors"                   ║
║    - "Analyze this netlist: M1 out in vss vss nmos w=1u l=100n"   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    copilot = EdaCopilot()

    while True:
        try:
            user_input = input("\n[YOU] > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye! Happy designing!")
                break

            if user_input.lower() == 'reset':
                copilot.reset()
                print("\n[SYSTEM] Conversation cleared.")
                continue

            # Get response from copilot
            copilot.chat(user_input)

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] {str(e)}")


def demo_mode():
    """Run predefined demo scenarios"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                    EDA COPILOT DEMO MODE                          ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    copilot = EdaCopilot()

    demo_queries = [
        "What is the minimum width for Metal1 in ASAP7?",
        "Generate SKILL code to iterate through all instances in a schematic and print their names",
        "Search for all spacing rules in the design rule manual",
    ]

    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'#'*60}")
        print(f"# DEMO {i}/{len(demo_queries)}")
        print(f"{'#'*60}")

        copilot.chat(query)
        copilot.reset()  # Reset between demos for clarity

        input("\n[Press Enter for next demo...]")

    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_mode()
