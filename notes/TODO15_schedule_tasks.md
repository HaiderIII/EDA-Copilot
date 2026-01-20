# TODO 15: Design Task Scheduler (Topological Sort)

## The Problem

Given tasks with dependencies, return a valid execution order. If a cycle exists (impossible to schedule), return empty list.

```
Example:
    tasks = ["A", "B", "C"]
    dependencies = [("A", "B"), ("B", "C")]

    Meaning: A must run before B, B must run before C
    Output: ["A", "B", "C"]
```

**CAD Context:** EDA tool job scheduling, build systems, dependency resolution in netlists.

---

## Solution: Kahn's Algorithm (BFS Topological Sort)

```python
from collections import defaultdict, deque

def schedule_tasks(tasks: list, dependencies: list) -> list:
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = {task: 0 for task in tasks}

    for parent, child in dependencies:
        graph[parent].append(child)
        in_degree[child] += 1

    # Start with tasks that have no dependencies
    queue = deque([task for task in tasks if in_degree[task] == 0])
    result = []

    while queue:
        current = queue.popleft()
        result.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all tasks were scheduled
    return result if len(result) == len(tasks) else []
```

---

## Step-by-Step Explanation

### 1. Build the dependency graph

```python
graph = defaultdict(list)
in_degree = {task: 0 for task in tasks}

for parent, child in dependencies:
    graph[parent].append(child)
    in_degree[child] += 1
```

**`graph[parent]`** = list of tasks that depend on parent
**`in_degree[task]`** = number of tasks that must run before this task

---

### 2. Find starting points

```python
queue = deque([task for task in tasks if in_degree[task] == 0])
```

Tasks with `in_degree = 0` have no dependencies → can run first.

---

### 3. Process tasks (BFS)

```python
while queue:
    current = queue.popleft()
    result.append(current)

    for neighbor in graph[current]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
```

- Take a task from queue
- Add to result
- "Complete" this task by reducing dependents' in-degree
- If dependent now has 0 in-degree, it's ready

---

### 4. Check for cycles

```python
return result if len(result) == len(tasks) else []
```

If we couldn't schedule all tasks, there's a cycle.

---

## Visualization

```
tasks = ["A", "B", "C", "D"]
dependencies = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]

Dependency Graph:
    A ──→ B
    │     │
    ▼     ▼
    C ──→ D

In-degree:
    A: 0 (no dependencies)
    B: 1 (depends on A)
    C: 1 (depends on A)
    D: 2 (depends on B and C)

Step 1: queue = [A] (only A has in_degree=0)
        result = []

Step 2: Process A
        result = ["A"]
        Reduce: in_degree[B] = 0, in_degree[C] = 0
        queue = [B, C]

Step 3: Process B
        result = ["A", "B"]
        Reduce: in_degree[D] = 1
        queue = [C]

Step 4: Process C
        result = ["A", "B", "C"]
        Reduce: in_degree[D] = 0
        queue = [D]

Step 5: Process D
        result = ["A", "B", "C", "D"]
        queue = []

Final: ["A", "B", "C", "D"]
```

---

## Python Syntax to Remember

### 1. `defaultdict(list)` - Auto-create empty lists

```python
from collections import defaultdict

graph = defaultdict(list)
graph["A"].append("B")  # No KeyError if "A" doesn't exist
graph["A"].append("C")
# graph = {"A": ["B", "C"]}
```

### 2. `deque` - Efficient queue

```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)      # Add to right: [1, 2, 3, 4]
queue.popleft()      # Remove from left: [2, 3, 4], returns 1
queue.appendleft(0)  # Add to left: [0, 2, 3, 4]
```

### 3. Dictionary comprehension

```python
tasks = ["A", "B", "C"]
in_degree = {task: 0 for task in tasks}
# {"A": 0, "B": 0, "C": 0}
```

### 4. Tuple unpacking in loop

```python
dependencies = [("A", "B"), ("B", "C")]
for parent, child in dependencies:
    print(f"{parent} → {child}")
# A → B
# B → C
```

### 5. List comprehension with condition

```python
tasks = ["A", "B", "C"]
in_degree = {"A": 0, "B": 1, "C": 0}

ready = [task for task in tasks if in_degree[task] == 0]
# ["A", "C"]
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  TOPOLOGICAL SORT (Kahn's)          │
│                                     │
│  1. BUILD GRAPH                     │
│     - graph[parent] = [children]    │
│     - in_degree[task] = count       │
│                                     │
│  2. INITIALIZE                      │
│     - queue = tasks with in_deg=0   │
│                                     │
│  3. PROCESS (BFS)                   │
│     while queue:                    │
│       - pop task → add to result    │
│       - reduce children's in_degree │
│       - if child's in_deg=0 → queue │
│                                     │
│  4. CHECK CYCLE                     │
│     - len(result) == len(tasks)?    │
└─────────────────────────────────────┘
```

---

## Why Topological Sort?

```
Problem: Given dependencies, find valid order

     A ──→ B ──→ C

Can't start B until A is done.
Can't start C until B is done.

Topological sort gives: A, B, C

This is the foundation of:
- Build systems (Makefile)
- Package managers (npm, pip)
- EDA tool scheduling
- Database migration ordering
```

---

## Detecting Cycles

```
Cycle example:
    A ──→ B
    ↑     │
    └─────┘

    A depends on B, B depends on A → IMPOSSIBLE!

In our algorithm:
    in_degree = {A: 1, B: 1}
    queue = [] (no task has in_degree=0)
    result = []
    len(result) != len(tasks) → return []
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(V + E) | V = tasks, E = dependencies |
| **Space** | O(V + E) | Graph storage |

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Using list instead of deque | O(n) for pop(0) | Use deque.popleft() |
| Forgetting to initialize in_degree | KeyError | Create dict for all tasks first |
| Not checking for cycles | Wrong result for impossible cases | Check `len(result) == len(tasks)` |
| Using regular dict for graph | KeyError on access | Use defaultdict(list) |

---

## CAD Application Example

```python
# EDA Build Flow
tasks = ["synthesis", "placement", "routing", "timing", "signoff"]
dependencies = [
    ("synthesis", "placement"),
    ("placement", "routing"),
    ("routing", "timing"),
    ("timing", "signoff")
]

order = schedule_tasks(tasks, dependencies)
# ["synthesis", "placement", "routing", "timing", "signoff"]

for task in order:
    run_eda_tool(task)
```

---

## Keywords for Interview

- "Topological sort"
- "Kahn's algorithm"
- "Dependency resolution"
- "In-degree counting"
- "Cycle detection"
- "Directed Acyclic Graph (DAG)"
- "BFS-based approach"
