# Product Context

## Project Overview
This project implements a sophisticated AI Agent Orchestration System based on the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology with advanced Cognitive Triangulation, RULER-based quality evaluation, and specialized domain agents.

## Core Purpose
The system coordinates multiple specialized AI agents to collaboratively design, implement, test, and validate complex software projects through a structured, verifiable workflow that ensures alignment with user intent at every stage.

## Key Features

### 1. SPARC Methodology Framework
- **Specification Phase**: Comprehensive requirements gathering, user stories, and acceptance criteria
- **Pseudocode Phase**: Language-agnostic logical blueprints
- **Architecture Phase**: High-level system design with resilience patterns
- **Refinement Phase**: Iterative TDD implementation with quality gates
- **Completion Phase**: Documentation, maintenance, and final verification

### 2. Cognitive Triangulation
- Multi-stage verification ensuring alignment between:
  - User's Core Intent
  - Specifications
  - Pseudocode
  - Architecture
  - Implementation
  - Tests
- Enforced by the Devil's Advocate agent at critical checkpoints

### 3. RULER Quality Evaluation
- LLM-as-Judge methodology for comparative quality assessment
- Generates multiple implementation trajectories
- Ranks solutions based on efficiency, clarity, maintainability
- Ensures optimal implementation selection

### 4. Specialized Domain Agents
Financial trading system specialists including:
- Performance Constraint Validator (sub-100ms latency)
- Financial Logic Auditor (capital preservation)
- Concurrency Safety Auditor (race condition detection)
- Performance Fee Calculator (high-water mark tracking)
- Client Portal Generator (transparency dashboard)
- Audit Trail Recorder (cryptographic logging)
- Capital Preservation Guardian (drawdown limits)
- Reconciliation Agent (exchange state validation)

### 5. State Management
- SQLite-based project memory (memory.db)
- Signal Interpretation Framework for context-aware event categorization
- Intelligent State Scribe for comprehensive project history

## Technology Stack
- Agent Definitions: YAML format
- Database: SQLite (memory.db)
- Documentation: Markdown
- Testing: Multi-methodology (TDD, Property-Based, Chaos, Metamorphic)

## Target Use Cases
1. Complex software project development
2. Financial trading system implementation
3. Multi-account management systems
4. High-reliability, low-latency applications
5. Systems requiring rigorous audit trails

## Success Criteria
- Complete workflow from user intent to verified implementation
- 100% traceability between requirements and code
- Automated quality gates preventing suboptimal implementations
- Comprehensive audit trail for all decisions and changes
- Alignment verification at every major phase transition

---
[2025-11-14 20:35:00] - Initial Memory Bank creation for AI Agent Orchestration System project