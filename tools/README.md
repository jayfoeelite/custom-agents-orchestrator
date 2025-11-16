# AI Agent Orchestration System - Validation & Analysis Tools

This directory contains tools for validating, analyzing, and visualizing the AI Agent Orchestration System.

## Installation

Install Python dependencies:

```bash
pip install -r tools/requirements.txt
```

## Tools

### 1. Agent Validator (`validate-agents.py`)

Validates all agent YAML files against the JSON schema to ensure structural integrity and compliance.

**Features:**
- JSON Schema validation for required fields
- Communication protocol header verification
- Signal Interpretation Framework validation (for state-scribe)
- Detection of overly long single-line customInstructions
- Colored terminal output for easy reading

**Usage:**

```bash
# Validate all agents
python tools/validate-agents.py

# Validate with verbose output
python tools/validate-agents.py --verbose

# Validate a specific agent
python tools/validate-agents.py --agent agents/uber-orchestrator.yaml
```

**Exit Codes:**
- `0` - All validations passed
- `1` - One or more validations failed

**Example Output:**
```
======================================================================
AI Agent Orchestration System - Validator
======================================================================

Loading schema from: schemas/agent-mode-schema.json
✓ Schema loaded successfully

Validating 45 agent files from: agents

Validating: agents/uber-orchestrator.yaml
  ✓ PASS

...

======================================================================
Validation Summary
======================================================================

Total agents:    45
Passed:          45
Failed:          0

✓ All validations PASSED
```

---

### 2. Dependency Graph Generator (`generate-dependency-graph.py`)

Analyzes agent YAML files to extract delegation patterns and generates visual dependency graphs.

**Features:**
- Extracts delegation relationships from customInstructions
- Categorizes agents (orchestrators, workers, validators, quality)
- Generates multiple output formats (Mermaid, PNG, SVG, DOT)
- Color-coded node visualization
- Graph statistics

**Usage:**

```bash
# Generate Mermaid diagram (default)
python tools/generate-dependency-graph.py

# Generate PNG diagram
python tools/generate-dependency-graph.py --format png

# Generate all formats
python tools/generate-dependency-graph.py --format all

# Custom output path
python tools/generate-dependency-graph.py --output docs/my-graph
```

**Supported Formats:**
- `mermaid` - Mermaid flowchart markdown (default)
- `png` - PNG image (requires graphviz)
- `svg` - SVG vector image (requires graphviz)
- `dot` - Graphviz DOT source file
- `all` - Generate all formats

**Color Coding:**
- **Blue** (`#4A90E2`) - Orchestrators
- **Green** (`#7ED321`) - Workers (coders, writers, testers, etc.)
- **Orange** (`#F5A623`) - Validators (auditors, guardians)
- **Purple** (`#BD10E0`) - Quality agents (RULER, Devil's Advocate, BMO)

**Example Output:**
```
======================================================================
AI Agent Orchestration System - Dependency Graph Generator
======================================================================

Analyzing 45 agent files...

✓ uber-orchestrator → orchestrator-goal-clarification, devils-advocate-critical-evaluator, ...
✓ orchestrator-sparc-specification-phase → research-planner-strategic, spec-writer-from-examples, ...
...

======================================================================
Graph Statistics
======================================================================

Total agents:     45
Total delegations: 127
Orchestrators:    11
Workers:          25
Validators:       5
Quality Agents:   4

✓ Generated Mermaid diagram: docs/agent-dependency-graph.md

✓ Dependency graph generation complete
```

---

## JSON Schema (`schemas/agent-mode-schema.json`)

Defines the structure and validation rules for agent mode definitions.

**Required Fields:**
- `slug` - Unique identifier (kebab-case)
- `name` - Display name with optional emoji
- `roleDefinition` - Agent's core purpose
- `customInstructions` - Detailed operational directives
- `groups` - Permission sets (`read`, `edit`, `mcp`, `command`)
- `source` - Origin indicator (`project`, `system`)

**Optional Fields:**
- `version` - Semantic version (recommended)
- `description` - Extended description
- `tags` - Categorization tags
- `dependencies` - List of dependent agent slugs

**Example:**
```json
{
  "customModes": [
    {
      "slug": "uber-orchestrator",
      "name": "🧐 UBER Orchestrator",
      "roleDefinition": "You are the master conductor...",
      "customInstructions": "You must adhere to...",
      "groups": ["read", "mcp"],
      "source": "project",
      "version": "1.0.0"
    }
  ]
}
```

---

## Validation Criteria

### Communication Protocol

All agents must include the mandatory routing header requirement in their `customInstructions`:

```
To: [recipient agent's slug], From: [your agent's slug]
```

The validator checks for the presence of this protocol mention.

### Signal Interpretation Framework

The `orchestrator-state-scribe` agent must include all Signal Framework components:
- Signal Interpretation Framework
- signalCategories
- signalTypes
- interpretationLogic
- keywordsToSignalType

### Code Quality

The validator warns about:
- Very long single-line `customInstructions` (>1000 characters)
- Recommendation: Use YAML literal blocks for better readability

---

## Development Workflow

### Adding a New Agent

1. Create `agents/new-agent.yaml` following the schema
2. Validate: `python tools/validate-agents.py --agent agents/new-agent.yaml`
3. Regenerate dependency graph: `python tools/generate-dependency-graph.py`
4. Commit changes

### Modifying Existing Agents

1. Edit agent YAML file
2. Run full validation: `python tools/validate-agents.py`
3. Update dependency graph if delegation patterns changed
4. Review validation report

### Pre-Commit Checks

Add to your `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python tools/validate-agents.py
if [ $? -ne 0 ]; then
    echo "Agent validation failed. Commit aborted."
    exit 1
fi
```

---

## Troubleshooting

### "graphviz not installed"

For PNG/SVG output, install graphviz:

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows
choco install graphviz

# Then install Python bindings
pip install graphviz
```

### "Schema validation failed"

Check the error message for which field is missing or invalid. Common issues:
- Missing required field (slug, name, roleDefinition, customInstructions, groups, source)
- Invalid `groups` value (must be one of: read, edit, mcp, command)
- Invalid `source` value (must be: project or system)
- Invalid slug format (must be kebab-case)

### "YAML parsing error"

Ensure valid YAML syntax:
- Proper indentation (spaces, not tabs)
- Quoted strings for special characters
- Valid list notation for arrays

---

## Files Created

```
tools/
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── validate-agents.py              # Schema validator (267 lines)
└── generate-dependency-graph.py    # Graph generator (311 lines)

schemas/
└── agent-mode-schema.json          # JSON Schema definition
```

---

## Future Enhancements

Potential improvements:
1. Versioning migration tool
2. Agent template generator
3. Circular dependency detector
4. Performance impact analyzer
5. Auto-documentation generator from agent definitions

---

**Last Updated**: 2025-11-14  
**Validator Version**: 1.0.0  
**Graph Generator Version**: 1.0.0