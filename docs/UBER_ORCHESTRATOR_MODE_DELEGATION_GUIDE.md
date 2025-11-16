# Uber-Orchestrator Mode Delegation Guide

## Overview

This guide explains how the [`uber-orchestrator`](../agents/uber-orchestrator.yaml) mode utilizes the 45+ custom global modes in the RooCode system to orchestrate complex software projects through the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology with Cognitive Triangulation.

## Core Concepts

### 1. RooCode Custom Mode Architecture

**Mode Definition Structure**:
```yaml
customModes:
  - slug: mode-identifier       # kebab-case unique ID
    name: 🎯 Display Name       # Human-readable with emoji
    roleDefinition: |           # Core purpose and responsibility
      High-level description
    customInstructions: |       # Detailed operational workflow
      Step-by-step instructions with mandatory protocols
    groups:                     # Permission levels
      - read                    # File reading
      - edit                    # File writing
      - mcp                     # External tools
      - command                 # Terminal execution
    source: project             # Source identifier
```

**Location**: All custom modes are defined in individual YAML files under [`agents/`](../agents/) directory.

### 2. Communication Protocol

**Mandatory Routing Headers**:
All mode-to-mode communication must include routing headers in `new_task` messages:

```
To: [recipient-agent-slug], From: [sender-agent-slug]
```

**Example**:
```
To: orchestrator-sparc-specification-phase, From: uber-orchestrator
```

This ensures complete traceability and accountability throughout the agent interaction chain.

### 3. Mode Delegation Tools

The uber-orchestrator uses these RooCode tools to orchestrate modes:

| Tool | Purpose | Usage |
|------|---------|-------|
| `new_task` | Delegate work to another mode | Primary delegation mechanism |
| `ask_followup_question` | Get user approval before delegation | Required before each major delegation |
| `attempt_completion` | Report results back to caller | Final step after delegation complete |
| `database-query` | Query `project_memory` table | Understand current project state |
| `read_file` | Read project documents | Context gathering |
| `switch_mode` | Switch to different mode (rare) | When mode change is needed |

## Uber-Orchestrator Workflow

### Phase 0: Initialization & Context Gathering

**Tools Used**: `database-query`, `read_file`

```yaml
Step 1: Query project state
  - Execute: SELECT * FROM project_memory
  - Load: docs/Mutual_Understanding_Document.md (if exists)
  - Load: docs/project_plan.md (if exists)

Step 2: Create Plan of Action
  - Generate comprehensive step-by-step plan
  - Document expected outcomes for each step
```

### Phase 1: Goal Clarification (Conditional)

**Trigger**: No Mutual Understanding Document exists

**Delegation Target**: [`orchestrator-goal-clarification`](../agents/orchestrator-goal-clarification.yaml)

**Process**:
```yaml
1. Use ask_followup_question:
   - Present plan: "I will delegate to orchestrator-goal-clarification to define project requirements"
   - Get user approval

2. Use new_task:
   To: orchestrator-goal-clarification, From: uber-orchestrator
   Message: |
     Conduct initial requirements gathering with the user.
     Your deliverables are:
     - docs/Mutual_Understanding_Document.md (user-validated success criteria)
     - Updated docs/project_plan.md (with agreed-upon tests/benchmarks)
     
3. Wait for attempt_completion from orchestrator-goal-clarification

4. Verify artifacts created:
   - Read docs/Mutual_Understanding_Document.md
   - Read docs/project_plan.md
```

**Sub-Delegations** (handled by orchestrator-goal-clarification):
- → [`research-planner-strategic`](../agents/research-planner-strategic.yaml): Deep research and project plan creation
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record foundational artifacts

### Phase 2: Triangulation Check #0 - Plan Validation

** Delegation Target**: [`devils-advocate-critical-evaluator`](../agents/devils-advocate-critical-evaluator.yaml)

**Purpose**: Validate project plan alignment with Simplicity Mandate

**Process**:
```yaml
1. Use ask_followup_question:
   - Present plan: "I will delegate to devils-advocate to verify the plan's alignment"
   - Get user approval

2. Use new_task:
   To: devils-advocate-critical-evaluator, From: uber-orchestrator
   Message: |
     Review docs/project_plan.md for:
     - Alignment with user's Core Intent
     - Technology stack simplicity
     - Unnecessary complexity
     
     PASS/FAIL verdict required. If FAIL, provide specific revisions needed.

3. Wait for attempt_completion

4. If FAIL: Loop back to revise plan
   If PASS: Proceed to Specification Phase
```

### Phase 3: SPARC Specification Phase

**Delegation Target**: [`orchestrator-sparc-specification-phase`](../agents/orchestrator-sparc-specification-phase.yaml)

**Process**:
```yaml
1. Use ask_followup_question:
   - Present plan: "I will delegate to specification phase orchestrator"
   - Get user approval

2. Use new_task:
   To: orchestrator-sparc-specification-phase, From: uber-orchestrator
   Message: |
     Create complete project specifications including:
     - Research findings
     - User stories with acceptance criteria
     - High-level test strategy
     - Master acceptance test plan
     - Granular component specifications
     
     Execute mandatory Triangulation Check via devils-advocate before completion.

3. Wait for attempt_completion
```

**Sub-Delegations** (handled by orchestrator-sparc-specification-phase):
- → [`research-planner-strategic`](../agents/research-planner-strategic.yaml): Research report
- → [`spec-writer-from-examples`](../agents/spec-writer-from-examples.yaml): User stories
- → [`researcher-high-level-tests`](../agents/researcher-high-level-tests.yaml): Testing strategy
- → [`tester-acceptance-plan-writer`](../agents/tester-acceptance-plan-writer.yaml): Acceptance tests
- → [`spec-writer-comprehensive`](../agents/spec-writer-comprehensive.yaml): Detailed specifications
- → [`devils-advocate-critical-evaluator`](../agents/devils-advocate-critical-evaluator.yaml): Triangulation check
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record artifacts

### Phase 4: SPARC Pseudocode Phase

**Delegation Target**: [`orchestrator-sparc-pseudocode-phase`](../agents/orchestrator-sparc-pseudocode-phase.yaml)

**Process**:
```yaml
1. Use ask_followup_question:
   - Present plan: "I will delegate to pseudocode phase orchestrator"
   - Get user approval

2. Use new_task:
   To: orchestrator-sparc-pseudocode-phase, From: uber-orchestrator
   Message: |
     Transform specifications into language-agnostic pseudocode.
     Required: devils-advocate Triangulation Check.

3. Wait for attempt_completion
```

**Sub-Delegations**:
- → [`pseudocode-writer`](../agents/pseudocode-writer.yaml): Create detailed pseudocode
- → [`devils-advocate-critical-evaluator`](../agents/devils-advocate-critical-evaluator.yaml): Verify pseudocode alignment
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record pseudocode

### Phase 5: SPARC Architecture Phase

**Delegation Target**: [`orchestrator-sparc-architecture-phase`](../agents/orchestrator-sparc-architecture-phase.yaml)

**Process**:
```yaml
1. Use ask_followup_question:
   - Present plan: "I will delegate to architecture phase orchestrator"
   - Get user approval

2. Use new_task:
   To: orchestrator-sparc-architecture-phase, From: uber-orchestrator
   Message: |
     Design high-level system architecture with resilience patterns.
     Required: devils-advocate Triangulation Check.

3. Wait for attempt_completion
```

**Sub-Delegations**:
- → [`architect-highlevel-module`](../agents/architect-highlevel-module.yaml): System design
- → [`devils-advocate-critical-evaluator`](../agents/devils-advocate-critical-evaluator.yaml): Verify architecture
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record architecture

### Phase 6: SPARC Refinement Loop (Iterative)

**For Each Feature**:

#### 6a. Testing Sub-Phase

**Delegation Target**: [`orchestrator-sparc-refinement-testing`](../agents/orchestrator-sparc-refinement-testing.yaml)

```yaml
1. Use ask_followup_question:
   - Present: "I will generate tests for Feature X"
   - Get approval

2. Use new_task:
   To: orchestrator-sparc-refinement-testing, From: uber-orchestrator
   Message: |
     Generate comprehensive test suite for [Feature Name].
     Use state-based TDD approach.

3. Wait for attempt_completion
```

**Sub-Delegations**:
- → [`spec-to-testplan-converter`](../agents/spec-to-testplan-converter.yaml): Convert specs to test plans
- → [`tester-tdd-master`](../agents/tester-tdd-master.yaml): Write actual tests
- → [`edge-case-synthesizer`](../agents/edge-case-synthesizer.yaml): Add edge case tests
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record tests

#### 6b. Implementation Sub-Phase

**Delegation Target**: [`orchestrator-sparc-refinement-implementation`](../agents/orchestrator-sparc-refinement-implementation.yaml)

```yaml
1. Use ask_followup_question:
   - Present: "I will implement Feature X using TDD"
   - Get approval

2. Use new_task:
   To: orchestrator-sparc-refinement-implementation, From: uber-orchestrator
   Message: |
     Implement [Feature Name] following TDD workflow.
     Tests must pass. RULER quality gate required.

3. Wait for attempt_completion
```

**Sub-Delegations**:
- → [`coder-test-driven`](../agents/coder-test-driven.yaml): Write implementation
- → [`ruler-quality-evaluator`](../agents/ruler-quality-evaluator.yaml): Evaluate multiple implementations
- → [`orchestrator-state-scribe`](../agents/orchestrator-state-scribe.yaml): Record code

### Phase 7: Ultimate Cognitive Triangulation

#### 7a. System Model Synthesis

**Delegation Target**: [`bmo-system-model-synthesizer`](../agents/bmo-system-model-synthesizer.yaml)

```yaml
1. Use ask_followup_question:
   - Present: "I will create comprehensive as-built system model"
   - Get approval

2. Use new_task:
   To: bmo-system-model-synthesizer, From: uber-orchestrator
   Message: |
     Analyze entire codebase and create as-built system model.
     Document all components, interactions, and data flows.

3. Wait for attempt_completion
```

#### 7b. Holistic Intent Verification

**Delegation Target**: [`bmo-holistic-intent-verifier`](../agents/bmo-holistic-intent-verifier.yaml)

```yaml
1. Use ask_followup_question:
   - Present: "I will perform final Cognitive Triangulation audit"
   - Get approval

2. Use new_task:
   To: bmo-holistic-intent-verifier, From: uber-orchestrator
   Message: |
     Verify complete alignment across:
     - User Core Intent
     - Specifications
     - Pseudocode
     - Architecture
     - Implementation
     - Tests
     
     Full PASS required on all triangulation points.

3. Wait for attempt_completion

4. If FAIL: Identify and fix misalignments
   If PASS: Proceed to final verification
```

### Phase 8: Final Multi-Method Simulation

**Delegation Target**: [`orchestrator-simulation-synthesis`](../agents/orchestrator-simulation-synthesis.yaml)

```yaml
1. Use ask_followup_question:
   - Present: "I will run comprehensive system simulation"
   - Get approval

2. Use new_task:
   To: orchestrator-simulation-synthesis, From: uber-orchestrator
   Message: |
     Execute multi-methodology system simulation:
     - Agent-Based Modeling
     - Discrete Event Simulation
     - Chaos Engineering
     - Property-Based Testing
     - Metamorphic Testing
     
     RULER quality verification required.

3. Wait for attempt_completion
```

**Sub-Delegations**:
- → [`simulation-worker-environment-setup`](../agents/simulation-worker-environment-setup.yaml)
- → [`simulation-worker-data-synthesizer`](../agents/simulation-worker-data-synthesizer.yaml)
- → [`simulation-worker-service-virtualizer`](../agents/simulation-worker-service-virtualizer.yaml)
- → [`simulation-worker-test-generator-multi-method`](../agents/simulation-worker-test-generator-multi-method.yaml)
- → [`ruler-quality-evaluator`](../agents/ruler-quality-evaluator.yaml)

### Phase 9: Completion

**Final Report**:
```yaml
Use attempt_completion:
  Summary: |
    SPARC workflow complete. Project successfully delivered.
    
    Phase Results:
    - ✅ Goal Clarification: MUD and plan validated
    - ✅ Specification: Comprehensive specs with user stories
    - ✅ Pseudocode: Language-agnostic blueprints
    - ✅ Architecture: Resilient system design
    - ✅ Refinement: All features implemented with TDD
    - ✅ Cognitive Triangulation: Full alignment verified
    - ✅ Simulation: Multi-method verification passed
    
    All triangulation checks: PASSED
    All quality gates: PASSED
    
    Deliverables:
    - Complete codebase in [location]
    - Test suite with [X]% coverage
    - Documentation in docs/
    - As-built system model
```

## Domain-Specific Modes

For specialized domains (e.g., financial trading), the uber-orchestrator may also delegate to:

### Financial System Modes

- [`calculator-performance-fee`](../agents/calculator-performance-fee.yaml): High-water mark fee calculation
- [`guardian-capital-preservation`](../agents/guardian-capital-preservation.yaml): Drawdown limit enforcement
- [`agent-reconciliation`](../agents/agent-reconciliation.yaml): Exchange state validation
- [`generator-client-portal`](../agents/generator-client-portal.yaml): P&L dashboard creation
- [`recorder-audit-trail`](../agents/recorder-audit-trail.yaml): Cryptographic event logging

### Quality & Security Modes

- [`auditor-concurrency-safety`](../agents/auditor-concurrency-safety.yaml): Race condition detection
- [`auditor-financial-logic`](../agents/auditor-financial-logic.yaml): Capital correctness validation
- [`security-reviewer-module`](../agents/security-reviewer-module.yaml): Security audit
- [`validator-performance-constraint`](../agents/validator-performance-constraint.yaml): Sub-100ms enforcement
- [`validator-api-integration`](../agents/validator-api-integration.yaml): External API verification

## Best Practices

### 1. Always Get User Approval

```yaml
Before each major delegation:
  1. Use ask_followup_question
  2. Explain what you're about to delegate
  3. Explain expected outcomes
  4. Wait for user approval
```

### 2. Comprehensive Delegation Messages

```yaml
new_task messages must include:
  - Routing header: "To: X, From: uber-orchestrator"
  - Clear objective
  - Expected deliverables (files, artifacts)
  - Success criteria
  - Any constraints or requirements
```

### 3. Verify Outcomes

```yaml
After each delegation:
  1. Wait for attempt_completion from delegated agent
  2. Read created artifacts to verify
  3. Update project state understanding
  4. Proceed only if outcomes are satisfactory
```

### 4. Maintain State Continuity

```yaml
Throughout workflow:
  - Query database regularly: SELECT * FROM project_memory
  - Read key documents before major decisions
  - Delegate to orchestrator-state-scribe to record milestones
```

### 5. Enforce Triangulation

```yaml
After each major phase:
  - Delegate to devils-advocate-critical-evaluator
  - Verify alignment with user Core Intent
  - Do NOT proceed if triangulation check fails
```

## Troubleshooting

### Delegation Not Working

**Issue**: Agent doesn't respond or errors occur

**Solutions**:
1. Verify agent slug is correct (check `agents/` directory)
2. Ensure routing header is present: `To: [slug], From: uber-orchestrator`
3. Check that message provides clear instructions and expected outcomes

### Triangulation Failures

**Issue**: devils-advocate reports misalignment

**Solutions**:
1. Read the devil's advocate report carefully
2. Identify specific misalignment points
3. Re-delegate to relevant agent with corrections
4. Re-run triangulation check
5. Do NOT proceed until PASS received

### Quality Gate Failures

**Issue**: RULER evaluation rejects implementation

**Solutions**:
1. Request multiple implementation trajectories
2. Use ruler-quality-evaluator to rank them
3. Select highest-scoring implementation
4. Re-test and re-evaluate

## Reference Diagram

```
┌─────────────────────────┐
│   Uber-Orchestrator     │
│  (Master Conductor)     │
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐    ┌─────────────┐
│  Goal   │    │  Cognitive  │
│Clarif.  │    │ Triangulation│
│ Orch.   │    │   (Devil's  │
└────┬────┘    │  Advocate)  │
     │         └──────────────┘
     ▼
┌──────────────────────┐
│ Research Planner     │
└──────────────────────┘
             │
    ┌────────┴──────────┐
    ▼                   ▼
┌─────────┐      ┌─────────────┐
│  SPARC  │      │    State    │
│ Phases  │◄────►│   Scribe    │
│  Orch.  │      │   (DB)      │
└────┬────┘      └─────────────┘
     │
     │    ┌──────────────┐
     ├───►│Specification │
     │    │    Phase     │
     │    └──────────────┘
     │
     │    ┌──────────────┐
     ├───►│  Pseudocode  │
     │    │    Phase     │
     │    └──────────────┘
     │
     │    ┌──────────────┐
     ├───►│ Architecture │
     │    │    Phase     │
     │    └──────────────┘
     │
     │    ┌──────────────┐
     ├───►│  Refinement  │
     │    │ Loop (TDD)   │
     │    └──────────────┘
     │
     ▼
┌──────────────────────┐
│   BMO Verification   │
│ (System Model +      │
│  Intent Verifier)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Simulation Synthesis │
│  (Multi-Method)      │
└──────────────────────┘
```

## Summary

The uber-orchestrator mode utilizes RooCode's custom mode system through:

1. **Sequential Delegation**: Using `new_task` to delegate work to phase-specific orchestrators
2. **User Approval**: Using `ask_followup_question` before each major delegation
3. **State Management**: Using `database-query` and `read_file` for context
4. **Verification**: Mandatory devils-advocate checks after each phase
5. **Quality Gates**: RULER-based evaluation of implementations
6. **Reporting**: Using `attempt_completion` with comprehensive summaries

This creates a robust, verifiable workflow that maintains alignment with user intent from initial requirements through final delivery.

---

**Related Documentation**:
- [Agent Dependency Graph](agent-dependency-graph.md)
- [Validation Report](../validation_report.md)
- [Tutorial](TUTORIAL.md)
- [Memory Bank](../memory-bank/)