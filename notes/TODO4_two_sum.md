# TODO 4: Two Sum

## The Problem

Given an array and a target sum, return indices of the two numbers that add up to the target.

```
Example:
    nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]
    Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

**CAD Context:** Finding complementary values in datasets, matching signal pairs.

---

## Solution 1: Brute Force (Your approach)

```python
def two_sum(nums: list, target: int) -> list:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Time:** O(n²) | **Space:** O(1)

---

## Solution 2: Hash Map (Optimal)

```python
def two_sum(nums: list, target: int) -> list:
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

**Time:** O(n) | **Space:** O(n)

---

## Step-by-Step Explanation (Brute Force)

### 1. Outer loop: first number

```python
for i in range(len(nums)):
```

`i` goes through 0, 1, 2, ... (first number's index)

---

### 2. Inner loop: second number

```python
for j in range(i + 1, len(nums)):
```

`j` starts at `i + 1` to avoid:
- Using same element twice (i == j)
- Checking same pair twice (e.g., [0,1] and [1,0])

---

### 3. Check sum

```python
if nums[i] + nums[j] == target:
    return [i, j]
```

---

## Visualization (Brute Force)

```
nums = [2, 7, 11, 15], target = 9

i=0 (nums[0]=2):
    j=1: 2 + 7 = 9 ✓ FOUND!
    Return [0, 1]

Would continue if not found:
i=0: j=2: 2 + 11 = 13 ✗
     j=3: 2 + 15 = 17 ✗
i=1: j=2: 7 + 11 = 18 ✗
     j=3: 7 + 15 = 22 ✗
i=2: j=3: 11 + 15 = 26 ✗
```

---

## Visualization (Hash Map)

```
nums = [2, 7, 11, 15], target = 9
seen = {}

i=0, num=2:
    complement = 9 - 2 = 7
    7 not in seen
    seen = {2: 0}

i=1, num=7:
    complement = 9 - 7 = 2
    2 IS in seen! (at index 0)
    Return [0, 1]
```

---

## Python Syntax to Remember

### 1. `range(len(nums))` - Loop with index

```python
nums = [2, 7, 11]
for i in range(len(nums)):
    print(i, nums[i])
# 0 2
# 1 7
# 2 11
```

### 2. `range(i + 1, len(nums))` - Start after i

```python
for i in range(3):
    for j in range(i + 1, 3):
        print(f"({i}, {j})")
# (0, 1)
# (0, 2)
# (1, 2)
```

### 3. `enumerate()` - Index AND value

```python
nums = [2, 7, 11]
for i, num in enumerate(nums):
    print(i, num)
# 0 2
# 1 7
# 2 11
```

### 4. Dictionary for lookup

```python
seen = {}
seen[7] = 1      # Store: value 7 found at index 1
seen[7]          # Retrieve: → 1
7 in seen        # Check: → True
```

### 5. List access: `[]` not `()`

```python
nums = [2, 7, 11]
nums[0]    # ✓ Correct: → 2
nums(0)    # ✗ Error! Lists use brackets, not parentheses
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `nums(i)` | TypeError | Use `nums[i]` (brackets) |
| `list(i, j)` | TypeError | Use `[i, j]` for literal list |
| `range(i, len(nums))` | Uses same index twice | Use `range(i + 1, len(nums))` |
| `=<` | Invalid syntax | Use `<=` |
| Single loop for brute force | Only checks one number | Need nested loops |

---

## Why Hash Map is Better

```
BRUTE FORCE:
    For each number (n iterations)
        Check all remaining numbers (n iterations)
    Total: O(n²)

HASH MAP:
    For each number (n iterations)
        Look up complement in hash map (O(1))
    Total: O(n)

Example with 10,000 elements:
    Brute Force: ~100,000,000 operations
    Hash Map: ~10,000 operations
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  BRUTE FORCE                        │
│                                     │
│  for i in range(n):                 │
│    for j in range(i+1, n):          │
│      if nums[i] + nums[j] == target:│
│        return [i, j]                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  HASH MAP (Optimal)                 │
│                                     │
│  seen = {}                          │
│  for i, num in enumerate(nums):     │
│    complement = target - num        │
│    if complement in seen:           │
│      return [seen[complement], i]   │
│    seen[num] = i                    │
└─────────────────────────────────────┘
```

---

## Complexity Comparison

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| Hash Map | O(n) | O(n) |

Trade-off: Hash map uses more memory but is much faster.

---

## Edge Cases

```python
two_sum([3, 3], 6)      # → [0, 1] (same values, different indices)
two_sum([1, 2, 3], 10)  # → None or [] (no solution)
two_sum([-1, 2], 1)     # → [0, 1] (negative numbers work)
```

---

## Keywords for Interview

- "Two Sum problem"
- "Hash map for O(1) lookup"
- "Complement = target - current"
- "Trade-off: time vs space"
- "Classic LeetCode problem"
