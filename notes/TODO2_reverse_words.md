# TODO 2: Reverse Words in a String

## The Problem

Reverse the order of words in a string. Also handle extra spaces.

```
Example:
    "the sky is blue" → "blue is sky the"
    "  hello world  " → "world hello"
    "a" → "a"
```

**CAD Context:** Reformatting log entries, reversing path hierarchies, string manipulation in scripts.

---

## Solution: One-liner

```python
def reverse_words(s: str) -> str:
    words = s.strip().split()
    return ' '.join(reversed(words))
```

Or even shorter:
```python
return ' '.join(s.split()[::-1])
```

---

## Step-by-Step Explanation

### Step 1: `strip()` - Remove leading/trailing spaces

```python
s = "  hello world  "
s.strip()  # → "hello world"
```

---

### Step 2: `split()` - Break into words

```python
"hello world".split()  # → ["hello", "world"]
```

**Note:** `split()` without arguments:
- Splits on ANY whitespace (spaces, tabs, newlines)
- Removes empty strings from result

```python
"  hello   world  ".split()  # → ["hello", "world"]
# Multiple spaces handled automatically!
```

---

### Step 3: `reversed()` - Reverse the list

```python
words = ["the", "sky", "is", "blue"]
list(reversed(words))  # → ["blue", "is", "sky", "the"]
```

---

### Step 4: `join()` - Combine with spaces

```python
words = ["blue", "is", "sky", "the"]
' '.join(words)  # → "blue is sky the"
```

---

## Visualization

```
Input: "  hello world  "

Step 1: strip()
        "hello world"

Step 2: split()
        ["hello", "world"]

Step 3: reversed()
        ["world", "hello"]

Step 4: join()
        "world hello"
```

---

## Python Syntax to Remember

### 1. `str.strip()` - Remove whitespace from ends

```python
"  text  ".strip()      # → "text"
"  text  ".lstrip()     # → "text  " (left only)
"  text  ".rstrip()     # → "  text" (right only)
```

### 2. `str.split()` - Split into list

```python
# Without argument: split on whitespace
"a b  c".split()        # → ["a", "b", "c"]

# With argument: split on specific character
"a,b,c".split(",")      # → ["a", "b", "c"]
"a,,b".split(",")       # → ["a", "", "b"] (keeps empty!)
```

### 3. `reversed()` vs `[::-1]`

```python
words = ["a", "b", "c"]

# reversed() - returns iterator (memory efficient)
list(reversed(words))   # → ["c", "b", "a"]

# [::-1] - returns new list (also works on strings)
words[::-1]             # → ["c", "b", "a"]
"abc"[::-1]             # → "cba"
```

### 4. `str.join()` - Combine list into string

```python
# Syntax: separator.join(list)
" ".join(["a", "b"])    # → "a b"
"-".join(["a", "b"])    # → "a-b"
"".join(["a", "b"])     # → "ab"
```

---

## Alternative Approaches

### Approach 1: split + reversed + join (Recommended)

```python
def reverse_words(s: str) -> str:
    return ' '.join(reversed(s.split()))
```

### Approach 2: split + slicing

```python
def reverse_words(s: str) -> str:
    return ' '.join(s.split()[::-1])
```

### Approach 3: Manual (for learning)

```python
def reverse_words(s: str) -> str:
    words = s.split()
    left, right = 0, len(words) - 1
    while left < right:
        words[left], words[right] = words[right], words[left]
        left += 1
        right -= 1
    return ' '.join(words)
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  REVERSE WORDS PATTERN              │
│                                     │
│  1. Clean: strip() whitespace       │
│  2. Break: split() into words       │
│  3. Reverse: reversed() or [::-1]   │
│  4. Rebuild: join() with space      │
└─────────────────────────────────────┘
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Process each character once |
| **Space** | O(n) | Store words in list |

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `split(" ")` | Keeps empty strings | Use `split()` without args |
| Forgetting `strip()` | Extra spaces in result | Always `strip()` first |
| `reverse()` vs `reversed()` | `reverse()` is in-place, returns None | Use `reversed()` for return value |
| `"".join(words)` | No spaces between words | Use `" ".join(words)` |

---

## Edge Cases

```python
reverse_words("")           # → "" (empty)
reverse_words("   ")        # → "" (only spaces)
reverse_words("a")          # → "a" (single word)
reverse_words("a b")        # → "b a" (two words)
```

---

## Keywords for Interview

- "String manipulation"
- "split() and join()"
- "Whitespace handling"
- "reversed() vs [::-1]"
- "O(n) time complexity"
