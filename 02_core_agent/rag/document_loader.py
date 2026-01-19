"""
Document Loader for RAG System
Loads and chunks design rule documents for embedding.
"""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class DocumentChunk:
    """Represents a single chunk of a document with metadata."""
    text: str
    metadata: dict  # rule_id, layer, value, description, etc.


def load_design_rules(file_path: str) -> list[DocumentChunk]:
    """
    Load design rules from a text file and split into chunks.

    Args:
        file_path: Path to the design_rules.txt file

    Returns:
        List of DocumentChunk objects, one per rule
    """
    # TODO 1: Read the file content
    # Hint: Use Path(file_path).read_text()
    content = Path(file_path).read_text()
    # TODO 2: Split into sections by "---" separator
    # Hint: Use content.split("---")
    sections = content.split("---")
    # TODO 3: For each section, call parse_rule() to extract metadata
    # Hint: Skip empty sections and section headers (lines starting with ===)
    chunks = []
    for section in sections:
        section = section.strip()
        if not section or section.startswith("==="):
            continue
        chunk = parse_rule(section)
        if chunk:
            chunks.append(chunk)
    # TODO 4: Return list of DocumentChunk objects

    return chunks


def parse_rule(rule_text: str) -> DocumentChunk | None:
    """
    Parse a single rule section and extract metadata.

    Example input:
        M1.W.1 - Minimum Width
        Layer: Metal1
        Value: 18nm
        Description: All Metal1 shapes must have minimum width of 18nm.

    Args:
        rule_text: Raw text of a single rule

    Returns:
        DocumentChunk with extracted metadata, or None if invalid
    """
    # TODO 5: Extract rule_id from first line (e.g., "M1.W.1")
    # Hint: Use regex r'^([A-Z0-9.]+)\s*-' to match rule ID
    rule_id_match = re.search(r'^([A-Z0-9.]+)\s*-', rule_text)
    # TODO 6: Extract layer using regex r'Layer:\s*(.+)'
    layer_match = re.search(r'Layer:\s*(.+)', rule_text)
    # TODO 7: Extract value using regex r'Value:\s*(.+)'
    value_match = re.search(r'Value:\s*(.+)', rule_text)
    # TODO 8: Extract description using regex r'Description:\s*(.+)'
    description_match = re.search(r'Description:\s*(.+)', rule_text)
    # TODO 9: Build metadata dict and return DocumentChunk
    # metadata = {
    #     "rule_id": ...,
    #     "layer": ...,
    #     "value": ...,
    #     "source": "ASAP7_DRM"
    # }
    if not rule_id_match:
        return None # Invalid rule format   
    metadata = {
        "rule_id": rule_id_match.group(1).strip(),
        "layer": layer_match.group(1).strip() if layer_match else "N/A",
        "value": value_match.group(1).strip() if value_match else "N/A",
        "description": description_match.group(1).strip() if description_match else "N/A",
        "source": "ASAP7_DRM"
    }
    return DocumentChunk(text=rule_text.strip(), metadata=metadata)             


# Test function - run this to verify your implementation
if __name__ == "__main__":
    # Get the path to design_rules.txt
    data_path = Path(__file__).parent / "data" / "design_rules.txt"

    # Load and parse
    chunks = load_design_rules(str(data_path))

    # Print results
    print(f"Loaded {len(chunks)} design rules\n")

    # Show first 3 chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"--- Chunk {i+1} ---")
        print(f"Rule ID: {chunk.metadata.get('rule_id', 'N/A')}")
        print(f"Layer: {chunk.metadata.get('layer', 'N/A')}")
        print(f"Value: {chunk.metadata.get('value', 'N/A')}")
        print(f"Text preview: {chunk.text[:100]}...")
        print()
