# Python Setup Guide for Agent Validation Tools

## Current Status
Python is not currently installed on your Windows system. The validation and analysis tools have been created but require Python 3.7 or higher to execute.

## Installation Options

### Option 1: Microsoft Store (Recommended for Windows 11)
1. Open Microsoft Store
2. Search for "Python 3.12" (or latest version)
3. Click "Get" to install
4. Verify installation: Open Command Prompt and run `python --version`

### Option 2: Python.org Installer
1. Visit https://www.python.org/downloads/
2. Download Python 3.12.x (latest stable version)
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Complete installation
6. Verify installation: Open Command Prompt and run `python --version`

### Option 3: Chocolatey (If you use package managers)
```powershell
choco install python
```

## Post-Installation Steps

### 1. Install Required Dependencies
```bash
cd "c:/Users/jazbo/Documents/develop/AI Agents"
pip install -r tools/requirements.txt
```

This will install:
- jsonschema (JSON Schema validation)
- PyYAML (YAML parsing)
- graphviz (Graph generation)
- pydot (Graph manipulation)
- colorama (Colored terminal output)
- rich (Rich text formatting)

### 2. Validate All Agents
```bash
# Validate all 45 agent YAML files
python tools/validate-agents.py

# Validate a single agent
python tools/validate-agents.py agents/uber-orchestrator.yaml
```

### 3. Generate Dependency Graph
```bash
# Generate Mermaid format (no extra dependencies)
python tools/generate-dependency-graph.py

# Generate PNG/SVG (requires graphviz system package)
python tools/generate-dependency-graph.py --format png
```

## Expected Validation Results

Based on the comprehensive validation report, all 45 agents should pass validation:
- ✅ Structural validation (JSON Schema compliance)
- ✅ Communication protocol verification (To:/From: headers)
- ✅ Signal Framework validation (for orchestrator-state-scribe)
- ✅ No critical issues detected

## Troubleshooting

### Python Not Found After Installation
1. Restart Command Prompt/Terminal
2. Check PATH environment variable
3. Try `py` command instead of `python`

### Graphviz Issues for Graph Generation
If PNG/SVG generation fails:
1. Install Graphviz system package from https://graphviz.org/download/
2. Add Graphviz bin directory to PATH
3. Or use Mermaid format (no dependencies): `python tools/generate-dependency-graph.py --format mermaid`

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r tools/requirements.txt --upgrade
```

## Verification Checklist

- [ ] Python 3.7+ installed and in PATH
- [ ] Dependencies installed via pip
- [ ] Validator runs successfully: `python tools/validate-agents.py`
- [ ] All 45 agents pass validation
- [ ] Dependency graph generated: `python tools/generate-dependency-graph.py`
- [ ] Review validation_report.md for detailed analysis

## Next Steps After Setup

1. **Run Full Validation**: Confirm all 45 agents pass
2. **Generate Dependency Graph**: Visualize orchestration workflow
3. **Review Validation Report**: Check [`validation_report.md`](validation_report.md:1)
4. **Optional Enhancements**: Consider future tools from tools/README.md

## Support Resources

- Python Documentation: https://docs.python.org/3/
- Tools Documentation: [`tools/README.md`](tools/README.md:1)
- Validation Report: [`validation_report.md`](validation_report.md:1)
- Memory Bank: [`memory-bank/`](memory-bank/)

## Quick Reference

```bash
# Complete setup sequence
python --version                              # Verify Python installation
pip install -r tools/requirements.txt         # Install dependencies
python tools/validate-agents.py               # Validate all agents
python tools/generate-dependency-graph.py     # Generate workflow graph
```

All tools are ready to use once Python is installed!