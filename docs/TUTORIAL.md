# Agent Validation Tools - Interactive Tutorial

This tutorial demonstrates how to use the validation and analysis tools to create, validate, and analyze custom agent modes for the SPARC orchestration system.

## Prerequisites

- Python 3.7+ installed
- Dependencies installed: `python -m pip install -r tools/requirements.txt`
- Basic understanding of YAML syntax

## Tutorial Overview

1. Understanding the Agent Schema
2. Creating a Valid Agent
3. Validating Your Agent
4. Common Validation Errors & Fixes
5. Analyzing Agent Dependencies
6. Best Practices

---

## Part 1: Understanding the Agent Schema

The JSON Schema ([`schemas/agent-mode-schema.json`](../schemas/agent-mode-schema.json:1)) defines the structure every agent must follow.

### Required Fields

```yaml
slug: agent-name           # kebab-case identifier
name: 🎯 Agent Name        # Display name with optional emoji
roleDefinition: |          # Agent's purpose and responsibility
  Clear description of what this agent does
customInstructions: |      # Detailed operational instructions
  Step-by-step instructions for the agent
groups:                    # Permission groups
  - read                   # Can read files
  - edit                   # Can write/modify files
  - mcp                    # Can use MCP tools
  - command                # Can execute commands
source: project            # Source identifier
```

### Optional Fields

```yaml
version: "1.0.0"           # Semantic version (X.Y.Z)
description: "Brief description"
tags: ["orchestrator", "tdd"]
dependencies: ["other-agent-slug"]
```

---

## Part 2: Creating a Valid Agent

Let's create a sample agent that performs code quality checks.

**Create: `agents/sample-code-quality-checker.yaml`**

```yaml
slug: sample-code-quality-checker
name: ✅ Sample Code Quality Checker
version: "1.0.0"
description: "Tutorial example demonstrating agent validation"
tags: ["quality", "validation", "tutorial"]
roleDefinition: |
  You are a specialized code quality checker responsible for analyzing
  code files to ensure they meet project standards. Your role is to
  identify potential issues, suggest improvements, and generate quality
  reports that help maintain code excellence.
customInstructions: |
  You must adhere to a strict communication protocol by including the
  mandatory routing header To: [recipient agent's slug], From: [your
  agent's slug] at the absolute beginning of your task_complete message
  ONLY. You must use the `database-query` tool to query the
  `project_memory` table. After completing your initial context-gathering
  phase using read_file, you must perform a mandatory planning step by
  creating a comprehensive, step-by-step Plan of Action.
  
  Your workflow consists of four phases. Phase one is Context Gathering
  where you use read_file to load the target code files and relevant
  project standards. Phase two is Quality Analysis where you check for
  code smells, naming conventions, complexity metrics, test coverage
  gaps, and documentation completeness. Phase three is Report Generation
  where you create a detailed quality report saved to reports/quality/
  directory. Phase four is Completion where you use attempt_completion
  with a summary of findings and the report file path.
  
  Your verifiable outcome is the creation of a quality report file. The
  report must include a summary of issues found, severity levels
  (critical, high, medium, low), specific file locations with line
  numbers, and actionable recommendations. Use write_to_file to save the
  report. Your attempt_completion summary must detail the number of
  issues by severity and provide the report file path.
groups:
  - read
  - edit
  - mcp
source: project
dependencies:
  - orchestrator-state-scribe
```

---

## Part 3: Validating Your Agent

### 3.1 Validate Single Agent

```bash
python tools/validate-agents.py agents/sample-code-quality-checker.yaml
```

**Expected Output:**

```
======================================================================
AI Agent Orchestration System - Validator
======================================================================

Loading schema from: schemas/agent-mode-schema.json
✓ Schema loaded successfully

Validating 1 agent file

Validating: agents/sample-code-quality-checker.yaml
  ✓ PASS
  ⚠️  Agent 'sample-code-quality-checker' has very long single-line customInstructions (>1000 chars)

======================================================================
Validation Summary
======================================================================

Total agents:    1
Passed:          1
Failed:          0
With warnings:   1

⚠ Validation PASSED with warnings
```

The warning about long customInstructions is expected and acceptable for complex agents with detailed workflows.

### 3.2 Validate All Agents

```bash
python tools/validate-agents.py
```

This validates all 45 production agents plus your sample agent (46 total).

---

## Part 4: Common Validation Errors & Fixes

### Error 1: Invalid Slug Format

**❌ Invalid:**
```yaml
slug: Sample_Agent_123   # Contains uppercase and underscore
```

**✅ Fixed:**
```yaml
slug: sample-agent-123   # kebab-case only
```

**Validator Output:**
```
✗ FAIL - Schema Validation Error
  'Sample_Agent_123' does not match '^[a-z0-9]+(-[a-z0-9]+)*$'
```

### Error 2: Missing Required Field

**❌ Invalid:**
```yaml
slug: sample-agent
name: Sample Agent
# Missing roleDefinition
customInstructions: "..."
groups:
  - read
source: project
```

**Validator Output:**
```
✗ FAIL - Schema Validation Error
  'roleDefinition' is a required property
```

**✅ Fixed:**
```yaml
slug: sample-agent
name: Sample Agent
roleDefinition: "This agent performs sample operations"
customInstructions: "..."
groups:
  - read
source: project
```

### Error 3: Invalid Group Permission

**❌ Invalid:**
```yaml
groups:
  - read
  - delete    # Not a valid group
```

**Validator Output:**
```
✗ FAIL - Schema Validation Error
  'delete' is not one of ['read', 'edit', 'mcp', 'command']
```

**✅ Fixed:**
```yaml
groups:
  - read
  - edit
```

### Error 4: Invalid Version Format

**❌ Invalid:**
```yaml
version: "1.0"      # Missing patch number
```

**Validator Output:**
```
✗ FAIL - Schema Validation Error
  '1.0' does not match semantic version pattern
```

**✅ Fixed:**
```yaml
version: "1.0.0"    # Semantic versioning: X.Y.Z
```

### Error 5: Missing Communication Protocol

**⚠️ Warning** (not an error, but best practice):

If your agent delegates to other agents, ensure customInstructions includes:

```yaml
customInstructions: |
  You must adhere to a strict communication protocol by including the
  mandatory routing header To: [recipient agent's slug], From: [your
  agent's slug] at the absolute beginning of your task_complete message
  ONLY.
```

---

## Part 5: Analyzing Agent Dependencies

### 5.1 Generate Dependency Graph

After creating your agent, analyze how it fits into the orchestration workflow:

```bash
python tools/generate-dependency-graph.py
```

**Output:**
```
✓ sample-code-quality-checker → orchestrator-state-scribe

======================================================================
Graph Statistics
======================================================================

Total agents:      46
Total delegations: 64
Orchestrators:     11
Workers:           10
Validators:        5
Quality Agents:    4

✓ Generated Mermaid diagram: docs/agent-dependency-graph.md
```

### 5.2 View the Graph

Open [`docs/agent-dependency-graph.md`](agent-dependency-graph.md:1) to see your agent in the visualization.

Your agent will appear as:
- **Green node** (Worker category)
- **Arrow** pointing to `orchestrator-state-scribe` (dependency)

### 5.3 Generate PNG/SVG (Optional)

If you have Graphviz installed:

```bash
python tools/generate-dependency-graph.py --format png
python tools/generate-dependency-graph.py --format svg
```

---

## Part 6: Best Practices

### 6.1 Naming Conventions

**Slugs:**
- Use kebab-case: `my-agent-name`
- Be descriptive: `code-quality-checker` not `checker`
- Include category prefix: `orchestrator-`, `tester-`, `coder-`

**Names:**
- Use emoji for visual recognition: `✅ Code Quality Checker`
- Keep it concise but descriptive
- Match the slug meaning

### 6.2 CustomInstructions Structure

Follow the proven SPARC pattern:

1. **Communication Protocol** (first paragraph)
2. **Database Query Requirement** (if applicable)
3. **Planning Step** (mandatory for orchestrators)
4. **Workflow Phases** (numbered steps)
5. **Verifiable Outcomes** (what files are created)
6. **Completion Requirements** (what to include in attempt_completion)

### 6.3 Group Permissions

Only request permissions you actually need:

- `read`: File reading only
- `edit`: File creation/modification
- `mcp`: External tool access
- `command`: Terminal command execution

### 6.4 Documentation

Include optional fields for clarity:

```yaml
version: "1.0.0"
description: "Brief one-liner describing the agent"
tags: ["category", "purpose", "workflow-phase"]
dependencies: ["agents-this-one-delegates-to"]
```

### 6.5 Testing Your Agent

Create a test scenario:

```bash
# 1. Validate structure
python tools/validate-agents.py agents/your-agent.yaml

# 2. Check dependencies
python tools/generate-dependency-graph.py

# 3. Review the graph
# Open docs/agent-dependency-graph.md

# 4. Test in practice
# Deploy and monitor in actual workflow
```

---

## Hands-On Exercise

Create your own agent by modifying the sample:

```bash
# 1. Copy the sample
cp agents/sample-code-quality-checker.yaml agents/my-custom-agent.yaml

# 2. Edit the file
# Change slug, name, roleDefinition, customInstructions

# 3. Validate
python tools/validate-agents.py agents/my-custom-agent.yaml

# 4. Generate graph
python tools/generate-dependency-graph.py

# 5. Review results
```

---

## Troubleshooting

### Python Not Found

```bash
# Try:
python --version
python3 --version
py --version

# Or use:
python -m pip install -r tools/requirements.txt
```

### Schema Not Found

Ensure you're running from the project root directory:

```bash
cd "c:/Users/jazbo/Documents/develop/AI Agents"
python tools/validate-agents.py
```

### Dependencies Missing

```bash
python -m pip install -r tools/requirements.txt --upgrade
```

### Graphviz Issues

For PNG/SVG generation:
1. Install Graphviz: https://graphviz.org/download/
2. Add to PATH
3. Or use Mermaid format (no dependencies)

---

## Next Steps

1. **Review Existing Agents**: Study the 45 production agents in `agents/` directory
2. **Read Validation Report**: Check [`validation_report.md`](../validation_report.md:1) for detailed analysis
3. **Explore Tooling**: Review [`tools/README.md`](../tools/README.md:1) for advanced features
4. **Memory Bank**: Check [`memory-bank/`](../memory-bank/) for project context

---

## Quick Reference Card

```bash
# Validate all agents
python tools/validate-agents.py

# Validate single agent
python tools/validate-agents.py agents/my-agent.yaml

# Generate dependency graph (Mermaid)
python tools/generate-dependency-graph.py

# Generate PNG/SVG
python tools/generate-dependency-graph.py --format png

# Help
python tools/validate-agents.py --help
python tools/generate-dependency-graph.py --help
```

## Schema Field Reference

| Field | Required | Type | Pattern/Values |
|-------|----------|------|----------------|
| `slug` | Yes | string | `[a-z0-9]+(-[a-z0-9]+)*` |
| `name` | Yes | string | Any |
| `roleDefinition` | Yes | string | Any |
| `customInstructions` | Yes | string | Any |
| `groups` | Yes | array | `read`, `edit`, `mcp`, `command` |
| `source` | Yes | string | Any |
| `version` | No | string | `X.Y.Z` (semver) |
| `description` | No | string | Any |
| `tags` | No | array | Any strings |
| `dependencies` | No | array | Valid agent slugs |

---

**Tutorial Complete!** You now know how to create, validate, and analyze custom agents for the SPARC orchestration system.