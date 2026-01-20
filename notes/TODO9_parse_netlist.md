# TODO 9: Parse Netlist (SPICE)

## The Problem

```
Input (SPICE netlist):
    .subckt inverter in out vdd vss
    M1 out in vdd vdd pmos w=1u l=100n
    M2 out in vss vss nmos w=500n l=100n
    .ends

Output:
    [{"name": "M1", "type": "pmos", "w": "1u", "l": "100n"},
     {"name": "M2", "type": "nmos", "w": "500n", "l": "100n"}]
```

**CAD Context:** Parse SPICE netlists to extract components (transistors, resistors, etc.)

---

## Anatomy of a SPICE Line

```
M1 out in vdd vdd pmos w=1u l=100n
│   │   │   │   │   │    │    │
│   │   │   │   │   │    │    └── Length
│   │   │   │   │   │    └── Width
│   │   │   │   │   └── Type (pmos/nmos)
│   │   │   │   └── Bulk
│   │   │   └── Source
│   │   └── Gate
│   └── Drain
└── Component name
```

---

## Reasoning

### What we want to capture
1. **Name:** `M1`, `M2`
2. **Type:** `pmos` or `nmos`
3. **Width (w):** `1u`, `500n`
4. **Length (l):** `100n`

### What we want to ignore
- Nodes: `out`, `in`, `vdd`, `vss`
- Lines `.subckt` and `.ends`

---

## The Regex Pattern

```python
r"(\w+)\s+.*?(pmos|nmos)\s+w=(\S+)\s+l=(\S+)"
```

### Breakdown

```
(\w+)       → Capture the name "M1"
\s+         → One or more spaces
.*?         → Anything (non-greedy) - SKIPS "out in vdd vdd"
(pmos|nmos) → Capture "pmos" or "nmos"
\s+         → Spaces
w=(\S+)     → "w=" then capture the value (anything except space)
\s+         → Spaces
l=(\S+)     → "l=" then capture the value
```

### Greedy vs Non-Greedy

| Pattern | Behavior | Example on "M1 out in vdd vdd pmos" |
|---------|----------|-------------------------------------|
| `.*` | **Greedy** - takes maximum | Matches everything up to the last possible "pmos" |
| `.*?` | **Non-greedy** - takes minimum | Stops at the first "pmos" found |

```python
# Why .*? and not .* ?
line = "M1 out in vdd vdd pmos w=1u"

r"(\w+)\s+.*(pmos)"    # .* eats everything → may match incorrectly
r"(\w+)\s+.*?(pmos)"   # .*? stops as soon as pmos is found ✓
```

---

## Final Code

```python
import re

def parse_netlist_cells(netlist: str) -> list:
    """Extract cell information from a SPICE netlist."""
    cells = []

    for line in netlist.splitlines():
        match = re.search(r"(\w+)\s+.*?(pmos|nmos)\s+w=(\S+)\s+l=(\S+)", line)
        if match:
            component = {
                "name": match.group(1),
                "type": match.group(2),
                "w": match.group(3),
                "l": match.group(4)
            }
            cells.append(component)

    return cells
```

---

## Python Syntax to Remember

### 1. `splitlines()` - Split by lines

```python
text = """line1
line2
line3"""

lines = text.splitlines()
# → ["line1", "line2", "line3"]

# Difference with split("\n"):
"a\nb\n".split("\n")      # → ["a", "b", ""] (empty element at end)
"a\nb\n".splitlines()     # → ["a", "b"] (no empty element)
```

### 2. `\S+` - Anything except space

```python
# \s = space, tab, newline
# \S = anything EXCEPT space (inverse of \s)

r"\S+"   # One or more non-space characters
# Matches: "1u", "100n", "abc123", "w=1u"
# Doesn't match: " ", "a b"
```

### 3. `.*?` - Non-greedy (minimal)

```python
text = "start XXX middle YYY end"

re.search(r"start(.*)end", text)    # .group(1) = " XXX middle YYY "
re.search(r"start(.*?)end", text)   # .group(1) = " XXX middle YYY "
# (same result here because only one "end")

text = "start XXX end YYY end"
re.search(r"start(.*)end", text)    # .group(1) = " XXX end YYY " (greedy)
re.search(r"start(.*?)end", text)   # .group(1) = " XXX " (non-greedy)
```

### 4. Build a list of dictionaries

```python
result = []

for item in items:
    d = {"key": value}
    result.append(d)

return result
```

---

## Mental Schema

```
┌─────────────────────────────────────┐
│  NETLIST (multi-line text)          │
└─────────────────┬───────────────────┘
                  │ splitlines()
                  ▼
┌─────────────────────────────────────┐
│  LIST OF LINES                      │
│  [".subckt...", "M1...", "M2..."]   │
└─────────────────┬───────────────────┘
                  │ for line in lines
                  ▼
┌─────────────────────────────────────┐
│  FOR EACH LINE                      │
│  re.search(pattern, line)           │
│                                     │
│  If match:                          │
│    Extract group(1), (2), (3), (4)  │
│    Create dictionary                │
│    Add to list                      │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│  LIST OF DICTIONARIES               │
│  [{"name":"M1",...}, {"name":"M2"}] │
└─────────────────────────────────────┘
```

---

## Useful SPICE Patterns

### MOS Transistors

```python
# MOSFET: Mxxx drain gate source bulk type [params]
r"^(M\w*)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(pmos|nmos)"
#   name   drain  gate  source bulk   type
```

### Resistors

```python
# R: Rxxx node1 node2 value
r"^(R\w*)\s+(\w+)\s+(\w+)\s+(\S+)"
#   name    n1     n2    value
```

### Capacitors

```python
# C: Cxxx node1 node2 value
r"^(C\w*)\s+(\w+)\s+(\w+)\s+(\S+)"
```

### Key=value parameters

```python
# Extract all parameters w=xxx l=xxx m=xxx
r"(\w+)=(\S+)"
# With findall: [("w", "1u"), ("l", "100n"), ("m", "2")]
```

---

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| `.*` instead of `.*?` | Too greedy, matches too much | Use `.*?` |
| Forgetting `if match:` | Error if no match | Always check |
| `split("\n")` | Empty elements | Use `splitlines()` |
| `\s` instead of `\S` | Opposite of intended | `\s`=space, `\S`=non-space |

---

## Real Application

```python
# Read a netlist file
with open("inverter.sp", "r") as f:
    netlist = f.read()

cells = parse_netlist_cells(netlist)

# Analyze the transistors
for cell in cells:
    print(f"{cell['name']}: {cell['type']} W={cell['w']} L={cell['l']}")

# Output:
# M1: pmos W=1u L=100n
# M2: nmos W=500n L=100n
```

---

## Keywords for Interview

- "SPICE netlist parsing"
- "Regular expressions"
- "Non-greedy matching"
- "Text processing"
- "EDA automation"
