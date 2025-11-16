# Custom Agents Orchestrator

A sophisticated AI Agent Orchestration System implementing the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology with advanced Cognitive Triangulation, RULER-based quality evaluation, and specialized domain agents.

## 🌟 Overview

This project coordinates multiple specialized AI agents to collaboratively design, implement, test, and validate complex software projects through a structured, verifiable workflow that ensures alignment with user intent at every stage.

## ✨ Key Features

### 🏗️ SPARC Methodology Framework
- **Specification Phase**: Comprehensive requirements gathering and acceptance criteria
- **Pseudocode Phase**: Language-agnostic logical blueprints
- **Architecture Phase**: High-level system design with resilience patterns
- **Refinement Phase**: Iterative TDD implementation with quality gates
- **Completion Phase**: Documentation, maintenance, and final verification

### 🔀 Cognitive Triangulation
Multi-stage verification ensuring alignment between:
- User's Core Intent → User Stories → Specifications → Pseudocode → Architecture → Implementation → Tests
- Enforced by the Devil's Advocate agent at critical checkpoints
- Prevents requirement drift and ensures implementation fidelity

### 📊 RULER Quality Evaluation
- LLM-as-Judge methodology for comparative quality assessment
- Generates multiple implementation trajectories
- Ranks solutions based on efficiency, clarity, and maintainability
- Ensures optimal implementation selection

### 🤖 46 Specialized Agent Modes

#### Orchestrators (11 agents)
- **uber-orchestrator**: Master conductor managing overall project flow
- **orchestrator-goal-clarification**: Intent validation and synthesis
- **orchestrator-sparc-*-phase**: Phase-specific coordinators (Specification, Pseudocode, Architecture)
- **orchestrator-sparc-refinement-***: Testing and implementation managers
- **orchestrator-sparc-completion-***: Documentation and maintenance coordinators
- **orchestrator-simulation-synthesis**: Multi-method verification orchestrator
- **orchestrator-state-scribe**: Intelligent state interpreter and recorder

#### Workers (9 agents)
- **spec-writer-comprehensive**: Modular specification creation
- **spec-writer-from-examples**: User story extraction from examples
- **pseudocode-writer**: Detailed logic blueprints
- **coder-test-driven**: TDD implementation specialist
- **coder-framework-boilerplate**: Project scaffolding generator
- **tester-tdd-master**: Test implementation expert
- **tester-acceptance-plan-writer**: High-level test strategy
- **docs-writer-feature**: Feature documentation specialist
- **research-planner-strategic**: Adaptive multi-arc research strategist

#### Validators & Auditors (5 agents)
- **devils-advocate-critical-evaluator**: Cognitive Triangulation enforcer
- **auditor-concurrency-safety**: Race condition detector
- **auditor-financial-logic**: Capital & risk validator
- **validator-api-integration**: External dependency verifier
- **validator-performance-constraint**: Sub-100ms latency enforcer

#### Quality & Analysis (4 agents)
- **ruler-quality-evaluator**: LLM-as-judge quality arbiter
- **bmo-system-model-synthesizer**: As-built system documentation
- **bmo-holistic-intent-verifier**: Final triangulation verifier
- **optimizer-module**: Code quality and performance enhancement

#### Domain Specialists (17 agents)
Financial trading and specialized vertical agents including performance fee calculators, client portal generators, audit trail recorders, and more.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+ (for validation tooling)
- Git
- RooCode or compatible AI coding assistant

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/custom-agents-orchestrator.git
cd custom-agents-orchestrator
```

2. Install Python dependencies for tooling:
```bash
pip install -r tools/requirements.txt
```

3. (Optional) Validate agent definitions:
```bash
python tools/validate-agents.py
```

## 📁 Project Structure

```
custom-agents-orchestrator/
├── agents/                    # 46 agent YAML definitions
├── docs/                      # Documentation
│   ├── research/             # Research findings and decisions
│   ├── TUTORIAL.md          # Interactive tutorial
│   ├── UBER_ORCHESTRATOR_MODE_DELEGATION_GUIDE.md
│   └── project_plan.md      # Implementation roadmap
├── memory-bank/              # Project context and state
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── decisionLog.md
│   └── progress.md
├── schemas/                  # JSON Schema for validation
│   └── agent-mode-schema.json
├── tools/                    # Validation and analysis tools
│   ├── validate-agents.py
│   ├── generate-dependency-graph.py
│   └── merge-agents.py
├── SETUP_GUIDE.md           # Detailed setup instructions
└── validation_report.md     # Agent validation results
```

## 🛠️ Usage

### Working with Agent Modes

All 46 agent modes are defined in the `agents/` directory as YAML files. Each agent has:
- Unique slug identifier
- Role definition
- Custom instructions
- Group permissions
- Communication protocols

### Validation Tools

**Validate all agents:**
```bash
python tools/validate-agents.py
```

**Generate dependency graph:**
```bash
python tools/generate-dependency-graph.py
```

**Merge agents for RooCode:**
```bash
python tools/merge-agents.py
```

### Agent Communication Protocol

All agents use standardized routing headers:
```
To: [recipient-agent-slug]
From: [sender-agent-slug]
```

## 📚 Documentation

- **[Tutorial](docs/TUTORIAL.md)**: Interactive guide to creating and validating agents
- **[Uber Orchestrator Guide](docs/UBER_ORCHESTRATOR_MODE_DELEGATION_GUIDE.md)**: Complete workflow documentation
- **[Setup Guide](SETUP_GUIDE.md)**: Detailed installation and configuration
- **[Project Plan](docs/project_plan.md)**: V2 implementation roadmap
- **[Agent Dependency Graph](docs/agent-dependency-graph.md)**: Visual workflow representation

## 🔄 Workflow

1. **Goal Clarification**: uber-orchestrator → orchestrator-goal-clarification
2. **Research & Planning**: → research-planner-strategic
3. **Triangulation Check #0**: → devils-advocate-critical-evaluator
4. **Specification Phase**: → orchestrator-sparc-specification-phase
5. **Pseudocode Phase**: → orchestrator-sparc-pseudocode-phase
6. **Architecture Phase**: → orchestrator-sparc-architecture-phase
7. **Refinement Loop** (per feature):
   - orchestrator-sparc-refinement-testing
   - orchestrator-sparc-refinement-implementation
8. **Ultimate Triangulation Audit**:
   - bmo-system-model-synthesizer
   - bmo-holistic-intent-verifier
9. **Final Verification**: → orchestrator-simulation-synthesis

## 🧪 Testing Strategy

- **State-Based Classical TDD**: Focus on observable outcomes
- **Multi-Methodology**: Unit, Integration, Property-Based, Chaos, Metamorphic
- **No Mock Internal Collaborators**: Maximize refactoring flexibility
- **Comprehensive Coverage**: Edge cases, error scenarios, performance constraints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Validate your changes (`python tools/validate-agents.py`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📊 Project Status

- ✅ Phase 1: Agent Definition & Validation (Complete)
- ✅ Validation Tooling (Complete)
- ✅ Documentation & Tutorial (Complete)
- ✅ RooCode Integration (Complete)
- 🔄 Phase 2: Full Automation via Anthropic API (In Planning)

See [V2_IMPLEMENTATION_STATUS.md](docs/V2_IMPLEMENTATION_STATUS.md) for detailed progress.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built on the SPARC methodology
- Implements Cognitive Triangulation principles
- Uses RULER (LLM-as-Judge) quality evaluation
- Powered by RooCode AI coding assistant

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Note**: This is an intelligent orchestration system for AI-assisted software development. It requires understanding of AI agent workflows and the SPARC methodology for effective use.