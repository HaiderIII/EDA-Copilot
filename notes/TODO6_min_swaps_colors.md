# TODO 6: Minimum Swaps to Group Colors

## The Problem

```
Input:  "RBRBRBB"
Output: 1

Goal: Group all R on one side, all B on the other
Result: "RRRBBBB" (1 swap) or "BBBBRRRR"
```

---

## Step-by-Step Reasoning

### Step 1: Count the elements

**Question to ask yourself:** How many R? How many B?

```python
num_R = colors.count("R")  # 3
num_B = colors.count("B")  # 4
```

**Why?** This defines the final "zones":
- If R on left → positions `0` to `num_R-1` should be R
- If B on left → positions `0` to `num_B-1` should be B

---

### Step 2: Identify "misplaced" elements

```
"RBRBRBB"
 0123456

If R on left (positions 0,1,2 should be R):
Position 0: R ✓ (well placed)
Position 1: B ✗ (misplaced)
Position 2: R ✓ (well placed)

→ 1 misplaced element = 1 swap needed
```

**Key insight:** Each B misplaced in the R zone must be swapped with an R misplaced in the B zone.

---

### Step 3: Consider both cases

Sometimes putting B on left requires fewer swaps!

```
Example: "BBRR"
- R on left: positions 0,1 should be R → 2 B misplaced → 2 swaps
- B on left: positions 0,1 should be B → 0 misplaced → 0 swaps ✓
```

---

## Final Python Code

```python
def min_swaps_colors(colors: str) -> int:
    num_R = colors.count("R")
    num_B = colors.count("B")

    # Case 1: R on left - count B in the R zone
    swaps_R_left = sum(1 for i in range(num_R) if colors[i] == "B")

    # Case 2: B on left - count R in the B zone
    swaps_B_left = sum(1 for i in range(num_B) if colors[i] == "R")

    return min(swaps_R_left, swaps_B_left)
```

---

## Python Syntax to Remember

### 1. Count in a string

```python
s = "RBRBRBB"
s.count("R")    # ✓ → 3
s.counter("R")  # ✗ DOES NOT EXIST!
```

### 2. Count with condition (sum + generator)

```python
# Long method
count = 0
for i in range(n):
    if condition:
        count += 1

# Short method (Pythonic)
count = sum(1 for i in range(n) if condition)
```

**How it works:**
- `(1 for i in range(n) if condition)` generates a `1` each time the condition is true
- `sum()` adds up all those `1`s

### 3. Access the first N elements

```python
s = "RBRBRBB"

# First 3 characters
for i in range(3):
    print(s[i])  # R, B, R

# Or with slicing
s[:3]  # "RBR"
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│ 1. COUNT: how many of each?         │
│    num_R = colors.count("R")        │
│    num_B = colors.count("B")        │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 2. DEFINE THE ZONES                 │
│    Zone R = positions 0 to num_R-1  │
│    Zone B = positions 0 to num_B-1  │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 3. COUNT THE MISPLACED              │
│    Case 1: B in zone R              │
│    Case 2: R in zone B              │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 4. RETURN THE MINIMUM               │
│    return min(case1, case2)         │
└─────────────────────────────────────┘
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | One pass for count, one for sum |
| **Space** | O(1) | Only a few variables |

---

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| `s.counter()` | `s.count()` |
| Forgetting the 2nd case | Always consider both options |
| `s(i)` to access | `s[i]` (brackets, not parentheses) |

---

## Keywords for Interview

- "Two-pointer approach" (two zones approach)
- "Greedy algorithm" (we count the misplaced)
- "O(n) time complexity"
- "Consider both cases" (R on left vs B on left)
