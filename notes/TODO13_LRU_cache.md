# TODO 13: LRU Cache Implementation

## The Problem

**LRU = Least Recently Used**

Design a cache with limited capacity. When full, evict the item that hasn't been used for the longest time.

```
Example:
    cache = LRUCache(2)  # capacity = 2
    cache.put(1, 1)      # cache: {1:1}
    cache.put(2, 2)      # cache: {1:1, 2:2}
    cache.get(1)         # returns 1, marks 1 as recently used
    cache.put(3, 3)      # cache full! evicts 2 (least recently used)
                         # cache: {1:1, 3:3}
    cache.get(2)         # returns -1 (not found)
```

**CAD Context:** Caching simulation results, synthesis data, or parsed netlists to avoid recomputation.

---

## Solution 1: Using dict + list (Your approach)

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}      # key → value
        self.order = []      # tracks usage order (oldest first)

    def get(self, key: int) -> int:
        if key in self.cache:
            self.order.remove(key)   # Remove from current position
            self.order.append(key)   # Add to end (most recent)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)   # Update position
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)  # Remove oldest
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)  # Add to end (most recent)
```

**Complexity:** O(n) for get and put (because `list.remove()` is O(n))

---

## Solution 2: Using OrderedDict (Optimal)

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key in self.cache:
            self.cache.move_to_end(key)  # O(1)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Remove oldest, O(1)
        self.cache[key] = value
```

**Complexity:** O(1) for get and put

---

## Step-by-Step Visualization

```
LRUCache(capacity=2)

Operation       | cache          | order        | Action
----------------|----------------|--------------|------------------
put(1, 1)       | {1:1}          | [1]          | Add 1
put(2, 2)       | {1:1, 2:2}     | [1, 2]       | Add 2
get(1) → 1      | {1:1, 2:2}     | [2, 1]       | Move 1 to end
put(3, 3)       | {1:1, 3:3}     | [1, 3]       | Evict 2, add 3
get(2) → -1     | {1:1, 3:3}     | [1, 3]       | Not found
```

---

## Key Data Structures

### dict + list approach

```
cache = {1: "A", 2: "B", 3: "C"}   # Fast lookup O(1)
order = [1, 2, 3]                   # Tracks order (oldest → newest)
         ↑        ↑
      oldest   newest
```

### OrderedDict approach

```python
from collections import OrderedDict

cache = OrderedDict()
cache[1] = "A"
cache[2] = "B"

cache.move_to_end(1)        # Move key 1 to end (most recent)
cache.popitem(last=False)   # Remove first item (oldest)
```

---

## Python Syntax to Remember

### 1. `list.remove(value)` - Remove by value

```python
order = [1, 2, 3]
order.remove(2)   # order = [1, 3]
# Note: O(n) complexity!
```

### 2. `list.pop(index)` - Remove by index

```python
order = [1, 2, 3]
oldest = order.pop(0)   # oldest = 1, order = [2, 3]
```

### 3. `del dict[key]` - Delete from dictionary

```python
cache = {1: "A", 2: "B"}
del cache[1]   # cache = {2: "B"}
```

### 4. `OrderedDict.move_to_end(key)`

```python
from collections import OrderedDict
cache = OrderedDict([(1, "A"), (2, "B")])
cache.move_to_end(1)   # Now: [(2, "B"), (1, "A")]
```

### 5. `OrderedDict.popitem(last=False)`

```python
cache = OrderedDict([(1, "A"), (2, "B")])
cache.popitem(last=False)  # Removes (1, "A"), oldest
cache.popitem(last=True)   # Removes last, newest
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  GET(key)                           │
│                                     │
│  key exists?                        │
│  ├─ YES → move to end (recent)      │
│  │        return value              │
│  └─ NO  → return -1                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  PUT(key, value)                    │
│                                     │
│  key exists?                        │
│  ├─ YES → update position           │
│  └─ NO  → cache full?               │
│           ├─ YES → evict oldest     │
│           └─ NO  → just add         │
│  Add key to end (most recent)       │
│  Set cache[key] = value             │
└─────────────────────────────────────┘
```

---

## Complexity Comparison

| Approach | get() | put() |
|----------|-------|-------|
| dict + list | O(n) | O(n) |
| OrderedDict | O(1) | O(1) |
| dict + doubly linked list | O(1) | O(1) |

---

## Interview Tips

1. **Start with the simple approach** (dict + list) to show understanding
2. **Mention the complexity** issue with `list.remove()`
3. **Propose optimization** with `OrderedDict`
4. **Know the trade-offs**:
   - dict + list: Simple but O(n)
   - OrderedDict: O(1) but uses Python built-in
   - Doubly linked list: O(1), shows low-level understanding

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting to update order on `get()` | LRU order incorrect | Always move to end on access |
| Not handling existing key in `put()` | Duplicate keys | Check `if key in cache` first |
| Using `list.pop()` without index | Removes last, not first | Use `pop(0)` for oldest |

---

## Real CAD Application

```python
# Cache simulation results
sim_cache = LRUCache(100)

def simulate(netlist_id, params):
    cache_key = f"{netlist_id}_{params}"
    result = sim_cache.get(cache_key)
    if result != -1:
        return result  # Cache hit!

    # Cache miss - run simulation
    result = run_expensive_simulation(netlist_id, params)
    sim_cache.put(cache_key, result)
    return result
```

---

## Keywords for Interview

- "LRU Cache"
- "Least Recently Used"
- "Cache eviction policy"
- "OrderedDict"
- "O(1) get and put operations"
- "Doubly linked list + hash map"
