"""
Exercise 1: Your First Claude API Call
======================================

GOAL: Understand the basic structure of Claude API calls

BEFORE RUNNING:
1. pip install anthropic python-dotenv
2. Create .env file with your ANTHROPIC_API_KEY
3. Run: python 01_first_api_call.py

WHAT YOU'LL LEARN:
- How to structure API calls
- Role of system prompts
- Response parsing
"""

import os
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

def basic_call():
    """
    Most basic API call - just a user message
    """
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        messages=[
            {"role": "user", "content": "What is SKILL in the context of Cadence EDA tools?"}
        ]
    )

    print("=" * 60)
    print("BASIC CALL (no system prompt)")
    print("=" * 60)
    print(response.content[0].text)
    print()

    # IMPORTANT: Notice these response attributes
    print(f"Tokens used - Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")
    print(f"Stop reason: {response.stop_reason}")


def call_with_system_prompt():
    """
    API call with a system prompt - much better for specialized tasks
    """
    client = anthropic.Anthropic()

    # The system prompt shapes the assistant's persona and expertise
    system_prompt = """You are an expert Cadence CAD engineer with 15 years of experience.
You specialize in SKILL programming for Virtuoso automation.
When explaining concepts:
- Be concise and practical
- Include code examples when relevant
- Focus on real-world applications"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system=system_prompt,
        messages=[
            {"role": "user", "content": "What is SKILL in the context of Cadence EDA tools?"}
        ]
    )

    print("=" * 60)
    print("WITH SYSTEM PROMPT (expert persona)")
    print("=" * 60)
    print(response.content[0].text)
    print()


def multi_turn_conversation():
    """
    Demonstrate conversation history - essential for agents
    """
    client = anthropic.Anthropic()

    # Conversation history is passed as a list of messages
    messages = [
        {"role": "user", "content": "I want to write a SKILL function to count transistors in a schematic."},
        {"role": "assistant", "content": "I can help with that. To count transistors in a schematic, you'll need to:\n1. Open the cellview\n2. Iterate over instances\n3. Check if each instance is a transistor (nmos/pmos)\n\nWould you like me to write the complete function?"},
        {"role": "user", "content": "Yes, please write the complete function."}
    ]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a Cadence SKILL programming expert. Write clean, well-commented code.",
        messages=messages
    )

    print("=" * 60)
    print("MULTI-TURN CONVERSATION")
    print("=" * 60)
    print(response.content[0].text)
    print()


def temperature_comparison():
    """
    Compare different temperature settings
    Low temp = deterministic (good for code)
    High temp = creative (good for brainstorming)
    """
    client = anthropic.Anthropic()

    prompt = "Write a one-line SKILL function to calculate area from width and height."

    print("=" * 60)
    print("TEMPERATURE COMPARISON")
    print("=" * 60)

    for temp in [0.0, 0.5, 1.0]:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            temperature=temp,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"\nTemperature {temp}:")
        print(response.content[0].text.strip())

    print()
    print("INSIGHT: For code generation, use low temperature (0.0-0.3) for consistency")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EXERCISE 1: FIRST API CALLS")
    print("=" * 60 + "\n")

    # Run each example
    basic_call()
    call_with_system_prompt()
    multi_turn_conversation()
    temperature_comparison()

    print("\n" + "=" * 60)
    print("EXERCISE COMPLETE!")
    print("=" * 60)
    print("""
KEY TAKEAWAYS:
1. System prompts shape the assistant's expertise - crucial for EDA applications
2. Conversation history enables multi-turn interactions - essential for agents
3. Temperature controls randomness - use low values for code generation
4. Always check token usage - important for cost management

NEXT: Run 02_function_calling.py to learn about tool use
""")
