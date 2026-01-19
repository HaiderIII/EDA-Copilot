"""
Circuit Analyzer Tool

Analyzes circuit netlists and provides insights.
Demonstrates how LLMs can help understand circuit topologies.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Device:
    """Represents a circuit device"""
    name: str
    device_type: str
    terminals: list[str]
    parameters: dict


@dataclass
class CircuitAnalysis:
    """Results of circuit analysis"""
    device_count: dict
    topology_hints: list[str]
    potential_issues: list[str]
    recommended_simulations: list[str]


class CircuitAnalyzer:
    """
    Analyzes circuit netlists to extract device information
    and provide design insights.
    """

    def __init__(self):
        # Common device patterns in SPICE netlists
        self.device_patterns = {
            "nmos": r"^[Mm]\w+\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+nmos",
            "pmos": r"^[Mm]\w+\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+pmos",
            "resistor": r"^[Rr]\w+\s+(\w+)\s+(\w+)\s+([\d.]+[kKmMgG]?)",
            "capacitor": r"^[Cc]\w+\s+(\w+)\s+(\w+)\s+([\d.]+[pPnNuUfF]?)",
            "inductor": r"^[Ll]\w+\s+(\w+)\s+(\w+)\s+([\d.]+[nNuUmM]?[Hh]?)",
            "voltage": r"^[Vv]\w+\s+(\w+)\s+(\w+)\s+([\d.]+)",
            "current": r"^[Ii]\w+\s+(\w+)\s+(\w+)\s+([\d.]+)",
        }

    def parse_netlist(self, netlist: str) -> list[Device]:
        """Parse a SPICE netlist and extract devices"""
        devices = []

        for line in netlist.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('*'):
                continue

            # Try to match each device type
            for device_type, pattern in self.device_patterns.items():
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    # Extract device name from line
                    parts = line.split()
                    name = parts[0]

                    devices.append(Device(
                        name=name,
                        device_type=device_type,
                        terminals=list(match.groups()[:-1]) if match.groups() else [],
                        parameters={"raw": line}
                    ))
                    break

        return devices

    def analyze(self, netlist: str) -> CircuitAnalysis:
        """
        Analyze a circuit netlist.

        Args:
            netlist: SPICE netlist string

        Returns:
            CircuitAnalysis with device counts, topology hints, etc.
        """
        devices = self.parse_netlist(netlist)

        # Count devices by type
        device_count = {}
        for d in devices:
            device_count[d.device_type] = device_count.get(d.device_type, 0) + 1

        # Detect common topologies
        topology_hints = self._detect_topologies(devices, device_count)

        # Check for potential issues
        potential_issues = self._check_issues(devices, device_count)

        # Recommend simulations
        recommended_sims = self._recommend_simulations(device_count, topology_hints)

        return CircuitAnalysis(
            device_count=device_count,
            topology_hints=topology_hints,
            potential_issues=potential_issues,
            recommended_simulations=recommended_sims
        )

    def _detect_topologies(self, devices: list[Device], counts: dict) -> list[str]:
        """Detect common analog circuit topologies"""
        hints = []

        nmos_count = counts.get("nmos", 0)
        pmos_count = counts.get("pmos", 0)

        # Differential pair detection
        if nmos_count >= 2 or pmos_count >= 2:
            hints.append("Possible differential pair (matched transistor pair)")

        # Current mirror
        if nmos_count >= 2:
            hints.append("Possible NMOS current mirror")
        if pmos_count >= 2:
            hints.append("Possible PMOS current mirror")

        # Amplifier stages
        if nmos_count > 0 and pmos_count > 0:
            if nmos_count + pmos_count <= 4:
                hints.append("Possible single-stage amplifier")
            elif nmos_count + pmos_count <= 8:
                hints.append("Possible two-stage amplifier (OTA)")
            else:
                hints.append("Complex multi-stage circuit")

        # RC networks
        if counts.get("resistor", 0) > 0 and counts.get("capacitor", 0) > 0:
            hints.append("Contains RC network (possible filter/compensation)")

        return hints

    def _check_issues(self, devices: list[Device], counts: dict) -> list[str]:
        """Check for potential design issues"""
        issues = []

        # Odd transistor counts might indicate asymmetry
        nmos = counts.get("nmos", 0)
        pmos = counts.get("pmos", 0)

        if nmos % 2 != 0 and nmos > 1:
            issues.append(f"Odd number of NMOS ({nmos}) - check for intentional asymmetry")

        if pmos % 2 != 0 and pmos > 1:
            issues.append(f"Odd number of PMOS ({pmos}) - check for intentional asymmetry")

        # No bias sources
        if counts.get("current", 0) == 0 and counts.get("voltage", 0) <= 1:
            issues.append("No explicit bias sources - verify biasing scheme")

        return issues

    def _recommend_simulations(self, counts: dict, topologies: list[str]) -> list[str]:
        """Recommend appropriate simulations based on circuit type"""
        sims = ["DC operating point (always start here)"]

        # AC analysis for amplifiers
        if any("amplifier" in t.lower() for t in topologies):
            sims.append("AC analysis (gain, bandwidth, phase margin)")

        # Transient for dynamic behavior
        if counts.get("capacitor", 0) > 0:
            sims.append("Transient analysis (settling, slew rate)")

        # Noise for analog circuits
        if counts.get("nmos", 0) > 0 or counts.get("pmos", 0) > 0:
            sims.append("Noise analysis (input-referred noise)")

        # Monte Carlo for matching-sensitive circuits
        if any("differential" in t.lower() or "mirror" in t.lower() for t in topologies):
            sims.append("Monte Carlo (mismatch sensitivity)")

        return sims

    def to_dict(self, analysis: CircuitAnalysis) -> dict:
        """Convert analysis to dictionary for JSON serialization"""
        return {
            "device_count": analysis.device_count,
            "topology_hints": analysis.topology_hints,
            "potential_issues": analysis.potential_issues,
            "recommended_simulations": analysis.recommended_simulations
        }


# Tool definition for agent integration
CIRCUIT_ANALYZER_TOOL = {
    "name": "analyze_circuit",
    "description": "Analyze a SPICE netlist to identify devices, detect circuit topology, and recommend simulations",
    "input_schema": {
        "type": "object",
        "properties": {
            "netlist": {
                "type": "string",
                "description": "SPICE netlist content to analyze"
            }
        },
        "required": ["netlist"]
    }
}


def handle_tool_call(tool_input: dict) -> str:
    """Handler for agent tool calls"""
    analyzer = CircuitAnalyzer()
    analysis = analyzer.analyze(tool_input["netlist"])
    return json.dumps(analyzer.to_dict(analysis), indent=2)


# Demo
if __name__ == "__main__":
    # Sample operational amplifier netlist
    sample_netlist = """
* Simple Differential Amplifier
* Input pair
M1 out1 inp tail vss nmos w=1u l=100n
M2 out2 inn tail vss nmos w=1u l=100n

* Active load (current mirror)
M3 out1 out1 vdd vdd pmos w=2u l=100n
M4 out2 out1 vdd vdd pmos w=2u l=100n

* Tail current source
M5 tail bias vss vss nmos w=500n l=100n

* Compensation cap
C1 out2 0 1p

* Bias
Ibias bias 0 10u
Vdd vdd 0 1.8
Vss vss 0 0
"""

    analyzer = CircuitAnalyzer()
    analysis = analyzer.analyze(sample_netlist)

    print("=" * 60)
    print("CIRCUIT ANALYSIS RESULTS")
    print("=" * 60)
    print(f"\nDevice Count: {analysis.device_count}")
    print(f"\nTopology Hints:")
    for hint in analysis.topology_hints:
        print(f"  - {hint}")
    print(f"\nPotential Issues:")
    for issue in analysis.potential_issues:
        print(f"  - {issue}")
    print(f"\nRecommended Simulations:")
    for sim in analysis.recommended_simulations:
        print(f"  - {sim}")
