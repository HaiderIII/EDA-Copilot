# Quiz 2: Function Calling (Tool Use)

> **This is THE most important concept for the Apple interview!**
> Complete this quiz BEFORE running `02_function_calling.py`

---

## Part 1: Core Concept

### Q1. In function calling, who EXECUTES the tool/function?
- [ ] A) The LLM (Claude)
- [X] B) Your Python code
- [ ] C) The Anthropic API servers
- [ ] D) The tool executes itself

<details>
<summary>Answer</summary>

**B) Your Python code**

Critical distinction:
- LLM **decides** which tool to call and with what parameters
- YOUR code **executes** the tool and returns results
- LLM then **interprets** the results for the user

The LLM never runs anything - it only generates structured requests.

</details>

---

### Q2. What does the LLM return when it wants to use a tool?
- [ ] A) The actual result of running the tool
- [X] B) A `tool_use` block with tool name and input parameters
- [ ] C) Python code to execute the tool
- [ ] D) A URL to call

<details>
<summary>Answer</summary>

**B) A `tool_use` block with tool name and input parameters**

Example response from Claude:
```json
{
  "type": "tool_use",
  "name": "query_design_rule",
  "input": {"layer": "M1", "rule_type": "min_width"}
}
```

Your code must parse this and execute the actual function.

</details>

---

### Q3. Why is function calling important for EDA/CAD automation?
- [ ] A) It makes the LLM faster
- [X] B) It allows controlled integration with real tools (Virtuoso, Calibre, etc.)
- [ ] C) It reduces API costs
- [ ] D) It's required by Cadence

<details>
<summary>Answer</summary>

**B) It allows controlled integration with real tools (Virtuoso, Calibre, etc.)**

Instead of the LLM generating free-form text that might be wrong, it calls **defined tools** with **validated parameters**. You control:
- What tools exist
- What parameters are valid
- How the tool actually executes

This is how you safely connect an LLM to production CAD systems.

</details>

---

## Part 2: Tool Definition

### Q4. Look at this tool definition. What's wrong with it?

```python
{
    "name": "run_drc",
    "description": "Run DRC",
    "input_schema": {
        "type": "object",
        "properties": {
            "cell": {"type": "string"}
        }
    }
}
```

- [X] A) Missing `required` field
- [X] B) Description is too vague - LLM won't know when to use it
- [ ] C) `input_schema` format is wrong
- [ ] D) Both A and B

<details>
<summary>Answer</summary>

**D) Both A and B**

Problems:
1. No `required` field - Claude might call it without the `cell` parameter
2. "Run DRC" is too vague - should be "Run Design Rule Check on a layout cellview"

Better version:
```python
{
    "name": "run_drc",
    "description": "Run Design Rule Check on a layout cellview. Returns list of violations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "cell": {
                "type": "string",
                "description": "Cell name to check"
            },
            "ruleset": {
                "type": "string",
                "description": "DRC ruleset (e.g., 'calibre_drc')"
            }
        },
        "required": ["cell"]
    }
}
```

</details>

---

### Q5. You define 10 tools. User asks "What's the weather?". What happens?
- [ ] A) Claude picks a random tool
- [ ] B) Claude returns an error
- [X] C) Claude responds with text (no tool use) since no tool matches
- [ ] D) The API call fails

<details>
<summary>Answer</summary>

**C) Claude responds with text (no tool use) since no tool matches**

Claude only uses tools when relevant. If no tool fits the query, it responds normally. This is good - the LLM is smart about when to use tools vs. when to just answer.

</details>

---

## Part 3: The Agentic Loop

### Q6. What is the "agentic loop"?

```
User Query → LLM → ??? → ??? → Final Answer
```

- [ ] A) User → LLM → Response
- [X] B) User → LLM → Tool Call → Execute → Results → LLM → Response
- [ ] C) User → Database → LLM → Response
- [ ] D) User → LLM → LLM → LLM → Response

<details>
<summary>Answer</summary>

**B) User → LLM → Tool Call → Execute → Results → LLM → Response**

The loop:
1. User sends query
2. LLM decides to use a tool
3. Your code executes the tool
4. Results sent back to LLM
5. LLM generates final response (or calls another tool!)

This can repeat multiple times for complex queries.

</details>

---

### Q7. User asks: "Check DRC for my amplifier, then list all Metal1 violations"

How many tool calls might this require?
- [ ] A) Exactly 1
- [ ] B) Exactly 2
- [X] C) 1 or more (LLM decides)
- [ ] D) 0 - this is just text generation

<details>
<summary>Answer</summary>

**C) 1 or more (LLM decides)**

Claude might:
1. Call `run_drc(cell="amplifier")` first
2. Then call `filter_violations(layer="M1")`

Or it might do it in one call if the tool supports filtering. The LLM autonomously decides the sequence.

</details>

---

### Q8. What should your code do if Claude calls a tool that doesn't exist?

- [ ] A) Crash with an exception
- [X] B) Return an error message that Claude can understand
- [ ] C) Ignore it and continue
- [ ] D) Call a default tool instead

<details>
<summary>Answer</summary>

**B) Return an error message that Claude can understand**

```python
def execute_tool(tool_name, inputs):
    if tool_name not in AVAILABLE_TOOLS:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    # ... execute tool
```

Claude will see the error and either try a different approach or inform the user.

</details>

---

## Part 4: Safety & Validation

### Q9. Claude generates this tool call:

```json
{"name": "delete_all_files", "input": {"path": "/"}}
```

What's the security concern?

- [ ] A) None - Claude is always safe
- [X] B) LLM could be tricked into calling dangerous tools (prompt injection)
- [ ] C) The JSON format is wrong
- [ ] D) Tool names must be lowercase

<details>
<summary>Answer</summary>

**B) LLM could be tricked into calling dangerous tools (prompt injection)**

This is why:
1. Only define tools you trust
2. Validate inputs before execution
3. Use principle of least privilege
4. Consider human-in-the-loop for destructive actions

For EDA: Don't define a tool that can delete designs without confirmation!

</details>

---

### Q10. How do you prevent Claude from executing arbitrary code?

- [ ] A) Trust Claude - it's safe
- [X] B) Define only specific, limited tools with validated inputs
- [ ] C) Use a firewall
- [ ] D) Disable function calling

<details>
<summary>Answer</summary>

**B) Define only specific, limited tools with validated inputs**

You control the "surface area" of what Claude can do:
- Only create tools for safe operations
- Validate all inputs against expected schemas
- Add confirmation steps for destructive operations

Claude can ONLY call tools YOU define. No tools defined = no tool calls possible.

</details>

---

## Part 5: EDA Application

### Q11. You're building an EDA assistant. Which tools would you define?

Select all that apply:
- [X] A) `query_design_rule` - lookup PDK rules
- [ ] B) `run_arbitrary_skill` - execute any SKILL code
- [X] C) `run_drc` - run design rule check
- [X] D) `generate_skill_code` - create SKILL from description

<details>
<summary>Answer</summary>

**A, C, D** - NOT B

- A) ✅ Safe - read-only query
- B) ❌ DANGEROUS - arbitrary code execution
- C) ✅ Safe - bounded operation
- D) ✅ Safe - generates code for review (doesn't execute)

Never create a tool that executes arbitrary code from LLM output without validation!

</details>

---

### Q12. A designer says: "Generate SKILL code and run it immediately"

What's your response as a CAD engineer?

- [ ] A) "Sure, I'll add a tool for that"
- [X] B) "I'll generate the code, but you should review before running"
- [ ] C) "LLMs can't generate code"
- [ ] D) "That requires a different API"

<details>
<summary>Answer</summary>

**B) "I'll generate the code, but you should review before running"**

Best practice for production:
1. Generate code ✅
2. Display to user for review ✅
3. User confirms ✅
4. Then execute ✅

This is "human-in-the-loop" - critical for any automation that modifies designs.

</details>

---

## Part 6: Interview Scenarios

### Q13. Interviewer asks: "How does function calling improve reliability over free-form text?"

Best answer:

- [ ] A) "It's faster"
- [X] B) "Outputs are constrained to defined schemas - the LLM can't hallucinate arbitrary actions"
- [ ] C) "It uses less tokens"
- [ ] D) "It's more secure because of encryption"

<details>
<summary>Answer</summary>

**B) "Outputs are constrained to defined schemas - the LLM can't hallucinate arbitrary actions"**

Key points for interview:
- Free-form text can contain anything (including errors)
- Tool calls must match your defined schemas
- Invalid parameters get rejected
- You control what operations are possible

</details>

---

### Q14. Interviewer asks: "What if the LLM calls the wrong tool?"

Best answer:

- [ ] A) "That never happens"
- [X] B) "The tool validates inputs and returns an error, LLM can try again"
- [ ] C) "We restart the conversation"
- [ ] D) "We need to retrain the model"

<details>
<summary>Answer</summary>

**B) "The tool validates inputs and returns an error, LLM can try again"**

The agentic loop handles this naturally:
1. LLM calls wrong tool
2. Tool returns error message
3. LLM sees error, tries different approach
4. Repeat until success or give up

This self-correction is a key feature of agentic systems.

</details>

---

## Score Yourself

| Score | Level |
|-------|-------|
| 14/14 | Expert - You understand agents! |
| 11-13 | Strong - Review missed questions |
| 8-10 | Good foundation - Re-read explanations |
| <8 | Need more study - This is critical for interview |

---

## Now Run the Code!

```bash
cd ~/projects/eda-copilot
source venv/bin/activate
```

Watch closely:
1. How tools are defined
2. When Claude decides to use them
3. How results flow back to Claude
4. The multi-step agentic loop in action
