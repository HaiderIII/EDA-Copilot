# Sorting Algorithms - Complete Guide

## Overview

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable? |
|-----------|-------------|------------|--------------|-------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |

**Stable** = Equal elements maintain their relative order.

---

## 1. Bubble Sort

### Concept
Compare adjacent elements and swap if in wrong order. Largest element "bubbles up" to the end.

### Code
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Optimization: stop if already sorted
            break
    return arr
```

### Visualization
```
[64, 34, 25, 12]

Pass 1: Compare adjacent pairs
  64 > 34 → swap → [34, 64, 25, 12]
  64 > 25 → swap → [34, 25, 64, 12]
  64 > 12 → swap → [34, 25, 12, 64]  ← 64 bubbled to end

Pass 2:
  34 > 25 → swap → [25, 34, 12, 64]
  34 > 12 → swap → [25, 12, 34, 64]

Pass 3:
  25 > 12 → swap → [12, 25, 34, 64]

Done: [12, 25, 34, 64]
```

### Key Points
- Simple to understand and implement
- O(n) best case when array is already sorted (with `swapped` optimization)
- Rarely used in practice due to O(n²) average case

---

## 2. Selection Sort

### Concept
Find minimum element in unsorted part, swap it with first unsorted element.

### Code
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

### Visualization
```
[64, 25, 12, 22]

Pass 1: Find min in [64, 25, 12, 22] → 12 at index 2
        Swap arr[0] and arr[2]
        [12, 25, 64, 22]

Pass 2: Find min in [25, 64, 22] → 22 at index 3
        Swap arr[1] and arr[3]
        [12, 22, 64, 25]

Pass 3: Find min in [64, 25] → 25 at index 3
        Swap arr[2] and arr[3]
        [12, 22, 25, 64]

Done: [12, 22, 25, 64]
```

### Key Points
- Always O(n²) - no best case optimization
- Minimizes number of swaps (exactly n-1 swaps)
- Not stable (can change order of equal elements)

---

## 3. Insertion Sort

### Concept
Build sorted array one element at a time. Take each element and insert it into its correct position in the sorted part.

### Code
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

### Visualization
```
[12, 11, 13, 5]

i=1: key=11, sorted=[12]
     11 < 12 → shift 12 right → [12, 12, 13, 5]
     Insert 11 → [11, 12, 13, 5]

i=2: key=13, sorted=[11, 12]
     13 > 12 → no shift needed
     [11, 12, 13, 5]

i=3: key=5, sorted=[11, 12, 13]
     5 < 13 → shift → [11, 12, 13, 13]
     5 < 12 → shift → [11, 12, 12, 13]
     5 < 11 → shift → [11, 11, 12, 13]
     Insert 5 → [5, 11, 12, 13]

Done: [5, 11, 12, 13]
```

### Key Points
- O(n) for nearly sorted arrays - very efficient!
- Stable sort
- Good for small arrays (used in hybrid algorithms)
- Works well for online sorting (sorting as data arrives)

---

## 4. Merge Sort

### Concept
Divide array in half, recursively sort each half, merge sorted halves.

### Code
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### Visualization
```
[38, 27, 43, 3]

Divide:
         [38, 27, 43, 3]
        /               \
    [38, 27]          [43, 3]
    /      \          /      \
  [38]    [27]      [43]    [3]

Merge:
  [38] + [27] → [27, 38]
  [43] + [3]  → [3, 43]
  [27, 38] + [3, 43] → [3, 27, 38, 43]
```

### Merge Process Detail
```
left = [27, 38], right = [3, 43]

i=0, j=0: 27 vs 3 → 3 smaller → result=[3], j=1
i=0, j=1: 27 vs 43 → 27 smaller → result=[3,27], i=1
i=1, j=1: 38 vs 43 → 38 smaller → result=[3,27,38], i=2
i=2: left exhausted → extend with right[1:] → result=[3,27,38,43]
```

### Key Points
- Guaranteed O(n log n) - no worst case degradation
- Stable sort
- Requires O(n) extra space
- Good for linked lists (no random access needed)
- Used for external sorting (sorting data on disk)

---

## 5. Quick Sort

### Concept
Choose a pivot, partition array so elements < pivot are left, elements > pivot are right. Recursively sort partitions.

### Code (Simple Version)
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)
```

### Code (In-Place Version)
```python
def quick_sort_inplace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### Visualization
```
[10, 7, 8, 9, 1, 5]   pivot = 8

Partition:
  Elements < 8: [7, 1, 5]
  Elements = 8: [8]
  Elements > 8: [10, 9]

Recursively sort [7, 1, 5] and [10, 9]

[1, 5, 7] + [8] + [9, 10] = [1, 5, 7, 8, 9, 10]
```

### Key Points
- Average O(n log n), but O(n²) worst case (already sorted + bad pivot)
- In-place version uses O(log n) space for recursion
- Not stable
- Fastest in practice for most cases
- Pivot selection is crucial (median-of-three is common)

---

## 6. Heap Sort

### Concept
Build a max heap from the array, then repeatedly extract the maximum.

### Code
```python
def heap_sort(arr):
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

### Heap Structure
```
Array: [12, 11, 13, 5, 6, 7]

As tree:
         12(0)
        /     \
     11(1)    13(2)
     /   \    /
   5(3) 6(4) 7(5)

Index formulas:
  Parent of i: (i - 1) // 2
  Left child of i: 2 * i + 1
  Right child of i: 2 * i + 2
```

### Key Points
- Guaranteed O(n log n)
- In-place (O(1) space)
- Not stable
- Good when you need guaranteed performance
- Useful for finding k largest/smallest elements

---

## 7. Counting Sort

### Concept
Count occurrences of each value, then reconstruct sorted array from counts.

### Code
```python
def counting_sort(arr):
    if not arr:
        return arr

    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1

    count = [0] * range_size

    # Count occurrences
    for num in arr:
        count[num - min_val] += 1

    # Reconstruct array
    result = []
    for i, c in enumerate(count):
        result.extend([i + min_val] * c)

    return result
```

### Visualization
```
arr = [4, 2, 2, 8, 3, 3, 1]

min=1, max=8, range=8

Count array (index = value - min):
  index: 0  1  2  3  4  5  6  7
  value: 1  2  3  4  5  6  7  8
  count: 1  2  2  1  0  0  0  1

Reconstruct:
  1 appears 1 time  → [1]
  2 appears 2 times → [1, 2, 2]
  3 appears 2 times → [1, 2, 2, 3, 3]
  4 appears 1 time  → [1, 2, 2, 3, 3, 4]
  8 appears 1 time  → [1, 2, 2, 3, 3, 4, 8]
```

### Key Points
- O(n + k) where k is range of values
- Only works for integers!
- Very fast when k is small relative to n
- Stable (with proper implementation)
- Used as subroutine in Radix Sort

---

## 8. Python Built-in Sort

### Timsort
Python uses Timsort (hybrid of merge sort and insertion sort).

```python
# Returns new sorted list
sorted_list = sorted(arr)

# Sorts in place
arr.sort()

# Custom key function
sorted(arr, key=abs)           # Sort by absolute value
sorted(arr, key=lambda x: -x)  # Descending
sorted(arr, reverse=True)      # Descending

# Sort objects by attribute
students.sort(key=lambda s: s.grade)

# Multiple criteria
students.sort(key=lambda s: (s.grade, s.name))
```

### Key Points
- Always use built-in for production code
- O(n log n) guaranteed
- Stable
- Highly optimized for real-world data

---

## When to Use What?

| Situation | Best Algorithm |
|-----------|----------------|
| Small array (n < 50) | Insertion Sort |
| Nearly sorted | Insertion Sort |
| Need guaranteed O(n log n) | Merge Sort or Heap Sort |
| Average case performance | Quick Sort |
| Limited memory | Heap Sort |
| Integers in small range | Counting Sort |
| Production code | Python `sorted()` |
| Stability required | Merge Sort |

---

## Common Interview Questions

1. **"Implement merge sort"** - Know the divide-conquer-merge pattern
2. **"Why is quick sort faster than merge sort in practice?"** - Cache efficiency, in-place
3. **"When would insertion sort beat quick sort?"** - Small or nearly sorted arrays
4. **"What's the difference between stable and unstable sort?"** - Equal elements order
5. **"How does heap sort work?"** - Build max heap, extract max repeatedly

---

## Python Syntax Reminders

### Swap two elements
```python
arr[i], arr[j] = arr[j], arr[i]
```

### List slicing
```python
arr[:mid]   # First half
arr[mid:]   # Second half
```

### List comprehension
```python
left = [x for x in arr if x < pivot]
```

### Extend list
```python
result.extend([1, 2, 3])  # Add multiple elements
```

### Range backwards
```python
for i in range(n - 1, -1, -1):  # n-1, n-2, ..., 0
```
