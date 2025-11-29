# Agent Orchestration Patterns - Complete Implementation Guide

## Overview

This guide documents the 5-point solution strategy for resolving the 46-agent orchestration challenges in RooCode, based on the Cognitive Triangulation workflow and SPARC methodology.

## Solution 1: 5-Step Task Decomposition Pattern

### The Pattern

Every uber-orchestrator task must follow this atomic decomposition:

```
PHASE 1: GOAL CLARIFICATION (5 min)
├── Input: Raw user request
├── Tool: ask_followup_question (max 3 suggestions)
├── Agent: uber-orchestrator
└── Output: Clarified requirements document

PHASE 2: MODE SELECTION (Atomic)
├── Input: Clarified requirements
├── Decision: Which 2-3 agents needed?
├── Agent: uber-orchestrator
└── Output: Agent selection rationale

PHASE 3: SEQUENTIAL DELEGATION (No parallelization)
├── Agent 1: execute (complete before moving to Agent 2)
├── Agent 1 completes (routing header confirmation)
├── Agent 2: execute (complete before moving to Agent 3)
├── Agent 2 completes (routing header confirmation)
└── (Continue sequentially for all selected agents)

PHASE 4: SYNTHESIS (SINGLE AGENT)
├── Input: All results
├── Tool: attempt_completion with routing header
├── Agent: uber-orchestrator
└── Output: Final deliverable
```

### Why This Works

- Reduces concurrent agent coordination from 46 to 2-3 agents
- Explicit step structure prevents "thought process failure" errors
- RooCode can track intermediate completion states
- Fits within Haiku model token budget (~90K tokens)

### Example Implementation

```yaml
Task: Implement authentication feature

Step 1: Goal Clarification
  Request: "Implement JWT-based authentication for REST API"
  Questions:
    - Should we support refresh tokens?
    - What's the token expiration policy?
    - Do we need multi-factor authentication?
  Output: requirements.md

Step 2: Mode Selection
  Decision: orchestrator-sparc-specification-phase + spec-writer-comprehensive
  Rationale: User intent is clear, can proceed directly to detailed specification

Step 3: Sequential Delegation
  Agent 1: spec-writer-comprehensive
    Input: requirements.md
    Task: Create detailed specification with acceptance criteria
    Output: spec.md
    
  Agent 2: pseudocode-writer
    Input: spec.md
    Task: Create language-agnostic implementation blueprint
    Output: pseudocode.md

Step 4: Synthesis
  uber-orchestrator collects all outputs
  Creates final deliverable package
  Returns to user with routing header
```

## Solution 2: User Guidance Pattern

### Standard Instructions Format

```
[EXECUTION PATTERN]

Step 1: Initialize Context
  - Read memory bank files (list specific files)
  - Query project state (list specific tables/queries)
  - Load relevant specifications (list file paths)

Step 2: Analyze Requirements
  - Validate alignment with core intent
  - Identify potential conflicts
  - Document assumptions

Step 3: Create Primary Output
  - File: output/filename.md
  - Format: markdown/json/yaml
  - Content requirements: (list 3-5 specific items)

Step 4: Update Memory Bank
  - File: memory-bank/decisionLog.md
  - Entry: "[YYYY-MM-DD HH:MM:SS] - [summary]"
  - Include: Rationale and implications

Step 5: Return Results
  - Summary: 2-3 sentence recap
  - Use routing header: To: next-agent, From: current-agent
```

### DO NOT Use

❌ "Research X and analyze Y"
❌ "Think about Z and suggest improvements"
❌ "Create something that meets criteria A, B, and C"

### DO Use

✅ "Read spec.md and pseudocode.md. Then create architecture.md with 4 sections: (1) Component diagram, (2) Data flow, (3) Error handling, (4) Performance constraints."

✅ "Query memory.db for all decisions related to feature_flag_system. Document findings in memory-bank/decisionLog.md with timestamp [2025-11-19 HH:MM:SS]."

✅ "Create test_plan.md with: (1) Unit test strategy, (2) Integration test scenarios, (3) Performance benchmarks, (4) Edge cases."

## Solution 3: Agent Selection Matrix

### By SPARC Phase

| Phase | Required Agents | Count | Dependencies |
|-------|-----------------|-------|--------------|
| **Goal Clarification** | uber-orchestrator, orchestrator-goal-clarification, devils-advocate-critical-evaluator | 3 | None |
| **Specification** | orchestrator-sparc-specification-phase, spec-writer-comprehensive, edge-case-synthesizer, researcher-high-level-tests | 4 | Goal clarification complete |
| **Pseudocode** | orchestrator-sparc-pseudocode-phase, pseudocode-writer, code-comprehension-assistant-v2 | 3 | Specification complete |
| **Architecture** | orchestrator-sparc-architecture-phase, architect-highlevel-module, security-reviewer-module, validator-performance-constraint | 4 | Pseudocode complete |
| **Implementation** | orchestrator-sparc-refinement-testing, orchestrator-sparc-refinement-implementation, coder-test-driven, tester-tdd-master, debugger-targeted | 5 | Architecture complete |
| **Quality** | orchestrator-simulation-synthesis, ruler-quality-evaluator, bmo-holistic-intent-verifier, bmo-system-model-synthesizer | 4 | Implementation complete |

**Total per cycle**: 6-9 agents active (manageable cognitive load for Haiku)

### Agents to Avoid Using Simultaneously

❌ Multiple orchestrators in same phase
❌ All 46 agents at once
❌ More than 5 agents without state checkpoints
❌ Agents from different phases without intermediate synthesis

### Recommended Groupings

**Quality Gate Sequence** (After Implementation):
1. bmo-system-model-synthesizer (reverse-engineer and document)
2. bmo-holistic-intent-verifier (verify alignment)
3. ruler-quality-evaluator (compare alternatives)
4. orchestrator-simulation-synthesis (final verification)

## Solution 4: MCP Server Configuration

### File Location

`C:\Users\jazbo\AppData\Roaming\Roo-Code\mcp_settings.json`

### Correct Configuration

```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": [
        "C:\\Users\\jazbo\\AppData\\Roaming\\Roo-Code\\MCP\\custom-agents-orchestrator\\build\\index.js"
      ],
      "env": {
        "AGENTS_DIR": "C:\\Users\\jazbo\\Documents\\develop\\AI Agents\\agents",
        "MEMORY_DB": "C:\\Users\\jazbo\\Documents\\develop\\AI Agents\\memory.db",
        "NODE_ENV": "production"
      },
      "disabled": false
    }
  }
}
```

### Critical Points

1. **Absolute paths only** - No relative paths (causes working directory sensitivity)
2. **Backslashes escaped** - Use `\\` in JSON strings for Windows paths
3. **Both env vars required** - AGENTS_DIR and MEMORY_DB
4. **NODE_ENV=production** - Enables error handling and logging

### MCP Server Code Fix

In `C:\Users\jazbo\AppData\Roaming\Roo-Code\MCP\custom-agents-orchestrator\build\index.ts`:

```typescript
// Add at initialization
const agentsDir = process.env.AGENTS_DIR || 
  path.resolve(__dirname, '../../agents');
const memoryDb = process.env.MEMORY_DB || 
  path.resolve(__dirname, '../../memory.db');

// Validate with helpful errors
if (!fs.existsSync(agentsDir)) {
  console.error(`ERROR: AGENTS_DIR not found at ${agentsDir}`);
  console.error(`Set AGENTS_DIR env var to: C:\\Users\\jazbo\\Documents\\develop\\AI Agents\\agents`);
  process.exit(1);
}

if (!fs.existsSync(memoryDb)) {
  console.error(`ERROR: MEMORY_DB not found at ${memoryDb}`);
  console.error(`Ensure memory.db exists in: C:\\Users\\jazbo\\Documents\\develop\\AI Agents\\`);
  process.exit(1);
}
```

## Solution 5: Routing Header Standardization

### Format (MANDATORY)

```
To: [target-agent-slug], From: [current-agent-slug]
```

### Usage in attempt_completion

```markdown
To: orchestrator-sparc-specification-phase, From: uber-orchestrator

Goal clarification complete. Requirements validated and documented in requirements.md.

Key findings:
- User intent: Implement JWT authentication
- Constraints: Sub-100ms latency requirement
- Dependencies: 3 external integrations

Proceeding to specification phase.
```

### Usage in new_task Message

```yaml
To: spec-writer-comprehensive, From: orchestrator-sparc-specification-phase

Task: Create detailed specification

Input files:
- requirements.md
- architecture-context.md

Deliverables:
- spec.md (detailed requirements with acceptance criteria)
- user-stories.md (user-facing requirements)
- test-plan.md (initial test strategy)
```

### Validation Rules

✅ **ALWAYS**:
- Include routing header at message start
- Use exact slug from agent YAML file
- End with period after slug

❌ **NEVER**:
- Skip routing header in inter-agent communication
- Use agent name instead of slug
- Mix "To" and "From" order
- Use incomplete slugs

## Solution 6: Best Practices & Anti-Patterns

### ✅ DO

1. **Provide explicit file references**
   - "Read spec.md lines 1-45"
   - "Query memory.db: SELECT * FROM project_memory WHERE feature='auth'"
   - NOT "think about the specification"

2. **Use 3-5 step sequences**
   - Sequential not parallel
   - Each step has clear input/output
   - Intermediate checkpoints

3. **Update memory bank between phases**
   - `decisionLog.md` for architectural decisions
   - `activeContext.md` for focus changes
   - `progress.md` for task completion

4. **Include routing headers**
   - All agent-to-agent communication
   - All completion messages
   - Format: "To: slug, From: slug"

5. **Group agents by phase**
   - Goal Clarification: 3 agents max
   - Specification: 4 agents max
   - Pseudocode: 3 agents max
   - Implementation: 5 agents max
   - Quality: 4 agents max

### ❌ DON'T

1. **Avoid vague instructions**
   - ❌ "Analyze the system"
   - ✅ "Create architecture.md with 4 sections: (1) Components, (2) Data flow, (3) Error handling, (4) Performance"

2. **Don't delegate all 46 agents**
   - ❌ "Delegate to all orchestrator agents"
   - ✅ "Delegate to orchestrator-sparc-specification-phase"

3. **Don't skip routing headers**
   - ❌ "Here's the result..."
   - ✅ "To: orchestrator-sparc-specification-phase, From: uber-orchestrator\n\nHere's the result..."

4. **Don't use relative paths**
   - ❌ `./agents/spec-writer.yaml`
   - ✅ `C:\Users\jazbo\Documents\develop\AI Agents\agents\spec-writer.yaml`

5. **Don't assume context transfer**
   - ❌ Send agent name alone
   - ✅ "Read spec.md for context before creating pseudocode.md"

## Implementation Checklist

- [ ] MCP server configuration updated with absolute paths
- [ ] uber-orchestrator.yaml updated with 5-step decomposition pattern
- [ ] Agent selection matrix documented in memory-bank/activeContext.md
- [ ] Routing header format enforced in all completions
- [ ] docs/AGENT_ORCHESTRATION_PATTERNS.md created (this file)
- [ ] Test with single agent (orchestrator-goal-clarification) only
- [ ] Run full SPARC cycle with 9 agents (3 per major phase)
- [ ] Monitor for "thought process failure" errors
- [ ] Create delegation workflows for common task types
- [ ] Update memory bank with completion status

## Success Metrics

✅ **Zero** "thought process failure" errors in 10 consecutive tasks
✅ **Agent delegation** completes within expected token limits (<100K)
✅ **Memory bank updates** captured for all phase transitions
✅ **Routing headers** present in 100% of inter-agent communications
✅ **Sub-10 minute** execution per SPARC phase

---

**Last Updated**: [2025-11-19 16:35:00]
**Status**: Implementation Guide Complete
**Next Step**: Apply solutions to uber-orchestrator.yaml and test with single agent