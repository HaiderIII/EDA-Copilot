# Apple CAD Custom Design / Simulation Automation Engineer
## Technical Interview Preparation Quiz

**Role:** CAD Custom Design or Simulation Automation Engineer
**Location:** Munich, Germany
**Focus Areas:** Cadence Virtuoso, Simulation Automation, SKILL/Python, AI/LLM

---

## Section 1: Cadence ADE & Simulation (Core Competency)

### Q1.1 - ADE Assembler Architecture
**Question:** Explain the difference between ADE Explorer, ADE Assembler, and ADE XL. When would you choose one over the other?

<details>
<summary>Expected Answer</summary>

- **ADE Explorer (ADE-E):** Single-view simulation, basic parametric analysis, good for quick debug
- **ADE Assembler:** Multi-view simulation, hierarchical testbench management, test reuse across corners
- **ADE XL:** Corner/Monte Carlo analysis, statistical simulations, production verification

**Use Cases:**
- ADE Explorer: Initial design exploration, quick transient/DC analysis
- ADE Assembler: Block-level verification with multiple testbenches, IP qualification
- ADE XL: Sign-off verification, PVT corners, Monte Carlo yield analysis
</details>

---

### Q1.2 - Simulation Performance
**Question:** A designer complains that their transient simulation takes 8 hours. What steps would you take to diagnose and optimize simulation runtime?

<details>
<summary>Expected Answer</summary>

1. **Analyze simulation log:** Check convergence issues, time-step behavior
2. **Netlist optimization:**
   - Remove unnecessary hierarchy
   - Check for floating nodes
   - Verify proper initial conditions
3. **Simulator settings:**
   - Adjust `errpreset` (conservative → moderate → liberal)
   - Tune `maxstep` and `reltol`
   - Enable `multithread` if available
4. **Design-specific:**
   - Check for numerical noise sources
   - Simplify stimulus where possible
   - Use `save` statements to reduce output data
5. **Infrastructure:**
   - Use faster compute nodes
   - Check memory/swap usage
   - Consider distributed simulation (APS)
</details>

---

### Q1.3 - Corner Analysis
**Question:** How would you set up a PVT corner sweep for an LDO regulator across 27 corners (3 process × 3 voltage × 3 temperature)?

<details>
<summary>Expected Answer</summary>

```
Corners Setup:
- Process: TT, FF, SS (+ optional SF, FS for mismatch)
- Voltage: 0.95V, 1.0V, 1.05V (±5%)
- Temperature: -40°C, 25°C, 125°C

In ADE XL:
1. Create corner definition file (.scs)
2. Define process corners using model files
3. Set up design variables for VDD and temp
4. Create corner matrix in Corners tab
5. Define specifications (PSRR > 60dB, dropout < 200mV)
6. Run all corners with parallel jobs

Best Practice:
- Use corner config files for reproducibility
- Enable "stop on first fail" for debug
- Archive results with timestamp
```
</details>

---

### Q1.4 - Monte Carlo Analysis
**Question:** Explain the difference between process variation and mismatch in Monte Carlo simulations. How do you configure each in Spectre?

<details>
<summary>Expected Answer</summary>

**Process Variation:**
- Global variation affecting all devices equally
- Models lot-to-lot and wafer-to-wafer variation
- Configured via `process` section in model files

**Mismatch:**
- Local variation between identical devices
- Scales with 1/sqrt(Area) - larger devices match better
- Configured via `mismatch` section

**Spectre Configuration:**
```spectre
montecarlo numruns=1000 variations=all {
    // process + mismatch
}
montecarlo numruns=1000 variations=process {
    // process only
}
montecarlo numruns=1000 variations=mismatch {
    // mismatch only
}
```

**Statistical Measures:**
- Mean (μ), Standard Deviation (σ)
- 3σ yield analysis
- Cpk for spec compliance
</details>

---

## Section 2: SKILL Programming (Strong Requirement)

### Q2.1 - SKILL Basics
**Question:** Write a SKILL function that finds all instances of a specific cell in a cellview and returns their coordinates.

<details>
<summary>Expected Answer</summary>

```skill
procedure(findCellInstances(libName cellName viewName targetCell)
  let((cv instances result)
    cv = dbOpenCellViewByType(libName cellName viewName nil "r")
    when(cv
      instances = cv~>instances
      result = nil
      foreach(inst instances
        when(inst~>cellName == targetCell
          result = cons(list(inst~>name inst~>xy) result)
        )
      )
      dbClose(cv)
    )
    result
  )
)

;; Usage:
;; findCellInstances("myLib" "topCell" "schematic" "nmos4")
;; Returns: (("I0" (10.0 20.0)) ("I1" (30.0 40.0)) ...)
```
</details>

---

### Q2.2 - Automation Script
**Question:** Write a SKILL script that automatically exports all schematic cellviews in a library to netlists.

<details>
<summary>Expected Answer</summary>

```skill
procedure(batchNetlistExport(libName outputDir @optional (simulator "spectre"))
  let((lib cells cv netlistFile count)
    lib = ddGetObj(libName)
    unless(lib
      error("Library %s not found" libName)
    )

    count = 0
    foreach(cell lib~>cells
      when(member("schematic" cell~>views~>name)
        cv = dbOpenCellViewByType(libName cell~>name "schematic" nil "r")
        when(cv
          netlistFile = strcat(outputDir "/" cell~>name ".scs")

          ;; Set up netlister
          simulator(simulator)
          design(libName cell~>name "schematic")
          createNetlist(?netlistFile netlistFile)

          printf("Exported: %s\n" netlistFile)
          count++
          dbClose(cv)
        )
      )
    )
    printf("Total cells exported: %d\n" count)
    count
  )
)
```
</details>

---

### Q2.3 - CDF and Callbacks
**Question:** Explain what CDF (Component Description Format) is and write a callback function that updates a resistor's width based on its resistance value.

<details>
<summary>Expected Answer</summary>

**CDF Explanation:**
- CDF defines component parameters, properties, and callbacks
- Stored in library as compiled SKILL
- Controls how instances behave in schematic/layout
- Enables parameter-driven design automation

**Callback Function:**
```skill
procedure(updateResWidth(param)
  let((inst R L W rsh)
    inst = param~>instance
    R = cdfParseFloatString(inst~>R)
    L = cdfParseFloatString(inst~>L)
    rsh = 100.0  ;; Sheet resistance in Ohms/sq

    ;; W = (Rsh * L) / R
    when(R > 0
      W = (rsh * L) / R
      dbReplaceProp(inst "W" "float" W)
      printf("Updated W to %g for R=%g, L=%g\n" W R L)
    )
  )
)

;; Register in CDF:
;; cdfCreateParam(cdf "R" "string" "1k"
;;   ?callback "updateResWidth")
```
</details>

---

### Q2.4 - OCEAN Scripting
**Question:** Write an OCEAN script to run a parametric DC sweep and extract the gain of an amplifier.

<details>
<summary>Expected Answer</summary>

```skill
;; OCEAN script for amplifier gain extraction
simulator('spectre)
design("myLib" "amplifier" "schematic")
createNetlist(?recreateAll t)

;; Analysis setup
analysis('dc ?saveOppoint t)
analysis('ac ?start 1 ?stop 1G ?dec 10)

;; Parametric sweep on input bias
desVar("vbias" 0.5)
paramAnalysis("vbias" ?start 0.3 ?stop 0.7 ?step 0.1)

;; Run simulation
run()

;; Extract results
selectResult('ac)
foreach(vb '(0.3 0.4 0.5 0.6 0.7)
  gain = value(db20(VF("/vout") / VF("/vin")) 1e6)
  bw = bandwidth(VF("/vout") 3 "low")
  printf("Vbias=%g: Gain=%gdB, BW=%gMHz\n" vb gain bw/1e6)
)

;; Plot
plot(db20(VF("/vout")))
```
</details>

---

## Section 3: Python Automation (Preferred)

### Q3.1 - Python + Virtuoso Integration
**Question:** How would you integrate Python scripts with Cadence Virtuoso? Describe different approaches.

<details>
<summary>Expected Answer</summary>

**Approaches:**

1. **SKILL-Python Bridge (skillbridge):**
```python
from skillbridge import Workspace
ws = Workspace()
cv = ws.db.open_cell_view_by_type("myLib", "myCell", "schematic")
instances = cv.instances
```

2. **PyCell (PDK development):**
```python
from cni.dlo import *
class MyResistor(DloGen):
    def __init__(self):
        # Define parameterized layout
        pass
```

3. **REST API / Socket Communication:**
```python
import socket
# Send SKILL commands via IPC
sock.send(b'geGetEditCellView()')
```

4. **File-based Integration:**
```python
# Generate SKILL script, execute via virtuoso -replay
with open("script.il", "w") as f:
    f.write('load("automation.il")')
os.system("virtuoso -replay script.il")
```

5. **Cadence AMSGEN / PyAMS:**
- Native Python interface for AMS simulation
</details>

---

### Q3.2 - Data Analysis
**Question:** Write a Python script to parse Spectre simulation output (.raw or .psf) and create a Bode plot.

<details>
<summary>Expected Answer</summary>

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
# Or use libpsf for PSF files

def parse_spectre_raw(filepath):
    """Parse Spectre .raw ASCII file"""
    data = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Parse header and data
    in_data = False
    variables = []
    values = []

    for line in lines:
        if 'Variables:' in line:
            continue
        elif line.startswith('Values:'):
            in_data = True
            continue
        elif in_data:
            values.append(float(line.strip()))

    return np.array(values)

def plot_bode(freq, vout, vin):
    """Create Bode plot from simulation data"""
    # Calculate transfer function
    H = vout / vin
    magnitude_db = 20 * np.log10(np.abs(H))
    phase_deg = np.angle(H, deg=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Magnitude plot
    ax1.semilogx(freq, magnitude_db, 'b-', linewidth=2)
    ax1.set_ylabel('Magnitude (dB)')
    ax1.set_title('Bode Plot - Amplifier Transfer Function')
    ax1.grid(True, which='both', linestyle='--', alpha=0.7)
    ax1.axhline(y=-3, color='r', linestyle='--', label='-3dB')

    # Phase plot
    ax2.semilogx(freq, phase_deg, 'g-', linewidth=2)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.grid(True, which='both', linestyle='--', alpha=0.7)

    # Extract metrics
    dc_gain = magnitude_db[0]
    idx_3db = np.where(magnitude_db < dc_gain - 3)[0]
    if len(idx_3db) > 0:
        bw = freq[idx_3db[0]]
        ax1.axvline(x=bw, color='r', linestyle=':', label=f'BW={bw/1e6:.2f}MHz')

    ax1.legend()
    plt.tight_layout()
    plt.savefig('bode_plot.png', dpi=150)
    plt.show()

    return dc_gain, bw

# Usage
if __name__ == "__main__":
    freq = np.logspace(0, 9, 1000)  # 1Hz to 1GHz
    # Load simulation data
    # plot_bode(freq, vout_data, vin_data)
```
</details>

---

### Q3.3 - Regression Framework
**Question:** Design a Python-based regression framework for nightly simulation runs. What components would you include?

<details>
<summary>Expected Answer</summary>

```python
"""
Simulation Regression Framework Architecture
"""

class RegressionFramework:
    """
    Components:
    1. Test Configuration (YAML/JSON)
    2. Job Scheduler (LSF/Grid Engine integration)
    3. Result Parser
    4. Comparison Engine
    5. Report Generator
    6. Notification System
    """

    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.db = ResultDatabase()

    def load_config(self, filepath):
        """Load test configuration"""
        # config.yaml:
        # tests:
        #   - name: ldo_psrr
        #     library: analog_ip
        #     cell: ldo_top
        #     testbench: tb_psrr
        #     corners: [tt, ff, ss]
        #     specs:
        #       psrr_1khz: "> 60dB"
        #       dropout: "< 200mV"
        pass

    def run_tests(self, parallel=True, max_jobs=32):
        """Execute all tests"""
        jobs = []
        for test in self.config['tests']:
            for corner in test['corners']:
                job = SimulationJob(test, corner)
                jobs.append(job)

        if parallel:
            with JobPool(max_jobs) as pool:
                results = pool.map(self.execute_job, jobs)
        return results

    def execute_job(self, job):
        """Run single simulation job"""
        # Generate OCEAN script
        script = self.generate_ocean(job)

        # Submit to compute farm
        cmd = f"bsub -q normal -o {job.log} spectre -batch {script}"
        subprocess.run(cmd, shell=True)

        # Parse results
        return self.parse_results(job)

    def compare_results(self, current, golden):
        """Compare against golden results"""
        diff = {}
        for metric, value in current.items():
            if metric in golden:
                delta = abs(value - golden[metric]) / golden[metric]
                if delta > 0.05:  # 5% tolerance
                    diff[metric] = {'current': value,
                                   'golden': golden[metric],
                                   'delta': delta}
        return diff

    def generate_report(self, results):
        """Generate HTML/PDF report"""
        # Include:
        # - Pass/Fail summary
        # - Corner coverage
        # - Spec compliance table
        # - Trend charts
        # - Failure analysis
        pass

    def notify(self, results):
        """Send notifications"""
        if results.has_failures():
            self.send_email(
                to=self.config['owners'],
                subject="[FAIL] Nightly Regression",
                body=results.summary()
            )
```
</details>

---

## Section 4: AI/LLM Applications (Preferred)

### Q4.1 - LLM for EDA
**Question:** How could Large Language Models be applied to improve CAD workflows? Give 3 specific use cases with implementation approaches.

<details>
<summary>Expected Answer</summary>

**Use Case 1: Natural Language to SKILL/OCEAN**
```python
# User: "Run AC analysis from 1Hz to 1GHz and plot the gain"
# LLM generates:
"""
analysis('ac ?start 1 ?stop 1G ?dec 20)
run()
plot(db20(VF("/vout")))
"""

# Implementation:
# - Fine-tune LLM on SKILL documentation + examples
# - Use RAG with Cadence command reference
# - Validate generated code before execution
```

**Use Case 2: Design Review Assistant**
```python
# Analyze schematic and provide feedback
class DesignReviewBot:
    def analyze_schematic(self, netlist):
        prompt = f"""
        Analyze this analog circuit netlist for:
        1. Potential stability issues
        2. Bias point problems
        3. Missing decoupling capacitors
        4. ESD protection

        Netlist: {netlist}
        """
        return llm.complete(prompt)
```

**Use Case 3: Log Analysis & Debug**
```python
# Parse simulation errors and suggest fixes
def diagnose_sim_error(log_file):
    error_context = extract_errors(log_file)

    prompt = f"""
    This Spectre simulation failed with:
    {error_context}

    Based on common issues, suggest:
    1. Root cause
    2. Fix recommendations
    3. Similar past issues from knowledge base
    """
    return llm.complete(prompt,
                       context=rag_search(error_context))
```
</details>

---

### Q4.2 - RAG for Documentation
**Question:** Design a RAG (Retrieval-Augmented Generation) system for Cadence documentation. How would you chunk, embed, and retrieve information?

<details>
<summary>Expected Answer</summary>

```python
"""
RAG System for Cadence Documentation
"""

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class CadenceDocRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def ingest_documentation(self, doc_paths):
        """Process Cadence manuals, SKILL reference, etc."""

        # Custom chunking for technical docs
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n## ",      # Section headers
                "\nSyntax:",  # Function definitions
                "\nExample:", # Code examples
                "\n\n",
                "\n"
            ]
        )

        documents = []
        for path in doc_paths:
            text = self.load_document(path)
            chunks = splitter.split_text(text)

            # Add metadata
            for i, chunk in enumerate(chunks):
                documents.append({
                    'content': chunk,
                    'metadata': {
                        'source': path,
                        'chunk_id': i,
                        'doc_type': self.classify_doc(path)
                    }
                })

        # Create vector store
        self.vector_store = Chroma.from_documents(
            documents,
            self.embeddings,
            collection_name="cadence_docs"
        )

    def query(self, question, k=5):
        """Retrieve relevant documentation"""

        # Hybrid search: semantic + keyword
        results = self.vector_store.similarity_search(
            question,
            k=k,
            filter={"doc_type": "skill_reference"}  # Optional filter
        )

        # Re-rank results
        ranked = self.rerank(question, results)

        return ranked

    def generate_answer(self, question):
        """RAG pipeline"""

        # Retrieve
        context = self.query(question)

        # Augment prompt
        prompt = f"""
        You are a Cadence CAD expert. Answer the question using
        the provided documentation context.

        Context:
        {context}

        Question: {question}

        Provide:
        1. Direct answer
        2. SKILL code example if applicable
        3. Reference to documentation section
        """

        # Generate
        return llm.complete(prompt)

# Usage:
rag = CadenceDocRAG()
rag.ingest_documentation([
    "/docs/skill_reference.pdf",
    "/docs/spectre_user_guide.pdf",
    "/docs/virtuoso_ade.pdf"
])

answer = rag.generate_answer(
    "How do I run Monte Carlo analysis with mismatch only?"
)
```
</details>

---

## Section 5: Unix/Infrastructure (Preferred)

### Q5.1 - Debugging with strace
**Question:** Virtuoso crashes during startup. How would you use `strace` to diagnose the issue?

<details>
<summary>Expected Answer</summary>

```bash
# Basic strace to trace system calls
strace -f -o virtuoso_trace.log virtuoso &

# Trace specific calls (file access)
strace -f -e trace=open,openat,read,write virtuoso 2>&1 | tee file_trace.log

# Trace with timestamps
strace -f -tt -T virtuoso 2>&1 | tee timed_trace.log

# Common issues to look for:
# 1. Missing library files
grep -i "ENOENT" virtuoso_trace.log | grep "\.so"

# 2. Permission denied
grep -i "EACCES" virtuoso_trace.log

# 3. License file issues
grep -i "license\|flexlm\|cdslmd" virtuoso_trace.log

# 4. Memory issues
grep -i "mmap\|brk\|ENOMEM" virtuoso_trace.log

# Example output analysis:
# open("/lib64/libstdc++.so.6", O_RDONLY) = -1 ENOENT
# -> Missing C++ runtime library
#
# connect(5, {sa_family=AF_INET, sin_port=htons(5280)}) = -1 ETIMEDOUT
# -> License server connection timeout
```
</details>

---

### Q5.2 - Bash Scripting
**Question:** Write a bash script to monitor simulation jobs and send alerts when they complete or fail.

<details>
<summary>Expected Answer</summary>

```bash
#!/bin/bash
#
# Simulation Job Monitor
# Usage: ./sim_monitor.sh <job_id> <email>
#

JOB_ID=$1
EMAIL=$2
CHECK_INTERVAL=60
LOG_DIR="/tmp/sim_monitor"

mkdir -p $LOG_DIR

monitor_job() {
    local job_id=$1
    local start_time=$(date +%s)

    echo "[$(date)] Starting monitor for job $job_id"

    while true; do
        # Check job status (LSF example)
        status=$(bjobs -noheader -o "stat" $job_id 2>/dev/null)

        case $status in
            "DONE")
                duration=$(($(date +%s) - start_time))
                send_notification "SUCCESS" "Job $job_id completed in ${duration}s"
                exit 0
                ;;
            "EXIT")
                send_notification "FAILURE" "Job $job_id failed. Check logs."
                exit 1
                ;;
            "RUN")
                echo "[$(date)] Job $job_id still running..."
                ;;
            "PEND")
                echo "[$(date)] Job $job_id pending..."
                ;;
            "")
                send_notification "ERROR" "Job $job_id not found"
                exit 2
                ;;
        esac

        # Check for simulation errors in log
        if [ -f "${LOG_DIR}/${job_id}.log" ]; then
            if grep -q "ERROR\|FATAL\|Convergence" "${LOG_DIR}/${job_id}.log"; then
                send_notification "WARNING" "Errors detected in job $job_id"
            fi
        fi

        sleep $CHECK_INTERVAL
    done
}

send_notification() {
    local status=$1
    local message=$2

    # Email notification
    echo "$message" | mail -s "[$status] Simulation Job Alert" $EMAIL

    # Slack webhook (optional)
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"[$status] $message\"}" \
            $SLACK_WEBHOOK
    fi

    echo "[$(date)] Notification sent: $status - $message"
}

# Parse resource usage
get_job_stats() {
    local job_id=$1
    bjobs -l $job_id | grep -E "CPU|MEM|SWAP"
}

# Main
if [ -z "$JOB_ID" ] || [ -z "$EMAIL" ]; then
    echo "Usage: $0 <job_id> <email>"
    exit 1
fi

monitor_job $JOB_ID
```
</details>

---

### Q5.3 - Environment Management
**Question:** How would you set up a reproducible Cadence environment for a team of 50 engineers? Consider tool versions, PDK access, and license management.

<details>
<summary>Expected Answer</summary>

```bash
# /opt/cad/setup/cadence_env.sh
# Modular environment setup

#==========================================
# Tool Version Management (Modules)
#==========================================
module purge
module load cadence/ic618_ISR20  # Specific version
module load cadence/spectre/23.1
module load cadence/pegasus/23.1

#==========================================
# License Configuration
#==========================================
export CDS_LIC_FILE="5280@license1.company.com:5280@license2.company.com"
export LM_LICENSE_FILE="$CDS_LIC_FILE"

# License queuing
export CDS_LIC_QUEUE_POLL=30
export CDS_LIC_QUEUE_TIMEOUT=3600

#==========================================
# PDK Setup
#==========================================
export PDK_HOME="/opt/pdk/tsmc_n5"
export PDK_VERSION="1.0.2a"

# Read-only PDK access
if [ ! -d "$PDK_HOME" ]; then
    echo "ERROR: PDK not found at $PDK_HOME"
    return 1
fi

# Add PDK to library path
export CDS_INST_DIR="/opt/cadence/IC618"
export CDSHOME="$CDS_INST_DIR"

#==========================================
# User-specific Configuration
#==========================================
export CDS_PROJECT="${HOME}/projects/current"
export CDS_WORKDIR="${CDS_PROJECT}/work"

# Create standard directory structure
mkdir -p ${CDS_WORKDIR}/{simulation,calibre,logs}

#==========================================
# cds.lib Generation
#==========================================
cat > ${CDS_WORKDIR}/cds.lib << EOF
SOFTINCLUDE ${PDK_HOME}/cds.lib
SOFTINCLUDE ${CDS_PROJECT}/cds.lib
DEFINE work ${CDS_WORKDIR}/lib
EOF

#==========================================
# Reproducibility: Lock versions
#==========================================
echo "Environment initialized:"
echo "  Virtuoso: $(virtuoso -V 2>&1 | head -1)"
echo "  Spectre:  $(spectre -V 2>&1 | head -1)"
echo "  PDK:      $PDK_VERSION"
echo "  Date:     $(date -I)"

# Log environment for reproducibility
env | sort > ${CDS_WORKDIR}/logs/env_$(date +%Y%m%d).log
```

**Docker/Container approach:**
```dockerfile
FROM centos:7
RUN yum install -y libXext libSM libXrender
COPY cadence_install/ /opt/cadence/
COPY pdk/ /opt/pdk/
ENV CDS_INST_DIR=/opt/cadence/IC618
ENTRYPOINT ["/opt/cad/setup/cadence_env.sh"]
```
</details>

---

## Section 6: Problem Solving & Communication

### Q6.1 - Scenario: Tool Evaluation
**Question:** Apple is evaluating a new simulation tool from a startup. How would you conduct the evaluation and present your findings to stakeholders?

<details>
<summary>Expected Answer</summary>

**Evaluation Framework:**

1. **Define Criteria (weighted)**
   - Performance: 30% (runtime, capacity, accuracy)
   - Features: 25% (capabilities vs current tool)
   - Integration: 20% (Virtuoso, flow compatibility)
   - Support: 15% (responsiveness, roadmap)
   - Cost: 10% (TCO over 3 years)

2. **Benchmark Suite**
   - Representative designs (small, medium, large)
   - Standard analyses (DC, AC, transient, noise)
   - Corner/Monte Carlo scalability
   - Compare against current tool (Spectre)

3. **Pilot Program**
   - 2-3 designers using tool for 1 month
   - Real project, non-critical path
   - Collect qualitative feedback

4. **Risk Assessment**
   - Startup viability
   - Vendor lock-in concerns
   - Migration effort

5. **Presentation Structure**
   - Executive summary (1 slide)
   - Quantitative comparison (benchmarks)
   - User feedback summary
   - TCO analysis
   - Recommendation with confidence level
   - Risk mitigation plan
</details>

---

### Q6.2 - Scenario: Production Issue
**Question:** On Friday at 5 PM, a critical tapeout simulation fails with a cryptic error. The designer needs results by Monday. Walk through your debugging approach.

<details>
<summary>Expected Answer</summary>

**Immediate Actions (First 30 minutes):**

1. **Gather Information**
   ```bash
   # Get full error context
   tail -100 simulation.log
   grep -i "error\|warning\|fatal" simulation.log

   # Check recent changes
   git log -5 --oneline
   p4 changes -m 5 //depot/...
   ```

2. **Reproduce Issue**
   - Run in debug mode: `spectre -log debug.log +diagnose`
   - Isolate: Does it fail on all corners or specific one?

3. **Quick Fixes to Try**
   - Clean rebuild: `rm -rf psf/ spectre.log; spectre ...`
   - Reset to known-good checkpoint
   - Try different compute node (rule out infra)

**Systematic Debug (1-2 hours):**

4. **Binary Search**
   - If design changed: revert to last working version
   - If tool updated: use previous version
   - Narrow down to specific subcircuit

5. **Common Root Causes**
   - Convergence: Check initial conditions, adjust `reltol`
   - License: Verify feature availability
   - Memory: Check `/tmp` space, increase swap
   - Netlist: Look for floating nodes, shorts

**Escalation Path:**

6. **If unresolved after 2 hours:**
   - Page on-call CAD engineer
   - Open priority ticket with Cadence
   - Prepare workaround (simplified sim, different corner)

7. **Communication**
   - Update designer every hour
   - Set realistic expectations
   - Document findings for post-mortem

**Monday Deliverable Plan:**
- Primary: Fix root cause
- Backup: Run with reduced accuracy
- Fallback: Provide partial results with known limitations
</details>

---

## Section 7: Behavioral Questions

### Q7.1 - Innovation
**Question:** Describe a time when you developed an automation solution that significantly improved a workflow. What was the impact?

<details>
<summary>Expected Answer Framework</summary>

**STAR Method:**

- **Situation:** [Describe the problem/inefficiency]
- **Task:** [Your responsibility]
- **Action:** [Technical approach + implementation]
- **Result:** [Quantified impact]

**Good Answer Elements:**
- Specific technical details
- Collaboration with users
- Measurable improvement (time saved, errors reduced)
- Adoption by team
- Lessons learned
</details>

---

### Q7.2 - Collaboration
**Question:** How do you handle situations where designers resist adopting new CAD tools or methodologies?

<details>
<summary>Expected Answer Framework</summary>

**Approach:**

1. **Understand Resistance**
   - Listen to concerns (learning curve, trust, workflow disruption)
   - Validate their expertise and current methods

2. **Demonstrate Value**
   - Show concrete benefits with their actual design
   - Side-by-side comparison
   - Quick wins first

3. **Reduce Friction**
   - Provide excellent documentation
   - Office hours / training sessions
   - Gradual rollout, not forced migration

4. **Build Champions**
   - Find early adopters
   - Let peer success speak

5. **Iterate Based on Feedback**
   - Be willing to adjust based on real usage
   - Show that their input matters
</details>

---

## Scoring Guide

| Section | Weight | Topics |
|---------|--------|--------|
| Cadence ADE/Simulation | 30% | Core technical competency |
| SKILL Programming | 25% | Automation capability |
| Python Integration | 15% | Modern tooling |
| AI/LLM Applications | 10% | Innovation mindset |
| Unix/Infrastructure | 10% | System-level understanding |
| Problem Solving | 10% | Real-world scenarios |

**Rating Scale:**
- **5 - Expert:** Deep knowledge, teaches others, innovates
- **4 - Strong:** Solid understanding, handles complex cases
- **3 - Proficient:** Competent, needs occasional guidance
- **2 - Developing:** Basic knowledge, needs mentoring
- **1 - Novice:** Limited exposure, requires training

---

## Additional Resources

- Cadence SKILL Language Reference
- Spectre Simulation Platform User Guide
- Python skillbridge documentation
- Apple Hardware Engineering culture

---

*Good luck with your interview!*
