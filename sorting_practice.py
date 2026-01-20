"""
Sorting Algorithms - Python Interview Practice
===============================================
Essential sorting algorithms for technical interviews.

How to use:
1. Work through each TODO one by one
2. Implement the sorting algorithm
3. Run the tests to check your answer
4. Study the notes for detailed explanations

Difficulty levels:
    [EASY]   - Basic, must know
    [MEDIUM] - Common interview questions
    [HARD]   - Advanced, shows deep understanding
"""

# =============================================================================
# TODO 1 [EASY] - Bubble Sort
# =============================================================================
# The simplest sorting algorithm. Compare adjacent elements and swap if needed.
# Repeat until no swaps are needed.
#
# Example: [64, 34, 25, 12] → [12, 25, 34, 64]
#
# Time: O(n²) | Space: O(1)

def bubble_sort(arr: list) -> list:
    """Sort array using bubble sort algorithm."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


# =============================================================================
# TODO 2 [EASY] - Selection Sort
# =============================================================================
# Find the minimum element and put it at the beginning. Repeat for remaining.
#
# Example: [64, 25, 12, 22] → [12, 22, 25, 64]
#
# Time: O(n²) | Space: O(1)

def selection_sort(arr: list) -> list:
    """Sort array using selection sort algorithm."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# =============================================================================
# TODO 3 [EASY] - Insertion Sort
# =============================================================================
# Build sorted array one element at a time by inserting each element
# into its correct position.
#
# Example: [12, 11, 13, 5] → [5, 11, 12, 13]
#
# Time: O(n²) | Space: O(1)
# Note: Efficient for small or nearly sorted arrays!

def insertion_sort(arr: list) -> list:
    """Sort array using insertion sort algorithm."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# =============================================================================
# TODO 4 [MEDIUM] - Merge Sort
# =============================================================================
# Divide array in half, sort each half, then merge the sorted halves.
# Classic divide-and-conquer algorithm.
#
# Example: [38, 27, 43, 3, 9, 82, 10] → [3, 9, 10, 27, 38, 43, 82]
#
# Time: O(n log n) | Space: O(n)

def merge_sort(arr: list) -> list:
    """Sort array using merge sort algorithm."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: list, right: list) -> list:
    """Merge two sorted arrays into one sorted array."""
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


# =============================================================================
# TODO 5 [MEDIUM] - Quick Sort
# =============================================================================
# Choose a pivot, partition array around pivot, recursively sort partitions.
# Most commonly used sorting algorithm in practice.
#
# Example: [10, 7, 8, 9, 1, 5] → [1, 5, 7, 8, 9, 10]
#
# Time: O(n log n) average, O(n²) worst | Space: O(log n)

def quick_sort(arr: list) -> list:
    """Sort array using quick sort algorithm."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# =============================================================================
# TODO 6 [MEDIUM] - Quick Sort (In-Place)
# =============================================================================
# Same as quick sort but without extra space for new arrays.
# Uses partitioning with swaps.
#
# Time: O(n log n) average | Space: O(log n) for recursion stack

def quick_sort_inplace(arr: list, low: int = None, high: int = None) -> list:
    """Sort array using in-place quick sort algorithm."""
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

    return arr


def partition(arr: list, low: int, high: int) -> int:
    """Partition array around pivot and return pivot index."""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# =============================================================================
# TODO 7 [HARD] - Heap Sort
# =============================================================================
# Build a max heap, then repeatedly extract the maximum element.
# Uses the heap data structure property.
#
# Example: [12, 11, 13, 5, 6, 7] → [5, 6, 7, 11, 12, 13]
#
# Time: O(n log n) | Space: O(1)

def heap_sort(arr: list) -> list:
    """Sort array using heap sort algorithm."""
    n = len(arr)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

    return arr


def heapify(arr: list, n: int, i: int) -> None:
    """Maintain heap property for subtree rooted at index i."""
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


# =============================================================================
# TODO 8 [MEDIUM] - Counting Sort
# =============================================================================
# Count occurrences of each element, then reconstruct sorted array.
# Only works for integers in a known range!
#
# Example: [4, 2, 2, 8, 3, 3, 1] → [1, 2, 2, 3, 3, 4, 8]
#
# Time: O(n + k) where k is range | Space: O(k)

def counting_sort(arr: list) -> list:
    """Sort array using counting sort algorithm."""
    if not arr:
        return arr

    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1

    count = [0] * range_size
    output = [0] * len(arr)

    # Count occurrences
    for num in arr:
        count[num - min_val] += 1

    # Cumulative count
    for i in range(1, range_size):
        count[i] += count[i - 1]

    # Build output array (traverse in reverse for stability)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output


# =============================================================================
# TODO 9 [EASY] - Python Built-in Sort
# =============================================================================
# Using Python's built-in sorting (Timsort algorithm).
# Know when to use built-in vs implementing your own!
#
# Time: O(n log n) | Space: O(n)

def python_sort(arr: list) -> list:
    """Sort array using Python's built-in sort."""
    return sorted(arr)  # Returns new list


def python_sort_inplace(arr: list) -> list:
    """Sort array in-place using Python's built-in sort."""
    arr.sort()  # Modifies original list
    return arr


# Custom sorting with key function
def sort_by_absolute(arr: list) -> list:
    """Sort array by absolute value."""
    return sorted(arr, key=abs)


def sort_descending(arr: list) -> list:
    """Sort array in descending order."""
    return sorted(arr, reverse=True)


# =============================================================================
# TESTS - Run to check your solutions
# =============================================================================

def run_tests():
    """Run all sorting tests."""
    print("=" * 60)
    print("SORTING ALGORITHMS - TEST RESULTS")
    print("=" * 60)

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 1, 4, 2, 8],
        [1],
        [],
        [3, 3, 3],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
    ]

    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Quick Sort In-Place", lambda arr: quick_sort_inplace(arr.copy())),
        ("Heap Sort", heap_sort),
        ("Counting Sort", counting_sort),
        ("Python Built-in", python_sort),
    ]

    for name, func in algorithms:
        print(f"\n[{name}]")
        try:
            all_passed = True
            for test in test_cases:
                arr_copy = test.copy()
                result = func(arr_copy)
                expected = sorted(test)
                if result != expected:
                    print(f"   FAILED: {test} → {result}, expected {expected}")
                    all_passed = False
            if all_passed:
                print("   PASSED")
        except Exception as e:
            print(f"   ERROR: {e}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
