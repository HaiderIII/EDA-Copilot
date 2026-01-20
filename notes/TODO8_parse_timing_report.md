# TODO 8: Parse Timing Report (Regex)

## The Problem

```
Input:  "Setup slack: -0.5ns | Hold slack: 0.2ns | Clock: clk_main"
Output: {"setup_slack": -0.5, "hold_slack": 0.2, "clock": "clk_main"}
```

**CAD Context:** Parse timing reports from EDA tools (PrimeTime, Tempus, etc.)

---

## Two Approaches

### Approach 1: split() (basic)

```python
def parse_timing_report(line: str) -> dict:
    pairs = line.split("|")
    result = {}
    for pair in pairs:
        key, value = pair.split(": ")
        # Problem: need to transform key and value manually
        # "Setup slack" → "setup_slack"
        # "-0.5ns" → -0.5
    return result
```

**Problem:** Lots of manual transformations needed.

---

### Approach 2: regex (clean) ✓

```python
import re

def parse_timing_report(line: str) -> dict:
    setup = re.search(r"Setup slack:\s*(-?[\d.]+)ns", line)
    hold = re.search(r"Hold slack:\s*(-?[\d.]+)ns", line)
    clock = re.search(r"Clock:\s*(\w+)", line)

    return {
        "setup_slack": float(setup.group(1)),
        "hold_slack": float(hold.group(1)),
        "clock": clock.group(1)
    }
```

---

## Understanding Regex

### Anatomy of a pattern

```
Pattern: r"Setup slack:\s*(-?[\d.]+)ns"

Setup slack:  → Exact text to find
\s*           → 0 or more spaces
(             → Start of capture group
  -?          → Optional minus sign (? = 0 or 1)
  [\d.]+      → One or more digits or dots
)             → End of capture group
ns            → Text "ns"
```

### Visualization

```
Text:    "Setup slack: -0.5ns"
Pattern: "Setup slack:\s*(-?[\d.]+)ns"
                        ↑_______↑
                        Capture: "-0.5"

match.group(0) → "Setup slack: -0.5ns"  (complete match)
match.group(1) → "-0.5"                  (first group)
```

---

## Regex Syntax to Remember

### Basic symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| `\d` | One digit [0-9] | `\d` matches "5" |
| `\d+` | One or more digits | `\d+` matches "123" |
| `\w` | Letter, digit or _ | `\w+` matches "clk_main" |
| `\s` | Space, tab, newline | `\s*` matches "   " |
| `.` | Any character | `a.c` matches "abc" |
| `*` | 0 or more | `a*` matches "", "a", "aaa" |
| `+` | 1 or more | `a+` matches "a", "aaa" |
| `?` | 0 or 1 (optional) | `-?` matches "", "-" |

### Character classes

| Pattern | Meaning |
|---------|---------|
| `[abc]` | a, b or c |
| `[0-9]` | Digit (= `\d`) |
| `[a-z]` | Lowercase letter |
| `[A-Za-z]` | Uppercase or lowercase letter |
| `[\d.]+` | Digits or dots |
| `[-\d.]+` | Minus, digits or dots |

### Capture groups

```python
import re

text = "width=100"
match = re.search(r"(\w+)=(\d+)", text)

match.group(0)  # → "width=100" (complete match)
match.group(1)  # → "width"     (1st group)
match.group(2)  # → "100"       (2nd group)
```

---

## Main re Functions

### `re.search()` - Find the first match

```python
import re

text = "Setup slack: -0.5ns"
match = re.search(r"(-?[\d.]+)ns", text)

if match:
    print(match.group(1))  # → "-0.5"
```

### `re.findall()` - Find all matches

```python
text = "a=1 b=2 c=3"
matches = re.findall(r"(\w+)=(\d+)", text)
# → [("a", "1"), ("b", "2"), ("c", "3")]
```

### `re.sub()` - Replace

```python
text = "Hello World"
result = re.sub(r"\s+", "_", text)
# → "Hello_World"
```

---

## Mental Schema for Regex

```
┌─────────────────────────────────────┐
│ 1. IDENTIFY what you're looking for │
│    "Setup slack: -0.5ns"            │
│     ↓                               │
│    Fixed text + variable value      │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 2. BUILD the pattern                │
│    Fixed text: "Setup slack:\s*"    │
│    Value:      "(-?[\d.]+)"         │
│    Suffix:     "ns"                 │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 3. CAPTURE with ()                  │
│    () creates a group               │
│    Accessible via .group(1)         │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 4. CONVERT the result               │
│    float(match.group(1))            │
└─────────────────────────────────────┘
```

---

## Useful Patterns for CAD

### Timing values

```python
# Slack in ns
r"(-?[\d.]+)ns"           # → "-0.5"

# Slack in ps
r"(-?[\d.]+)ps"           # → "150"

# With variable unit
r"(-?[\d.]+)(ns|ps|us)"   # group(1)=value, group(2)=unit
```

### Signal names

```python
# Signal name
r"(\w+)"                  # → "clk_main"

# Hierarchical path
r"([\w/]+)"               # → "top/cpu/alu"

# Bus signal
r"(\w+)\[(\d+)\]"         # → "data", "7" for "data[7]"
```

### Values with units

```python
# Capacitance
r"(\d+\.?\d*)(fF|pF)"     # → "10.5", "fF"

# Resistance
r"(\d+\.?\d*)(ohm|kohm)"  # → "100", "kohm"

# Size
r"w=(\d+)([nu]).*l=(\d+)([nu])"  # w=1u l=100n
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting `r"..."` | Backslash interpreted | Always use `r"pattern"` |
| Forgetting `match.group(1)` | Returns match object | Use `.group(1)` for capture |
| `\d` without `+` | Matches single digit | `\d+` for multiple |
| Pattern too strict | Doesn't match variations | Use `\s*` for flexible spaces |

---

## Final Code

```python
import re

def parse_timing_report(line: str) -> dict:
    """Extract timing values from a timing report line."""

    setup = re.search(r"Setup slack:\s*(-?[\d.]+)ns", line)
    hold = re.search(r"Hold slack:\s*(-?[\d.]+)ns", line)
    clock = re.search(r"Clock:\s*(\w+)", line)

    return {
        "setup_slack": float(setup.group(1)),
        "hold_slack": float(hold.group(1)),
        "clock": clock.group(1)
    }
```

---

## Keywords for Interview

- "Regular expressions"
- "Pattern matching"
- "Capture groups"
- "Text parsing"
- "Log file analysis"
