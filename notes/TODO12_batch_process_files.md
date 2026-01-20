# TODO 12: Batch Process Files with Pattern Matching

## The Problem

```
Input:
    files = ["test1.v", "test2.v", "lib.sv", "data.txt"]
    pattern = "*.v"
    transform = lambda x: x.replace(".v", "_new.v")

Output:
    ["test1_new.v", "test2_new.v"]
```

**CAD Context:** Batch rename Verilog files, process simulation outputs, organize design files.

---

## Final Code

```python
import fnmatch

def batch_process_files(files: list, pattern: str, transform) -> list:
    """Filter files by pattern and apply transformation."""
    matched_files = fnmatch.filter(files, pattern)
    return [transform(f) for f in matched_files]
```

Or in one line:
```python
return [transform(f) for f in fnmatch.filter(files, pattern)]
```

---

## Step-by-Step Logic

```
files = ["test1.v", "test2.v", "lib.sv", "data.txt"]
pattern = "*.v"

Step 1: fnmatch.filter(files, "*.v")
        → ["test1.v", "test2.v"]
        (lib.sv doesn't match *.v, data.txt doesn't match)

Step 2: Apply transform to each matched file
        → transform("test1.v") = "test1_new.v"
        → transform("test2.v") = "test2_new.v"

Result: ["test1_new.v", "test2_new.v"]
```

---

## Python Syntax to Remember

### 1. `fnmatch.filter()` - Glob pattern matching

```python
import fnmatch

files = ["test.v", "test.sv", "test.txt"]

fnmatch.filter(files, "*.v")    # → ["test.v"]
fnmatch.filter(files, "*.sv")   # → ["test.sv"]
fnmatch.filter(files, "test.*") # → ["test.v", "test.sv", "test.txt"]
fnmatch.filter(files, "*.?v")   # → ["test.v", "test.sv"] (? = single char)
```

### 2. Glob pattern wildcards

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*` | Match everything | `*.v` matches `test.v`, `foo.v` |
| `?` | Match single character | `test?.v` matches `test1.v` |
| `[abc]` | Match a, b, or c | `test[123].v` matches `test1.v` |
| `[!abc]` | Match NOT a, b, c | `test[!0].v` matches `test1.v` |

### 3. Lambda functions

```python
# Long form
def transform(x):
    return x.replace(".v", "_new.v")

# Short form (lambda)
transform = lambda x: x.replace(".v", "_new.v")

# Both are equivalent
transform("test.v")  # → "test_new.v"
```

### 4. List comprehension

```python
# Long form
result = []
for f in matched_files:
    result.append(transform(f))

# Short form (list comprehension)
result = [transform(f) for f in matched_files]
```

### 5. Functions as parameters

```python
def batch_process_files(files, pattern, transform):
    # 'transform' is a function passed as argument
    # We can call it like: transform(f)
    return [transform(f) for f in files]

# Usage:
batch_process_files(files, "*.v", lambda x: x.upper())
batch_process_files(files, "*.v", str.upper)  # Same thing
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  INPUT: files, pattern, transform   │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  FILTER: fnmatch.filter()           │
│  Keep only files matching pattern   │
│  ["test1.v", "test2.v"]             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  TRANSFORM: apply function          │
│  [transform(f) for f in matched]    │
│  ["test1_new.v", "test2_new.v"]     │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│  OUTPUT: transformed list           │
└─────────────────────────────────────┘
```

---

## Alternative: Manual implementation (without fnmatch)

```python
def batch_process_files_manual(files, pattern, transform):
    result = []
    for f in files:
        if fnmatch.fnmatch(f, pattern):  # Check single file
            result.append(transform(f))
    return result
```

---

## Real CAD Applications

### Rename Verilog files

```python
files = ["adder.v", "mult.v", "alu.v"]
batch_process_files(files, "*.v", lambda x: x.replace(".v", "_syn.v"))
# → ["adder_syn.v", "mult_syn.v", "alu_syn.v"]
```

### Add prefix to netlists

```python
files = ["top.sp", "pll.sp", "io.sp"]
batch_process_files(files, "*.sp", lambda x: "post_sim_" + x)
# → ["post_sim_top.sp", "post_sim_pll.sp", "post_sim_io.sp"]
```

### Get base names

```python
files = ["dir/test1.v", "dir/test2.v"]
import os
batch_process_files(files, "*.v", os.path.basename)
# → ["test1.v", "test2.v"]
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Filter + transform each file once |
| **Space** | O(m) | m = number of matched files |

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting `import fnmatch` | NameError | Always import |
| `*.v` matches `*.sv` | No, `*.v` only matches `.v` extension | Use `*.*v` or `*.{v,sv}` |
| Lambda missing return | Returns None | Lambda auto-returns expression |

---

## fnmatch vs glob vs re

| Module | Use case | Example |
|--------|----------|---------|
| `fnmatch` | Filter list of strings | `fnmatch.filter(files, "*.v")` |
| `glob` | Find files on disk | `glob.glob("*.v")` |
| `re` | Complex regex patterns | `re.search(r"test\d+\.v", f)` |

---

## Keywords for Interview

- "Glob pattern matching"
- "fnmatch module"
- "Higher-order functions" (function as parameter)
- "List comprehension"
- "Lambda functions"
- "Batch processing"
