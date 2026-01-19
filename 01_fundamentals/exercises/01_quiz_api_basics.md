# Quiz 1: API Basics - First API Call

> Complete this quiz BEFORE running `01_first_api_call.py`
> Then run the code to verify your answers

---

## Part 1: Conceptual Understanding

### Q1. What does an LLM actually do?
- [ ] A) Executes code and returns results
- [X] B) Predicts the most likely next tokens based on input
- [ ] C) Searches a database for answers
- [ ] D) Runs simulations

<details>
<summary>Answer</summary>

**B) Predicts the most likely next tokens based on input**

LLMs are trained to predict "what text comes next". They don't execute anything - they generate text that *looks like* what should follow your prompt.

</details>

---

### Q2. What is a "token" in LLM context?
- [ ] A) A security key for API access
- [X] B) A unit of text (word or subword) the model processes
- [ ] C) A type of neural network layer
- [ ] D) A billing unit

<details>
<summary>Answer</summary>

**B) A unit of text (word or subword) the model processes**

Tokens are chunks of text. "Hello world" = 2 tokens. "Transistor" = 1-2 tokens. Longer text = more tokens = higher cost.

</details>

---

### Q3. What is the "context window"?
- [ ] A) The GUI window of the application
- [X] B) Maximum tokens the model can process in one request
- [ ] C) The time window for API rate limiting
- [ ] D) A debugging feature

<details>
<summary>Answer</summary>

**B) Maximum tokens the model can process in one request**

Claude Sonnet has ~200K tokens context. This limits how much code/documentation you can include in a single prompt.

</details>

---

## Part 2: System Prompts

### Q4. What is the purpose of a system prompt?
- [ ] A) To authenticate the API request
- [X] B) To define the assistant's persona, expertise, and behavior
- [ ] C) To set the output language (Python, SKILL, etc.)
- [ ] D) To enable streaming responses

<details>
<summary>Answer</summary>

**B) To define the assistant's persona, expertise, and behavior**

Example: "You are an expert Cadence CAD engineer" makes the LLM respond with domain expertise.

</details>

---

### Q5. Which system prompt would produce better SKILL code?

**Option A:**
```
You are a helpful assistant.
```

**Option B:**
```
You are an expert Cadence SKILL programmer with 10 years of experience.
You write clean, well-commented code following Cadence conventions.
Always include error handling.
```

- [ ] A) Option A
- [X] B) Option B
- [ ] C) Both are equivalent
- [ ] D) Neither affects code quality

<details>
<summary>Answer</summary>

**B) Option B**

Specific, domain-focused system prompts dramatically improve output quality. The LLM "plays the role" you define.

</details>

---

## Part 3: Temperature

### Q6. What does "temperature" control?
- [ ] A) API response speed
- [X] B) Randomness/creativity in the output
- [ ] C) Maximum token length
- [ ] D) Cost per request

<details>
<summary>Answer</summary>

**B) Randomness/creativity in the output**

- Temperature 0 = deterministic, always picks most likely token
- Temperature 1 = more random, creative variations

</details>

---

### Q7. For generating SKILL code, what temperature should you use?
- [X] A) 0.0 - 0.3 (low)
- [ ] B) 0.5 (medium)
- [ ] C) 0.8 - 1.0 (high)
- [ ] D) Temperature doesn't matter for code

<details>
<summary>Answer</summary>

**A) 0.0 - 0.3 (low)**

Code needs to be consistent and correct. High temperature introduces variations that could be bugs. Always use low temperature for code generation.

</details>

---

### Q8. You run the same prompt twice with temperature=1.0. What happens?
- [ ] A) Identical responses both times
- [X] B) Potentially different responses each time
- [ ] C) Error - temperature must be 0
- [ ] D) Faster response the second time (cached)

<details>
<summary>Answer</summary>

**B) Potentially different responses each time**

High temperature = randomness = different outputs. This is why temperature=0 is critical for reproducible automation.

</details>

---

## Part 4: Conversation History

### Q9. How does the LLM "remember" previous messages in a conversation?
- [ ] A) It stores them in a database
- [X] B) You send the entire conversation history with each request
- [ ] C) The API maintains session state automatically
- [ ] D) It uses cookies like a web browser

<details>
<summary>Answer</summary>

**B) You send the entire conversation history with each request**

The LLM is stateless. YOUR code must track conversation history and send it with each request:
```python
messages = [
    {"role": "user", "content": "First question"},
    {"role": "assistant", "content": "First answer"},
    {"role": "user", "content": "Follow-up question"}  # NEW
]
```

</details>

---

### Q10. What's the implication of Q9 for long conversations?
- [ ] A) No implications
- [X] B) Token usage increases with each turn (more expensive)
- [ ] C) Responses get faster over time
- [ ] D) The LLM becomes more accurate

<details>
<summary>Answer</summary>

**B) Token usage increases with each turn (more expensive)**

Each request includes ALL previous messages. A 20-turn conversation sends 20 messages every time. This is why:
- Context management matters
- You may need to summarize/truncate old messages
- Token costs accumulate

</details>

---

## Part 5: Practical Application

### Q11. You're building an EDA assistant. A designer asks the same question 100 times a day. How do you optimize?
- [ ] A) Increase temperature for variety
- [X] B) Cache common responses
- [ ] C) Use a longer system prompt
- [ ] D) Nothing - LLMs are already optimized

<details>
<summary>Answer</summary>

**B) Cache common responses**

For identical inputs (same prompt + parameters), cache the response. No need to call the API repeatedly for the same query.

</details>

---

### Q12. Your SKILL code generator sometimes produces invalid syntax. What's your FIRST debugging step?
- [ ] A) Switch to a different LLM
- [] B) Lower the temperature
- [ ] C) Remove the system prompt
- [ ] D) Increase max_tokens

<details>
<summary>Answer</summary>

**B) Lower the temperature**

Temperature is the most common cause of inconsistent code. Set temperature=0 first. If still failing, improve the system prompt with examples of correct syntax.

</details>

---

## Score Yourself

| Score | Level |
|-------|-------|
| 12/12 | Expert - Ready for deep technical discussions |
| 9-11 | Strong - Review the ones you missed |
| 6-8 | Good foundation - Re-read llm_basics.md |
| <6 | Need more study - Review documentation carefully |

---

## Now Run the Code!

```bash
cd ~/projects/eda-copilot
source venv/bin/activate
python 01_fundamentals/exercises/01_first_api_call.py
```

Watch how each concept plays out in real API calls.
