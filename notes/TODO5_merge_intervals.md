# TODO 5: Merge Overlapping Intervals

## The Problem

Given a list of intervals, merge all overlapping intervals.

```
Example:
    Input:  [[1,3], [2,6], [8,10], [15,18]]
    Output: [[1,6], [8,10], [15,18]]

    Explanation: [1,3] and [2,6] overlap → merge to [1,6]
```

**CAD Context:** Timing analysis (merging timing windows), signal overlap detection, scheduling.

---

## Solution

```python
def merge_intervals(intervals: list) -> list:
    if not intervals:
        return []

    # Step 1: Sort by start time
    intervals.sort()

    # Step 2: Initialize with first interval
    result = [intervals[0]]

    # Step 3: Process remaining intervals
    for current in intervals[1:]:
        last = result[-1]

        if current[0] <= last[1]:  # Overlap!
            last[1] = max(last[1], current[1])  # Merge
        else:
            result.append(current)

    return result
```

---

## Step-by-Step Explanation

### Step 1: Sort by start time

```python
intervals.sort()
```

Before: `[[8,10], [1,3], [2,6], [15,18]]`
After:  `[[1,3], [2,6], [8,10], [15,18]]`

**Why sort?** So we only need to compare with the previous interval.

---

### Step 2: Initialize result

```python
result = [intervals[0]]  # Start with first interval
```

`result = [[1,3]]`

---

### Step 3: Check for overlap

```python
if current[0] <= last[1]:
```

**Overlap condition:** Current start ≤ Previous end

```
last:    [1─────3]
current:    [2─────6]
              ↑
         current[0]=2 <= last[1]=3 → OVERLAP!
```

---

### Step 4: Merge or append

```python
if overlap:
    last[1] = max(last[1], current[1])  # Extend end
else:
    result.append(current)  # No overlap, add new
```

**Why `max()`?** The current interval might end before or after the previous one.

---

## Visualization

```
Input: [[1,3], [2,6], [8,10], [15,18]]

After sorting: [[1,3], [2,6], [8,10], [15,18]]

┌─────────────────────────────────────────────────────────┐
│ Timeline:                                               │
│   1   2   3   4   5   6   7   8   9  10  ...  15  16  17  18
│   [───────]                                             │
│       [───────────────]                                 │
│                           [───────────]                 │
│                                              [──────────]
└─────────────────────────────────────────────────────────┘

Step 1: result = [[1,3]]

Step 2: current = [2,6]
        current[0]=2 <= last[1]=3 → OVERLAP
        Merge: last[1] = max(3, 6) = 6
        result = [[1,6]]

Step 3: current = [8,10]
        current[0]=8 > last[1]=6 → NO OVERLAP
        Append: result = [[1,6], [8,10]]

Step 4: current = [15,18]
        current[0]=15 > last[1]=10 → NO OVERLAP
        Append: result = [[1,6], [8,10], [15,18]]

Final: [[1,6], [8,10], [15,18]]
```

---

## Python Syntax to Remember

### 1. `list.sort()` - Sort in place

```python
intervals = [[3,4], [1,2]]
intervals.sort()  # Sorts by first element, then second
# intervals = [[1,2], [3,4]]
```

### 2. `list[-1]` - Last element

```python
result = [[1,3], [8,10]]
result[-1]  # → [8,10]
```

### 3. Modifying list element

```python
last = result[-1]  # last IS the same object as result[-1]
last[1] = 6        # This modifies result[-1] too!
```

### 4. Slicing `[1:]` - Skip first element

```python
intervals = [[1,3], [2,6], [8,10]]
intervals[1:]  # → [[2,6], [8,10]]

for current in intervals[1:]:
    # Iterates over [2,6], then [8,10]
```

### 5. `max()` function

```python
max(3, 6)       # → 6
max(10, 5)      # → 10
max(7, 7)       # → 7
```

---

## Overlap Cases

```
Case 1: Partial overlap
[1─────3]
    [2─────6]
Result: [1,6]

Case 2: One contains the other
[1─────────────6]
    [2───4]
Result: [1,6] (max(6,4)=6)

Case 3: Adjacent (touching)
[1───3]
      [3───5]
Result: [1,5] (3 <= 3 is true → overlap)

Case 4: No overlap
[1───3]
        [5───7]
Result: [1,3], [5,7] (5 > 3)
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  MERGE INTERVALS                    │
│                                     │
│  1. Sort intervals by start time    │
│                                     │
│  2. Initialize result with first    │
│                                     │
│  3. For each remaining interval:    │
│     ├─ Overlap? (start <= prev end) │
│     │   YES → Merge (extend end)    │
│     │   NO  → Append new interval   │
│                                     │
│  4. Return result                   │
└─────────────────────────────────────┘
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n log n) | Sorting dominates |
| **Space** | O(n) | Result list in worst case |

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Not sorting first | Algorithm fails | Always sort first |
| `current[0] < last[1]` | Misses adjacent intervals | Use `<=` |
| `last[1] = current[1]` | Wrong when current ends earlier | Use `max(last[1], current[1])` |
| Forgetting empty check | Error on empty input | Add `if not intervals: return []` |

---

## Edge Cases

```python
merge_intervals([])                    # → []
merge_intervals([[1,3]])               # → [[1,3]]
merge_intervals([[1,4], [2,3]])        # → [[1,4]] (contained)
merge_intervals([[1,2], [2,3]])        # → [[1,3]] (adjacent)
merge_intervals([[1,2], [3,4]])        # → [[1,2], [3,4]] (no overlap)
```

---

## Keywords for Interview

- "Merge overlapping intervals"
- "Sort by start time first"
- "Greedy approach"
- "Overlap condition: start <= previous end"
- "Common in scheduling problems"
- "O(n log n) due to sorting"
