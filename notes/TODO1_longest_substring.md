# TODO 1: Longest Substring Without Repeating Characters

## The Problem

Find the length of the longest substring without repeating characters.

```
Example:
    "abcabcbb" → 3 (answer is "abc")
    "bbbbb" → 1 (answer is "b")
    "pwwkew" → 3 (answer is "wke")
```

**CAD Context:** Finding unique signal names, analyzing patterns in logs without repetition.

---

## Solution: Sliding Window

```python
def longest_substring_no_repeat(s: str) -> int:
    char_index = {}    # Store last seen position of each character
    max_length = 0
    start = 0          # Start of current window

    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1  # Move start past the duplicate
        char_index[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length
```

---

## Step-by-Step Explanation

### 1. Initialize variables

```python
char_index = {}    # Dictionary: character → last index where it appeared
max_length = 0     # Track the longest substring found
start = 0          # Left boundary of sliding window
```

---

### 2. Iterate with enumerate

```python
for end, char in enumerate(s):
```

`enumerate(s)` gives us both:
- `end` = current index (0, 1, 2, ...)
- `char` = character at that index

---

### 3. Check for duplicate

```python
if char in char_index and char_index[char] >= start:
    start = char_index[char] + 1
```

**Two conditions:**
1. `char in char_index` → We've seen this character before
2. `char_index[char] >= start` → The duplicate is within our current window

If both true, move `start` to skip past the duplicate.

---

### 4. Update character position

```python
char_index[char] = end
```

Always update where we last saw this character.

---

### 5. Calculate window size

```python
max_length = max(max_length, end - start + 1)
```

Window size = `end - start + 1` (inclusive on both ends)

---

## Visualization

```
String: "abcabcbb"

Step 0: char='a', start=0, end=0
        Window: [a]bcabcbb → length=1
        char_index = {a:0}

Step 1: char='b', start=0, end=1
        Window: [ab]cabcbb → length=2
        char_index = {a:0, b:1}

Step 2: char='c', start=0, end=2
        Window: [abc]abcbb → length=3
        char_index = {a:0, b:1, c:2}

Step 3: char='a', start=0, end=3
        'a' found at index 0, which is >= start(0)
        Move start to 0+1=1
        Window: a[bca]bcbb → length=3
        char_index = {a:3, b:1, c:2}

Step 4: char='b', start=1, end=4
        'b' found at index 1, which is >= start(1)
        Move start to 1+1=2
        Window: ab[cab]cbb → length=3
        char_index = {a:3, b:4, c:2}

... continues ...

Final answer: 3 (substring "abc" or "bca" or "cab")
```

---

## Why Sliding Window?

```
┌─────────────────────────────────────┐
│  BRUTE FORCE: Check all substrings │
│  "abc" → check, "ab" → check...    │
│  Time: O(n³)                        │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  SLIDING WINDOW: One pass          │
│  Expand right, shrink left         │
│  Time: O(n)                         │
└─────────────────────────────────────┘
```

---

## Python Syntax to Remember

### 1. `enumerate()` - Get index AND value

```python
s = "abc"
for i, char in enumerate(s):
    print(i, char)
# 0 a
# 1 b
# 2 c
```

### 2. Dictionary for last seen index

```python
char_index = {}
char_index['a'] = 5      # 'a' last seen at index 5
char_index['a'] = 10     # Update: 'a' now at index 10
```

### 3. `max()` to track maximum

```python
max_length = max(max_length, new_value)
```

### 4. Window size formula

```python
# For window from index start to end (inclusive)
size = end - start + 1

# Example: start=2, end=5
# Indices: 2, 3, 4, 5 → 4 elements
# Size = 5 - 2 + 1 = 4 ✓
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  SLIDING WINDOW PATTERN            │
│                                     │
│  1. Initialize: start=0, end=0      │
│                                     │
│  2. Expand right (end++)            │
│     - Check if valid window         │
│     - If invalid, shrink left       │
│                                     │
│  3. Update answer at each step      │
│                                     │
│  4. Return max_length               │
└─────────────────────────────────────┘
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Single pass through string |
| **Space** | O(min(n, k)) | k = size of character set (26 for lowercase) |

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting `>= start` check | Counts old duplicates outside window | Add `char_index[char] >= start` |
| Using `end - start` | Off by one error | Use `end - start + 1` |
| Not updating `char_index` every time | Wrong positions | Always update after checking |
| Checking `if char not in char_index` | Misses logic | Check `if char in char_index` first |

---

## Keywords for Interview

- "Sliding window technique"
- "Two pointers"
- "Hash map for character positions"
- "O(n) single pass"
- "Window shrinking on duplicate"
