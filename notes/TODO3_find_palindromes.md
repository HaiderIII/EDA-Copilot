# TODO 3: Find All Palindrome Substrings

## The Problem

Find all palindrome substrings in a string. A palindrome reads the same forwards and backwards.

```
Example:
    "aab" → ["a", "a", "b", "aa"]
    "abc" → ["a", "b", "c"]
    "aba" → ["a", "b", "a", "aba"]
```

**CAD Context:** Pattern detection in signal names, finding symmetric structures in designs.

---

## Solution: Brute Force with Set

```python
def find_palindromes(s: str) -> list:
    palindromes = set()  # Use set to avoid duplicates
    n = len(s)

    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if substring == substring[::-1]:
                palindromes.add(substring)

    return list(palindromes)
```

---

## Step-by-Step Explanation

### 1. Use a set for unique results

```python
palindromes = set()
```

Why set? To avoid duplicates like `"a"` appearing multiple times.

---

### 2. Generate all substrings

```python
for i in range(n):           # Start index
    for j in range(i + 1, n + 1):  # End index (exclusive)
        substring = s[i:j]
```

**Slicing:** `s[i:j]` gives characters from index `i` to `j-1`.

---

### 3. Check if palindrome

```python
if substring == substring[::-1]:
    palindromes.add(substring)
```

`[::-1]` reverses the string. If equal to original, it's a palindrome.

---

### 4. Convert set to list

```python
return list(palindromes)
```

---

## Visualization

```
String: "aab"
n = 3

All substrings:
i=0, j=1: s[0:1] = "a"   → "a" == "a" ✓ palindrome
i=0, j=2: s[0:2] = "aa"  → "aa" == "aa" ✓ palindrome
i=0, j=3: s[0:3] = "aab" → "aab" != "baa" ✗
i=1, j=2: s[1:2] = "a"   → "a" == "a" ✓ palindrome (duplicate, set ignores)
i=1, j=3: s[1:3] = "ab"  → "ab" != "ba" ✗
i=2, j=3: s[2:3] = "b"   → "b" == "b" ✓ palindrome

Result: {"a", "aa", "b"} → ["a", "aa", "b"]
```

---

## Python Syntax to Remember

### 1. String slicing `s[i:j]`

```python
s = "hello"
s[0:2]    # → "he" (index 0, 1)
s[1:4]    # → "ell" (index 1, 2, 3)
s[2:]     # → "llo" (from index 2 to end)
s[:3]     # → "hel" (from start to index 2)
```

### 2. Reverse with `[::-1]`

```python
"abc"[::-1]     # → "cba"
[1, 2, 3][::-1] # → [3, 2, 1]
```

### 3. Set operations

```python
s = set()
s.add("a")      # Add element
s.add("a")      # Duplicate ignored
s.add("b")
print(s)        # → {"a", "b"}
list(s)         # → ["a", "b"] (order not guaranteed)
```

### 4. Range for nested loops

```python
for i in range(n):              # 0, 1, ..., n-1
    for j in range(i + 1, n + 1):  # i+1, i+2, ..., n
```

**Why `n + 1`?** Because `s[i:j]` excludes index `j`. To include the last character, `j` must go up to `n`.

---

## Alternative: Expand Around Center (Optimal)

```python
def find_palindromes_optimal(s: str) -> list:
    palindromes = set()
    n = len(s)

    def expand(left, right):
        while left >= 0 and right < n and s[left] == s[right]:
            palindromes.add(s[left:right+1])
            left -= 1
            right += 1

    for i in range(n):
        expand(i, i)      # Odd-length palindromes (center = single char)
        expand(i, i + 1)  # Even-length palindromes (center = between chars)

    return list(palindromes)
```

This approach is O(n²) vs O(n³) for brute force.

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  BRUTE FORCE APPROACH               │
│                                     │
│  1. Generate ALL substrings         │
│     for i in range(n):              │
│       for j in range(i+1, n+1):     │
│         substring = s[i:j]          │
│                                     │
│  2. Check if palindrome             │
│     substring == substring[::-1]    │
│                                     │
│  3. Use SET to avoid duplicates     │
└─────────────────────────────────────┘
```

---

## Complexity

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n³) | O(n²) |
| Expand Around Center | O(n²) | O(n²) |

- Brute Force: O(n²) substrings × O(n) to check each
- Expand: O(n) centers × O(n) expansion

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `range(i, n+1)` for j | Includes empty string | Use `range(i+1, n+1)` |
| Using list instead of set | Duplicates in result | Use set |
| `s[i:j-1]` | Wrong slice bounds | `s[i:j]` already excludes j |
| Forgetting single characters | Missing "a", "b" | Single chars are palindromes |

---

## Edge Cases

```python
find_palindromes("")      # → []
find_palindromes("a")     # → ["a"]
find_palindromes("aa")    # → ["a", "aa"]
find_palindromes("ab")    # → ["a", "b"]
```

---

## Keywords for Interview

- "Palindrome checking"
- "Substring generation"
- "Set for deduplication"
- "String reversal with [::-1]"
- "Expand around center" (optimal)
- "O(n²) or O(n³) complexity"
