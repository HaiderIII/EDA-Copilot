# TODO 11: Compare Two Files and Find Differences

## The Problem

```
Input:
    file1 = ["line1", "line2", "line3"]
    file2 = ["line1", "line2_modified", "line4"]

Output:
    {
        "only_in_file1": [],
        "only_in_file2": [],
        "different": [("line2", "line2_modified"), ("line3", "line4")]
    }
```

**CAD Context:** Compare netlists, config files, or reports between runs to detect changes.

---

## Reasoning

### Three categories of differences

1. **only_in_file1** → Lines that exist in file1 but not in file2 (extra lines)
2. **only_in_file2** → Lines that exist in file2 but not in file1 (extra lines)
3. **different** → Lines at the same position but with different content

---

## Step-by-Step Logic

```
file1 = ["A", "B", "C"]
file2 = ["A", "X", "C", "D"]

Position 0: "A" == "A" → same, skip
Position 1: "B" != "X" → different
Position 2: "C" == "C" → same, skip
Position 3: file1 has nothing, file2 has "D" → only_in_file2
```

---

## Final Code

```python
def compare_files(file1_lines: list, file2_lines: list) -> dict:
    """Compare two files and return differences."""
    only_in_file1 = []
    only_in_file2 = []
    different = []

    len1 = len(file1_lines)
    len2 = len(file2_lines)
    max_len = max(len1, len2)

    for i in range(max_len):
        line1 = file1_lines[i] if i < len1 else None
        line2 = file2_lines[i] if i < len2 else None

        if line1 != line2:
            if line1 is not None and line2 is not None:
                different.append((line1, line2))
            elif line1 is not None:
                only_in_file1.append(line1)
            else:
                only_in_file2.append(line2)

    return {
        "only_in_file1": only_in_file1,
        "only_in_file2": only_in_file2,
        "different": different
    }
```

---

## Python Syntax to Remember

### 1. Ternary Operator (inline if/else)

```python
# Long form
if i < len1:
    line1 = file1_lines[i]
else:
    line1 = None

# Short form (ternary)
line1 = file1_lines[i] if i < len1 else None
```

### 2. `is not None` vs `!= None`

```python
# Preferred (more Pythonic)
if line1 is not None:

# Also works but less idiomatic
if line1 != None:
```

### 3. Append a tuple

```python
different = []
different.append((line1, line2))  # Adds a tuple (line1, line2)

# Result: [("line2", "line2_modified"), ("line3", "line4")]
```

### 4. `max()` with multiple values

```python
max_len = max(len1, len2)  # Returns the larger value
max(5, 3)   # → 5
max(2, 10)  # → 10
```

---

## Step-by-Step Visualization

```
file1 = ["line1", "line2", "line3"]
file2 = ["line1", "line2_modified", "line4"]

len1 = 3, len2 = 3, max_len = 3

i=0: line1="line1", line2="line1"
     line1 == line2 → skip

i=1: line1="line2", line2="line2_modified"
     line1 != line2 and both not None
     → different.append(("line2", "line2_modified"))

i=2: line1="line3", line2="line4"
     line1 != line2 and both not None
     → different.append(("line3", "line4"))

Result:
{
    "only_in_file1": [],
    "only_in_file2": [],
    "different": [("line2", "line2_modified"), ("line3", "line4")]
}
```

---

## Another Example (Different Lengths)

```
file1 = ["A", "B", "C", "D", "E"]
file2 = ["A", "B", "X"]

len1 = 5, len2 = 3, max_len = 5

i=0: "A" == "A" → skip
i=1: "B" == "B" → skip
i=2: "C" != "X" → different.append(("C", "X"))
i=3: "D" != None → only_in_file1.append("D")
i=4: "E" != None → only_in_file1.append("E")

Result:
{
    "only_in_file1": ["D", "E"],
    "only_in_file2": [],
    "different": [("C", "X")]
}
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  INPUT: Two lists of lines          │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  CALCULATE max length               │
│  max_len = max(len1, len2)          │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  FOR EACH POSITION i                │
│                                     │
│  line1 = file1[i] or None           │
│  line2 = file2[i] or None           │
│                                     │
│  If line1 != line2:                 │
│    ├─ Both exist → different        │
│    ├─ Only line1 → only_in_file1    │
│    └─ Only line2 → only_in_file2    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  OUTPUT: Dictionary with 3 lists    │
└─────────────────────────────────────┘
```

---

## Alternative Approach: Using `set` (content-based)

```python
def compare_files_set(file1_lines, file2_lines):
    set1 = set(file1_lines)
    set2 = set(file2_lines)
    return {
        "only_in_file1": list(set1 - set2),
        "only_in_file2": list(set2 - set1),
        "in_both": list(set1 & set2)
    }
```

**Limitation:** Set approach doesn't preserve positions or detect "different" lines.

Your line-by-line approach is better for comparing files where **position matters**.

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Single pass through max(len1, len2) |
| **Space** | O(n) | Store differences in lists |

---

## Real CAD Application

```python
# Compare two netlist versions
with open("netlist_v1.sp") as f1:
    v1_lines = f1.read().splitlines()

with open("netlist_v2.sp") as f2:
    v2_lines = f2.read().splitlines()

diff = compare_files(v1_lines, v2_lines)

print("Added lines:", diff["only_in_file2"])
print("Removed lines:", diff["only_in_file1"])
print("Modified lines:", diff["different"])
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `file1[i]` without bounds check | IndexError | Use ternary: `if i < len1 else None` |
| `!= None` | Works but not Pythonic | Use `is not None` |
| Forgetting different lengths | Misses extra lines | Use `max(len1, len2)` |

---

## Keywords for Interview

- "Line-by-line comparison"
- "Diff algorithm"
- "File comparison"
- "Bounds checking"
- "Ternary operator"
