"""
Apple CAD Engineer - Python Interview Practice
===============================================
Based on real Apple interview questions from Glassdoor and Educative.

How to use:
1. Work through each TODO one by one
2. Write your solution in the function
3. Run the tests to check your answer
4. Move to the next question

Difficulty levels:
    [EASY]   - Warm-up, basic Python
    [MEDIUM] - Typical Apple interview level
    [HARD]   - Advanced, shows strong skills
"""

# =============================================================================
# PART 1: STRING MANIPULATION (Common in CAD automation)
# =============================================================================

# TODO 1 [MEDIUM] - Longest Substring Without Repeating Characters
# Real Apple interview question!
# Example: "abcabcbb" -> 3 (answer is "abc")
# Example: "bbbbb" -> 1 (answer is "b")
# Example: "pwwkew" -> 3 (answer is "wke")
def longest_substring_no_repeat(s: str) -> int:
    """Find the length of the longest substring without repeating characters."""

    char_index = {}
    max_length = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length


# TODO 2 [EASY] - Reverse Words in a String
# Example: "the sky is blue" -> "blue is sky the"
# Example: "  hello world  " -> "world hello"
def reverse_words(s: str) -> str:
    """Reverse the order of words in a string."""
    words = s.strip().split()
    return ' '.join(reversed(words))


# TODO 3 [MEDIUM] - Find All Palindrome Substrings
# Example: "aab" -> ["a", "a", "b", "aa"]
# Example: "abc" -> ["a", "b", "c"]
def find_palindromes(s: str) -> list:
    """Find all palindrome substrings in a string."""
    palindromes = set()
    n = len(s)

    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if substring == substring[::-1]:
                palindromes.add(substring)

    return list(palindromes)



# =============================================================================
# PART 2: ARRAYS & DATA STRUCTURES (Important for EDA data processing)
# =============================================================================

# TODO 4 [EASY] - Two Sum
# Given an array and a target, return indices of two numbers that add up to target.
# Example: nums = [2, 7, 11, 15], target = 9 -> [0, 1]
def two_sum(nums: list, target: int) -> list:
    """Return indices of two numbers that add up to target."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):   # j commence après i
            if nums[i] + nums[j] == target:
                return [i, j]


# TODO 5 [MEDIUM] - Merge Overlapping Intervals
# Very useful for timing analysis in EDA!
# Example: [[1,3], [2,6], [8,10], [15,18]] -> [[1,6], [8,10], [15,18]]
def merge_intervals(intervals: list) -> list:
    if not intervals:
        return []
    
    # Étape 1: Trier
    intervals.sort()
    
    # Étape 2: Initialiser avec le premier intervalle
    result = [intervals[0]]
    
    # Étape 3: Parcourir les intervalles restants
    for current in intervals[1:]:
        last = result[-1]
        
        if current[0] <= last[1]:  # Chevauchement
            last[1] = max(last[1], current[1])  # Fusionner
        else:
            result.append(current)
    
    return result


                
    

# TODO 6 [MEDIUM] - Minimum Swaps to Group Colors
# Real Apple interview question!
# Given array of colors (R, B), find minimum swaps to group same colors together.
# Example: "RBRBRBB" -> 1 (swap position 1 and 5 to get "RRRBBBB")
def min_swaps_colors(colors: str) -> int:
    """Find minimum swaps to group all R on one side and all B on other side."""
    num_R = colors.count("R")
    num_B = colors.count("B")
    # Count misplaced R in first num_R positions
    swaps_R_left = sum(1 for i in range(num_R) if colors[i] == "B")
    # Count misplaced R in last num_R positions
    swaps_B_left = sum(1 for i in range(num_B) if colors[i] == "R")
    return min(swaps_R_left, swaps_B_left)


# =============================================================================
# PART 3: FILE PARSING & REGEX (Essential for CAD automation)
# =============================================================================

# TODO 7 [EASY] - Parse Key-Value Pairs
# Common in EDA config files!
# Example: "width=10 height=20 depth=5" -> {"width": "10", "height": "20", "depth": "5"}
def parse_key_value(s: str) -> dict:
    """Parse space-separated key=value pairs into a dictionary."""
    pairs = s.split()
    result = {}
    for pair in pairs:
        key, value = pair.split("="
                                )
        result[key] = value
    return result


# TODO 8 [MEDIUM] - Extract Timing Values from Log
# Parse timing report lines like EDA tools produce.
# Example: "Setup slack: -0.5ns | Hold slack: 0.2ns | Clock: clk_main"
# Return: {"setup_slack": -0.5, "hold_slack": 0.2, "clock": "clk_main"}
from collections import defaultdict, deque
import re

def parse_timing_report(line: str) -> dict:
    """Extract timing values from a timing report line."""
    
    # Pattern pour extraire: "Setup slack: -0.5ns"
    # Capture: (nom) : (valeur)
    
    setup = re.search(r"Setup slack:\s*(-?[\d.]+)ns", line)
    hold = re.search(r"Hold slack:\s*(-?[\d.]+)ns", line)
    clock = re.search(r"Clock:\s*(\w+)", line)
    
    return {
        "setup_slack": float(setup.group(1)),
        "hold_slack": float(hold.group(1)),
        "clock": clock.group(1)
    }



# TODO 9 [MEDIUM] - Find Cells in Netlist
# Parse a simple netlist format and extract cell instances.
# Example netlist:
#   .subckt inverter in out vdd vss
#   M1 out in vdd vdd pmos w=1u l=100n
#   M2 out in vss vss nmos w=500n l=100n
#   .ends
# Return: [{"name": "M1", "type": "pmos", "w": "1u", "l": "100n"},
#          {"name": "M2", "type": "nmos", "w": "500n", "l": "100n"}]
def parse_netlist_cells(netlist: str) -> list:
    """Extract cell information from a SPICE netlist."""
    component={}
    cell =[]
    for line in netlist.splitlines():
        match = re.search(r"(\w+)\s+.*?(pmos|nmos)\s+w=(\S+)\s+l=(\S+)", line)
        if match:
            component={
                "name": match.group(1),
                "type": match.group(2),
                "w": match.group(3),
                "l": match.group(4)
            }
            cell.append(component)
    return cell

    



# =============================================================================
# PART 4: AUTOMATION & SCRIPTING (Daily CAD work)
# =============================================================================

# TODO 10 [EASY] - Run Shell Command and Parse Output
# Use subprocess to run a command and return stdout as list of lines.
import subprocess

def run_command(cmd: str) -> list:
    """Run a shell command and return output as list of lines."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().splitlines()


# TODO 11 [MEDIUM] - Compare Two Files and Find Differences
# Compare two text files line by line, return differences.
# Return: {"only_in_file1": [...], "only_in_file2": [...], "different": [...]}
def compare_files(file1_lines: list, file2_lines: list) -> dict:
    """Compare two files and return differences."""
    only_in_file1 = []
    only_in_file2 = []
    different = []  
    len1 = len(file1_lines)
    len2 = len(file2_lines)
    max_len = max(len1, len2)
    for i in range(max_len):
        line1 = file1_lines[i] if i < len1 else None
        line2 = file2_lines[i] if i < len2 else None
        if line1 != line2:
            if line1 is not None and line2 is not None:
                different.append((line1, line2))
            elif line1 is not None:
                only_in_file1.append(line1)
            else:
                only_in_file2.append(line2)
    return {
        "only_in_file1": only_in_file1,
        "only_in_file2": only_in_file2,
        "different": different
    }


# TODO 12 [MEDIUM] - Batch Process Files with Pattern Matching
# Given a list of filenames, filter by pattern and apply transformation.
# Example: files = ["test1.v", "test2.v", "lib.sv", "data.txt"]
#          pattern = "*.v"
#          transform = lambda x: x.replace(".v", "_new.v")
# Return: ["test1_new.v", "test2_new.v"]
import fnmatch

def batch_process_files(files: list, pattern: str, transform) -> list:
    """Filter files by pattern and apply transformation."""
    matched_files = fnmatch.filter(files, pattern)
    return [transform(f) for f in matched_files]



# =============================================================================
# PART 5: DATA STRUCTURES & ALGORITHMS (LeetCode-style)
# =============================================================================

# TODO 13 [MEDIUM] - LRU Cache Implementation
# Design a data structure for Least Recently Used (LRU) cache.
# Used in EDA tools for caching simulation results!
class LRUCache:
    """
    Implement LRU Cache with get and put operations in O(1) time.

    Example:
        cache = LRUCache(2)  # capacity = 2
        cache.put(1, 1)
        cache.put(2, 2)
        cache.get(1)       # returns 1
        cache.put(3, 3)    # evicts key 2
        cache.get(2)       # returns -1 (not found)
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []

    def get(self, key: int) -> int:
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)


# TODO 14 [HARD] - Longest Increasing Path in Matrix
# Real Apple interview question!
# Given an m x n matrix, find the length of the longest increasing path.
# Example: [[9,9,4],[6,6,8],[2,1,1]] -> 4 (path: 1->2->6->9)
def longest_increasing_path(matrix: list) -> int:
    """Find the length of the longest increasing path in matrix."""
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


# TODO 15 [HARD] - Design Task Scheduler
# Simulate EDA tool job scheduling with dependencies.
# Given tasks with dependencies, return order of execution (or [] if impossible).
# Example: tasks = ["A", "B", "C"], deps = [("A", "B"), ("B", "C")]
# Means: A must run before B, B must run before C
# Return: ["A", "B", "C"]
def schedule_tasks(tasks: list, dependencies: list) -> list:
    """Return valid execution order for tasks with dependencies."""


    graph = defaultdict(list)
    in_degree = {task: 0 for task in tasks}

    for dep in dependencies:
        parent, child = dep
        graph[parent].append(child)
        in_degree[child] += 1

    queue = deque([task for task in tasks if in_degree[task] == 0])
    result = []

    while queue:
        current = queue.popleft()
        result.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(tasks) else []


# =============================================================================
# TESTS - Run to check your solutions
# =============================================================================

def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("PYTHON INTERVIEW PRACTICE - TEST RESULTS")
    print("=" * 60)

    # Test TODO 1
    print("\n[TODO 1] Longest Substring No Repeat:")
    try:
        assert longest_substring_no_repeat("abcabcbb") == 3, "Failed: abcabcbb"
        assert longest_substring_no_repeat("bbbbb") == 1, "Failed: bbbbb"
        assert longest_substring_no_repeat("pwwkew") == 3, "Failed: pwwkew"
        assert longest_substring_no_repeat("") == 0, "Failed: empty string"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 2
    print("\n[TODO 2] Reverse Words:")
    try:
        assert reverse_words("the sky is blue") == "blue is sky the"
        assert reverse_words("  hello world  ") == "world hello"
        assert reverse_words("a") == "a"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 3
    print("\n[TODO 3] Find Palindromes:")
    try:
        result = find_palindromes("aab")
        assert "aa" in result, "Missing 'aa'"
        assert "a" in result, "Missing 'a'"
        assert "b" in result, "Missing 'b'"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 4
    print("\n[TODO 4] Two Sum:")
    try:
        result = two_sum([2, 7, 11, 15], 9)
        assert sorted(result) == [0, 1], f"Expected [0,1], got {result}"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 5
    print("\n[TODO 5] Merge Intervals:")
    try:
        result = merge_intervals([[1,3], [2,6], [8,10], [15,18]])
        assert result == [[1,6], [8,10], [15,18]], f"Got {result}"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 6
    print("\n[TODO 6] Min Swaps Colors:")
    try:
        assert min_swaps_colors("RBRBRBB") == 1
        assert min_swaps_colors("RRRBBB") == 0
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 7
    print("\n[TODO 7] Parse Key-Value:")
    try:
        result = parse_key_value("width=10 height=20 depth=5")
        assert result == {"width": "10", "height": "20", "depth": "5"}
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 8
    print("\n[TODO 8] Parse Timing Report:")
    try:
        result = parse_timing_report("Setup slack: -0.5ns | Hold slack: 0.2ns | Clock: clk_main")
        assert result["setup_slack"] == -0.5
        assert result["hold_slack"] == 0.2
        assert result["clock"] == "clk_main"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 9
    print("\n[TODO 9] Parse Netlist:")
    try:
        netlist = """
        .subckt inverter in out vdd vss
        M1 out in vdd vdd pmos w=1u l=100n
        M2 out in vss vss nmos w=500n l=100n
        .ends
        """
        result = parse_netlist_cells(netlist)
        assert len(result) == 2
        assert result[0]["name"] == "M1"
        assert result[0]["type"] == "pmos"
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 10
    print("\n[TODO 10] Run Command:")
    try:
        result = run_command("echo hello")
        assert "hello" in result[0]
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 11
    print("\n[TODO 11] Compare Files:")
    try:
        file1 = ["line1", "line2", "line3"]
        file2 = ["line1", "line2_modified", "line4"]
        result = compare_files(file1, file2)
        assert "only_in_file1" in result
        assert "only_in_file2" in result
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 12
    print("\n[TODO 12] Batch Process Files:")
    try:
        files = ["test1.v", "test2.v", "lib.sv", "data.txt"]
        result = batch_process_files(files, "*.v", lambda x: x.replace(".v", "_new.v"))
        assert result == ["test1_new.v", "test2_new.v"]
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 13
    print("\n[TODO 13] LRU Cache:")
    try:
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)
        assert cache.get(2) == -1
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 14
    print("\n[TODO 14] Longest Increasing Path:")
    try:
        matrix = [[9,9,4],[6,6,8],[2,1,1]]
        assert longest_increasing_path(matrix) == 4
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    # Test TODO 15
    print("\n[TODO 15] Schedule Tasks:")
    try:
        result = schedule_tasks(["A", "B", "C"], [("A", "B"), ("B", "C")])
        assert result.index("A") < result.index("B") < result.index("C")
        print("   PASSED")
    except AssertionError as e:
        print(f"   FAILED: {e}")
    except:
        print("   NOT IMPLEMENTED")

    print("\n" + "=" * 60)
    print("Done! Keep practicing!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
