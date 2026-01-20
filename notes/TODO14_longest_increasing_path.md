# TODO 14: Longest Increasing Path in Matrix

## The Problem

Find the longest path in a matrix where each step moves to a **strictly greater** value. You can move up, down, left, or right (not diagonal).

```
Matrix:
[[9, 9, 4],
 [6, 6, 8],
 [2, 1, 1]]

Answer: 4 (path: 1 → 2 → 6 → 9)
```

**CAD Context:** Finding critical paths in timing analysis, dependency chains in design hierarchy.

---

## Solution: DFS + Memoization

```python
def longest_increasing_path(matrix: list) -> int:
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    memo = [[0] * cols for _ in range(rows)]

    def dfs(r, c):
        if memo[r][c]:
            return memo[r][c]

        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        max_length = 1

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                length = 1 + dfs(nr, nc)
                max_length = max(max_length, length)

        memo[r][c] = max_length
        return max_length

    longest_path = 0
    for i in range(rows):
        for j in range(cols):
            longest_path = max(longest_path, dfs(i, j))

    return longest_path
```

---

## Step-by-Step Explanation

### 1. Edge case

```python
if not matrix or not matrix[0]:
    return 0
```
Handle empty matrix.

---

### 2. Initialize memo table

```python
rows, cols = len(matrix), len(matrix[0])
memo = [[0] * cols for _ in range(rows)]
```

`memo[i][j]` = longest path starting from cell (i, j).
- `0` means not computed yet.

---

### 3. DFS function

```python
def dfs(r, c):
    if memo[r][c]:          # Already computed?
        return memo[r][c]   # Return cached result
```

**Memoization:** Avoid recomputing the same cell.

---

### 4. Four directions

```python
directions = [(0,1), (1,0), (0,-1), (-1,0)]
#             right   down   left    up
```

---

### 5. Explore neighbors

```python
max_length = 1  # At minimum, the cell itself

for dr, dc in directions:
    nr, nc = r + dr, c + dc  # New position

    if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
        length = 1 + dfs(nr, nc)
        max_length = max(max_length, length)
```

**Three conditions to move:**
1. `0 <= nr < rows` → within vertical bounds
2. `0 <= nc < cols` → within horizontal bounds
3. `matrix[nr][nc] > matrix[r][c]` → next cell is **strictly greater**

---

### 6. Cache and return

```python
memo[r][c] = max_length
return max_length
```

Store result to avoid recomputation.

---

### 7. Try all starting points

```python
longest_path = 0
for i in range(rows):
    for j in range(cols):
        longest_path = max(longest_path, dfs(i, j))
return longest_path
```

The longest path could start from any cell.

---

## Visualization

```
Matrix:                    Memo (after computation):
┌───┬───┬───┐             ┌───┬───┬───┐
│ 9 │ 9 │ 4 │             │ 4 │ 1 │ 2 │
├───┼───┼───┤             ├───┼───┼───┤
│ 6 │ 6 │ 8 │             │ 3 │ 2 │ 1 │
├───┼───┼───┤             ├───┼───┼───┤
│ 2 │ 1 │ 1 │             │ 2 │ 1 │ 1 │
└───┴───┴───┘             └───┴───┴───┘

Path: (2,1)=1 → (2,0)=2 → (1,0)=6 → (0,0)=9
      memo=1    memo=2    memo=3    memo=4
```

---

## Why Memoization?

Without memoization:
```
dfs(0,0) calls dfs(1,0)
dfs(0,1) calls dfs(1,0)  ← Same computation!
dfs(1,1) calls dfs(1,0)  ← Again!
```

With memoization: computed once, reused everywhere.

---

## Python Syntax to Remember

### 1. Create 2D array

```python
# Correct way
memo = [[0] * cols for _ in range(rows)]

# WRONG way (all rows share same list!)
memo = [[0] * cols] * rows
```

### 2. Tuple unpacking in loop

```python
directions = [(0,1), (1,0), (0,-1), (-1,0)]
for dr, dc in directions:
    nr, nc = r + dr, c + dc
```

### 3. Bounds checking

```python
if 0 <= nr < rows and 0 <= nc < cols:
    # Valid position
```

### 4. Nested function (closure)

```python
def outer():
    rows, cols = 3, 3
    memo = [[0] * cols for _ in range(rows)]

    def inner(r, c):
        # Can access rows, cols, memo from outer scope
        return memo[r][c]

    return inner(0, 0)
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(m × n) | Each cell computed once due to memoization |
| **Space** | O(m × n) | Memo table + recursion stack |

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  FOR EACH CELL (i, j)               │
│                                     │
│  dfs(i, j):                         │
│    Already in memo? → return it     │
│                                     │
│    For each direction:              │
│      Valid move? (bounds + greater) │
│      YES → 1 + dfs(neighbor)        │
│                                     │
│    Save max in memo[i][j]           │
│    Return max                       │
└─────────────────────────────────────┘
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `[[0]*cols]*rows` | All rows share same list | Use list comprehension |
| Forgetting `> matrix[r][c]` | Allows equal values | Must be strictly greater |
| Not checking memo first | Timeout (recomputation) | Check `if memo[r][c]` |
| Starting from only one cell | Misses longest path | Try all cells |

---

## Alternative: Topological Sort

For advanced interviews, you can mention:
1. Build a directed graph (edges from smaller to larger neighbors)
2. Use topological sort
3. Time: O(m × n), same as DFS+memo

---

## Keywords for Interview

- "DFS with memoization"
- "Dynamic programming on grid"
- "Top-down approach"
- "Four-directional movement"
- "Strictly increasing constraint"
