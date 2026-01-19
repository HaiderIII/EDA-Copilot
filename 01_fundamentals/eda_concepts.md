# EDA & Cadence Concepts for Apple Interview

> **Goal**: Understand enough about Cadence tools and analog design flow to have intelligent conversations and build relevant automation.

---

## 1. The Analog/RF Design Flow

Unlike digital design (which you're familiar with from your Physical-Design repo), **analog design** is more iterative and manual:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALOG DESIGN FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Specs   │───▶│Schematic │───▶│Simulation│───▶│  Layout  │  │
│  │ (Design  │    │  Entry   │    │  (ADE)   │    │(Virtuoso)│  │
│  │  Goals)  │    │          │    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │              │               │               │         │
│       │              │               │               ▼         │
│       │              │               │         ┌──────────┐    │
│       │              │               │         │   DRC    │    │
│       │              │               │         │   LVS    │    │
│       │              │               │         │   PEX    │    │
│       │              │               │         └──────────┘    │
│       │              │               │               │         │
│       │              │               ▼               │         │
│       │              │         ┌──────────┐         │         │
│       │              │         │Post-Layout│◀────────┘         │
│       │              │         │Simulation │                   │
│       │              │         └──────────┘                    │
│       │              │               │                         │
│       │              │               ▼                         │
│       │              │    ┌────────────────────┐               │
│       └──────────────┴───▶│ Iterate until specs│               │
│                           │     are met        │               │
│                           └────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Differences from Digital:
| Aspect | Digital | Analog |
|--------|---------|--------|
| **Sizing** | Automated (synthesis) | Manual, critical for performance |
| **Layout** | Place & route tools | Manual, parasitic-sensitive |
| **Simulation** | RTL sim, STA | SPICE-level (Spectre) |
| **Iteration** | Linear flow | Many loops back |

---

## 2. Cadence Virtuoso Ecosystem

### 2.1 Core Tools

**Virtuoso Schematic Editor**
- Draw circuit schematics
- Instance devices (transistors, resistors, caps)
- Connect with wires/pins
- **SKILL Automation**: `schEditor`, `schCellView`, `dbOpenCellView`

**Virtuoso Layout Editor**
- Draw physical geometries
- Place devices, route metals
- **SKILL Automation**: `leHiCreateRect`, `dbCreatePath`

**ADE (Analog Design Environment)**
- Configure simulations
- Set analyses (DC, AC, Transient, Noise)
- View results
- **Variants**: ADE L (legacy), ADE XL (explorer), ADE Assembler

**Spectre Simulator**
- SPICE-level circuit simulation
- Highly accurate but slow
- Netlist → Simulation → Results

### 2.2 Verification Tools

| Tool | Purpose | Output |
|------|---------|--------|
| **DRC** | Design Rule Check | Violations list |
| **LVS** | Layout vs Schematic | Match/mismatch report |
| **PEX** | Parasitic Extraction | Extracted netlist |

---

## 3. SKILL Programming

**SKILL** is Cadence's built-in Lisp-like language for automation.

### Basic Syntax
```skill
; This is a comment

; Define a variable
myVar = 5

; Define a function (procedure)
procedure(myFunction(x y)
    let((result)          ; local variable
        result = x + y
        result             ; return value
    )
)

; Call the function
myFunction(3 4)  ; returns 7

; List operations (SKILL loves lists)
myList = '(1 2 3 4)
car(myList)      ; returns 1 (first element)
cdr(myList)      ; returns (2 3 4) (rest)
```

### Common EDA Operations in SKILL

**Open a cellview:**
```skill
cv = dbOpenCellViewByType("myLib" "myCell" "schematic")
```

**Iterate over instances:**
```skill
foreach(inst cv~>instances
    printf("Instance: %s, Cell: %s\n" inst~>name inst~>cellName)
)
```

**Create a rectangle in layout:**
```skill
cv = dbOpenCellViewByType("myLib" "myCell" "layout" "maskLayout" "w")
dbCreateRect(cv "Metal1" list(0:0 10:5))  ; layer, bBox
```

**Run a simulation:**
```skill
; In ADE context
simulator('spectre)
analysis('dc ?saveOppoint t)
run()
```

### Why Apple Cares About SKILL:
- Virtuoso automation is 90% SKILL
- You can script entire design flows
- **LLM opportunity**: Generate SKILL from natural language!

---

## 4. Simulation Types

### DC Analysis
- Find operating point (bias conditions)
- Input: voltage sources at fixed values
- Output: node voltages, branch currents

### AC Analysis
- Small-signal frequency response
- Input: frequency sweep range
- Output: gain, phase, bandwidth

### Transient Analysis
- Time-domain behavior
- Input: time duration, input waveforms
- Output: voltage/current vs time

### Noise Analysis
- Noise figure, noise contributors
- Critical for RF circuits

### Monte Carlo
- Statistical variation analysis
- Process corners, mismatch

---

## 5. Key Terms for Interview

| Term | Definition | Why It Matters |
|------|------------|----------------|
| **PDK** | Process Design Kit | Library of devices for a specific foundry process |
| **Schematic** | Circuit diagram representation | Input to simulation |
| **Netlist** | Text description of circuit connectivity | Interface to simulators |
| **Testbench** | Circuit + stimulus for simulation | Defines what to simulate |
| **Corner** | Process/voltage/temperature variation | Ensures design works across conditions |
| **Parasitic** | Unintended R/L/C from layout | Extracted for accurate simulation |
| **Symbol** | Graphical representation for hierarchy | Creates reusable blocks |
| **CDF** | Component Description Format | Properties/parameters for instances |

---

## 6. Typical CAD Engineer Tasks (What You'd Automate)

1. **Design Migration**
   - Port schematics between PDKs
   - Update device parameters automatically

2. **Simulation Setup**
   - Create testbenches from templates
   - Configure analyses consistently

3. **Results Processing**
   - Extract metrics from simulation results
   - Generate reports/dashboards

4. **Layout Assistance**
   - Check symmetry requirements
   - Auto-generate guard rings
   - Match parasitic extraction settings

5. **DRC/LVS Debugging**
   - Parse error reports
   - Navigate to violations
   - Suggest fixes

---

## 7. Where LLMs Fit in CAD

### High-Value Opportunities:

```
┌────────────────────────────────────────────────────────────────┐
│                    LLM IN EDA WORKFLOWS                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐     ┌─────────────────┐                  │
│  │  Natural        │     │   SKILL/Python  │                  │
│  │  Language       │────▶│   Code          │  Code Generation │
│  │  Request        │     │   Generation    │                  │
│  └─────────────────┘     └─────────────────┘                  │
│                                                                │
│  ┌─────────────────┐     ┌─────────────────┐                  │
│  │  Error          │     │   Root Cause    │                  │
│  │  Messages       │────▶│   Analysis +    │  Debug Assistant │
│  │  (DRC/LVS)      │     │   Fix Suggest   │                  │
│  └─────────────────┘     └─────────────────┘                  │
│                                                                │
│  ┌─────────────────┐     ┌─────────────────┐                  │
│  │  Documentation  │     │   Instant       │                  │
│  │  (DRM, PDK)     │────▶│   Q&A           │  Knowledge Base  │
│  │                 │     │                 │                  │
│  └─────────────────┘     └─────────────────┘                  │
│                                                                │
│  ┌─────────────────┐     ┌─────────────────┐                  │
│  │  Simulation     │     │   Insights +    │                  │
│  │  Results        │────▶│   Recommendations│ Analysis Help   │
│  │                 │     │                 │                  │
│  └─────────────────┘     └─────────────────┘                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Interview Answer: "How would you apply LLMs to CAD?"

> "I see three high-value applications:
>
> 1. **Intelligent scripting** - Designers describe automation needs in plain
>    English, and the LLM generates SKILL code. This democratizes automation
>    beyond CAD experts.
>
> 2. **Documentation Q&A** - Using RAG to let designers query PDK docs, design
>    rules, and internal wikis conversationally. Faster than manual searching.
>
> 3. **Debug assistance** - LLM analyzes DRC/LVS errors with design context
>    and suggests likely root causes. Experienced engineer knowledge captured
>    and made accessible."

---

## 8. Sample SKILL Code Patterns

You should recognize and be able to explain these patterns:

### Pattern 1: Iterate Over Design Hierarchy
```skill
procedure(listAllCells(libName)
    let((lib)
        lib = ddGetObj(libName)
        foreach(cell lib~>cells
            printf("%s\n" cell~>name)
        )
    )
)
```

### Pattern 2: Property Access
```skill
; The ~> operator accesses object properties
inst~>cellName      ; cell name of instance
inst~>master        ; master cellview
cv~>instances       ; all instances in cellview
cv~>nets            ; all nets
net~>name           ; net name
```

### Pattern 3: Create Shapes
```skill
procedure(createRectangle(cv layer x1 y1 x2 y2)
    dbCreateRect(cv layer list(x1:y1 x2:y2))
)
```

### Pattern 4: Simulation Control
```skill
; Pseudocode for ADE automation
procedure(runDCSweep(varName startVal stopVal)
    analysis('dc)
    desVar(varName startVal)
    sweep(varName startVal stopVal)
    run()
    plot(...)
)
```

---

## 9. Quick Reference Commands

```skill
; Database operations
dbOpenCellViewByType(lib cell view [mode])
dbSave(cv)
dbClose(cv)

; Instance operations
dbCreateInst(cv master instName point orient)
dbCreateNet(cv netName)
dbCreateTerm(cv name direction)

; Layout operations
dbCreateRect(cv layer bBox)
dbCreatePath(cv layer points width)
dbCreatePolygon(cv layer points)

; Schematic operations
schCreateWire(cv type points width)
schCreatePin(cv pinNet direction position)
```

---

## Next Steps

1. Review the SKILL patterns above until you can explain them
2. Move to [Exercise 1](./exercises/01_first_api_call.py) to start coding
3. We'll build tools that generate this type of code automatically

---

## Next: [Exercises](./exercises/)
