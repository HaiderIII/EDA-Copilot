# TODO 7: Parse Key-Value Pairs

## The Problem

```
Input:  "width=10 height=20 depth=5"
Output: {"width": "10", "height": "20", "depth": "5"}

Goal: Transform a config string into a Python dictionary
```

**CAD Context:** Very common in EDA configuration files (Cadence, Synopsys, etc.)

---

## Step-by-Step Reasoning

### Step 1: Split by spaces

```python
s = "width=10 height=20 depth=5"
pairs = s.split()  # ["width=10", "height=20", "depth=5"]
```

**`split()` without argument:** splits by whitespace (one or more)

---

### Step 2: For each pair, split by "="

```python
pair = "width=10"
key, value = pair.split("=")  # key="width", value="10"
```

**Unpacking:** `a, b = list` assigns the 1st element to `a`, the 2nd to `b`

---

### Step 3: Store in a dictionary

```python
result = {}
result[key] = value  # result["width"] = "10"
```

---

## Final Python Code

```python
def parse_key_value(s: str) -> dict:
    pairs = s.split()        # Split by spaces
    result = {}
    for pair in pairs:
        key, value = pair.split("=")  # Split by "="
        result[key] = value
    return result
```

---

## Step-by-Step Visualization

```
Input: "width=10 height=20 depth=5"

Step 1: split()
         ↓
["width=10", "height=20", "depth=5"]

Step 2: Loop
         ↓
Iteration 1: "width=10"  → split("=") → ["width", "10"]
             key="width", value="10"
             result = {"width": "10"}

Iteration 2: "height=20" → split("=") → ["height", "20"]
             key="height", value="20"
             result = {"width": "10", "height": "20"}

Iteration 3: "depth=5"   → split("=") → ["depth", "5"]
             key="depth", value="5"
             result = {"width": "10", "height": "20", "depth": "5"}

Output: {"width": "10", "height": "20", "depth": "5"}
```

---

## Python Syntax to Remember

### 1. `split()` - Split a string

```python
# Without argument: splits by whitespace (handles multiple spaces)
"a b  c".split()      # → ["a", "b", "c"]

# With argument: splits by that character
"a=b".split("=")      # → ["a", "b"]
"a,b,c".split(",")    # → ["a", "b", "c"]
```

### 2. Unpacking - Assign multiple variables

```python
# List of 2 elements → 2 variables
key, value = ["width", "10"]  # key="width", value="10"

# Equivalent to:
temp = ["width", "10"]
key = temp[0]
value = temp[1]
```

### 3. Dictionary - Create and populate

```python
# Create an empty dict
d = {}

# Add a key-value pair
d["key"] = "value"

# Access a value
print(d["key"])  # → "value"
```

---

## Compact Version (Pythonic)

```python
def parse_key_value(s: str) -> dict:
    return dict(pair.split("=") for pair in s.split())
```

**How it works:**
1. `s.split()` → list of pairs
2. `pair.split("=")` → list `[key, value]` for each pair
3. `dict(...)` → converts `[key, value]` pairs into a dictionary

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  INPUT STRING                       │
│  "width=10 height=20 depth=5"       │
└─────────────────┬───────────────────┘
                  │ split()
                  ▼
┌─────────────────────────────────────┐
│  LIST OF PAIRS                      │
│  ["width=10", "height=20", "depth=5"]│
└─────────────────┬───────────────────┘
                  │ for pair in pairs
                  ▼
┌─────────────────────────────────────┐
│  FOR EACH PAIR                      │
│  pair.split("=") → [key, value]     │
│  result[key] = value                │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  RESULT DICTIONARY                  │
│  {"width": "10", "height": "20"...} │
└─────────────────────────────────────┘
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Traverses each character once |
| **Space** | O(k) | k = number of key-value pairs |

---

## Edge Cases to Consider (Bonus)

```python
# Empty string
parse_key_value("")  # → {}

# Multiple spaces
parse_key_value("a=1   b=2")  # → {"a": "1", "b": "2"} (split() handles this)

# Value containing "=" (watch out!)
parse_key_value("url=http://a=b")  # → Problem! split("=") gives 3 parts
# Solution: split("=", 1) to limit to 1 split
```

---

## Real CAD Application

```python
# Cadence config file
config = "technology=7nm voltage=0.75 temperature=25"
params = parse_key_value(config)

print(params["technology"])  # → "7nm"
print(params["voltage"])     # → "0.75"
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `s.split(" ")` | Doesn't handle multiple spaces | Use `s.split()` |
| `pair.split()` | Splits by space, not "=" | `pair.split("=")` |
| Forgetting `result = {}` | NameError | Always initialize the dict |

---

## Keywords for Interview

- "String parsing"
- "Dictionary building"
- "split() method"
- "Key-value pairs"
- "Configuration file parsing"
