# TODO 10: Run Shell Command and Parse Output

## The Problem

Use Python's `subprocess` module to run a shell command and return the output as a list of lines.

```
Example:
    run_command("echo hello")
    Output: ["hello"]

    run_command("ls -la")
    Output: ["total 8", "-rw-r--r-- 1 user ...", ...]
```

**CAD Context:** Running EDA tools (synthesis, simulation), executing scripts, automation workflows.

---

## Solution

```python
import subprocess

def run_command(cmd: str) -> list:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip().splitlines()
```

---

## Step-by-Step Explanation

### 1. Import subprocess

```python
import subprocess
```

The `subprocess` module allows running external commands from Python.

---

### 2. Run the command

```python
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
```

**Parameters explained:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `cmd` | `"echo hello"` | The command to run |
| `shell=True` | Execute through shell | Allows shell features (pipes, wildcards) |
| `capture_output=True` | Capture stdout/stderr | Instead of printing to terminal |
| `text=True` | Return as string | Instead of bytes |

---

### 3. Process the output

```python
result.stdout.strip().splitlines()
```

- `result.stdout` → The command's output as string
- `.strip()` → Remove leading/trailing whitespace
- `.splitlines()` → Split into list of lines

---

## The `result` Object

```python
result = subprocess.run("echo hello", shell=True, capture_output=True, text=True)

result.stdout       # → "hello\n" (standard output)
result.stderr       # → "" (error output)
result.returncode   # → 0 (exit code, 0 = success)
```

---

## Visualization

```
┌─────────────────────────────────────┐
│  Python                             │
│                                     │
│  subprocess.run("ls -la")           │
│         │                           │
│         ▼                           │
│  ┌─────────────────┐                │
│  │  Shell (bash)   │                │
│  │  Executes: ls   │                │
│  └─────────────────┘                │
│         │                           │
│         ▼                           │
│  stdout: "file1.txt\nfile2.txt"     │
│                                     │
│         │                           │
│         ▼                           │
│  .strip().splitlines()              │
│  → ["file1.txt", "file2.txt"]       │
└─────────────────────────────────────┘
```

---

## Python Syntax to Remember

### 1. `subprocess.run()` - Basic command execution

```python
import subprocess

# Simple command
subprocess.run("echo hello", shell=True)

# Capture output
result = subprocess.run("echo hello", shell=True, capture_output=True, text=True)
print(result.stdout)  # → "hello\n"
```

### 2. `str.strip()` - Remove whitespace

```python
"  hello  \n".strip()  # → "hello"
```

### 3. `str.splitlines()` - Split by newlines

```python
"line1\nline2\nline3".splitlines()  # → ["line1", "line2", "line3"]

# Different from split("\n"):
"line1\nline2\n".split("\n")       # → ["line1", "line2", ""]
"line1\nline2\n".splitlines()       # → ["line1", "line2"] (cleaner!)
```

### 4. Check return code

```python
result = subprocess.run("ls nonexistent", shell=True, capture_output=True, text=True)
if result.returncode != 0:
    print(f"Error: {result.stderr}")
```

---

## Common Use Cases in CAD

### Run synthesis tool

```python
def run_synthesis(design_file):
    cmd = f"dc_shell -f {design_file}"
    result = run_command(cmd)
    return result
```

### Run simulation

```python
def run_simulation(testbench):
    cmd = f"vcs -full64 {testbench} && ./simv"
    return run_command(cmd)
```

### Get file list

```python
def get_verilog_files(directory):
    cmd = f"ls {directory}/*.v"
    return run_command(cmd)
```

---

## Alternative: Without shell=True (Safer)

```python
import subprocess

def run_command_safe(cmd_list: list) -> list:
    result = subprocess.run(cmd_list, capture_output=True, text=True)
    return result.stdout.strip().splitlines()

# Usage:
run_command_safe(["ls", "-la"])     # ✓ Safer
run_command_safe(["echo", "hello"]) # ✓ Safer

# shell=True is needed for:
# - Pipes: "ls | grep foo"
# - Wildcards: "ls *.v"
# - Shell built-ins
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  RUN SHELL COMMAND                  │
│                                     │
│  1. Import subprocess               │
│                                     │
│  2. subprocess.run() with:          │
│     - shell=True (if needed)        │
│     - capture_output=True           │
│     - text=True                     │
│                                     │
│  3. Process result:                 │
│     - result.stdout → output        │
│     - result.stderr → errors        │
│     - result.returncode → exit code │
│                                     │
│  4. Clean up:                       │
│     - .strip() → remove whitespace  │
│     - .splitlines() → list of lines │
└─────────────────────────────────────┘
```

---

## Error Handling

```python
def run_command_with_error(cmd: str) -> dict:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {
        "stdout": result.stdout.strip().splitlines(),
        "stderr": result.stderr.strip().splitlines(),
        "success": result.returncode == 0
    }

# Usage:
output = run_command_with_error("ls nonexistent")
if not output["success"]:
    print("Command failed:", output["stderr"])
```

---

## Complexity

| | Value | Explanation |
|--|-------|-------------|
| **Time** | O(n) | Processing output lines |
| **Space** | O(n) | Storing output |

Note: Actual time depends on the command being run.

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Forgetting `capture_output=True` | Output goes to terminal | Add `capture_output=True` |
| Forgetting `text=True` | Returns bytes, not string | Add `text=True` |
| Not checking `returncode` | Ignoring errors | Check `result.returncode` |
| Using `split("\n")` | Empty string at end | Use `splitlines()` |

---

## Keywords for Interview

- "subprocess module"
- "Shell command execution"
- "capture_output for stdout/stderr"
- "text=True for string output"
- "Return code checking"
- "Process automation"
