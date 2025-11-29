# RooCode 46-Agent Orchestration: Complete Solutions Guide

## Executive Summary

Your error "Roo is having trouble... failure in the model's thought process or inability to use a tool properly" indicates critical issues with agent synchronization and delegation in RooCode when managing 46 custom agents. This guide provides comprehensive solutions based on your SPARC methodology architecture.

## Root Cause Analysis

### Primary Issues

1. **Task Decomposition Failure**
   - 46 agents exceeds cognitive load for single delegation
   - RooCode's default thought process struggles with complex orchestration
   - Missing step-by-step task breakdown guidance

2. **Context Window Overflow**
   - Agent YAML files + custom instructions exceed token limits
   - Routing header validation consuming processing overhead
   - Signal interpretation framework creating decision paralysis

3. **Delegation Chain Breakdown**
   - Uber-orchestrator attempting direct delegation to all 46 agents
   - No intermediate aggregation layer
   - Missing state persistence between delegations

### Secondary Issues

4. **Tool Usage Pattern Mismatch**
   - `new_task` tool invocations not following RooCode's expected structure
   - Missing explicit step numbers in user guidance
   - Inadequate error context in attempt_completion messages

5. **MCP Server Configuration**
   - Environment variables (AGENTS_DIR, MEMORY_DB) not properly configured
   - Fallback paths using relative directories causing failures
   - No circuit breaker for missing agent definitions

## Solution Strategy: 5-Point Approach

### 1. Task Decomposition Pattern

**Implementation**:
Break every uber-orchestrator task into atomic 3-5 step sequences:

```yaml
Phase 1: Goal Clarification (SINGLE STEP)
- Input: User request
- Tool: ask_followup_question (max 3 suggestions)
- Output: Clarified requirements document

Phase 2: Mode Selection (ATOMIC)
- Input: Clarified requirements
- Decision: Which 2-3 agents needed?
- Output: Agent selection rationale

Phase 3: Delegation (SEQUENTIAL, not parallel)
- Agent 1: execute
- Agent 1 completes
- Agent 2: execute
- Agent 2 completes
- (etc.)

Phase 4: Synthesis (SINGLE AGENT)
- Input: All results
- Tool: attempt_completion with routing header
- Output: Final deliverable
```

**Why this works**:
- Reduces concurrent agent coordination from 46 to 2-3
- Explicit step structure prevents "thought process failure"
- RooCode can track intermediate completion states

### 2. User Guidance Pattern

**For Custom Agents**: Always provide explicit instructions:

```
[EXECUTION PATTERN]
Step 1: Read memory bank files sequentially
- File A
- File B  
- File C
Step 2: Analyze findings
Step 3: Create one output file
Step 4: Update memory bank with decision log entry
Step 5: Return to user with summary
```

**Instead of**:
```
Research RooCode agent orchestration
```

**Result**: Haiku model stays within decision boundaries, completes tasks successfully

### 3. Agent Selection Matrix

**Don't use all 46 simultaneously**. Group by phase:

| Phase | Required Agents | Count | Notes |
|-------|-----------------|-------|-------|
| Goal Clarification | uber-orchestrator, orchestrator-goal-clarification, devils-advocate | 3 | User intent validation |
| Specification | spec-writer-comprehensive, edge-case-synthesizer, researcher-high-level-tests | 3 | Detailed requirements |
| Pseudocode | pseudocode-writer, code-comprehension-assistant-v2, bmo-system-model-synthesizer | 3 | Language-agnostic logic |
| Architecture | architect-highlevel-module, security-reviewer-module, performance-constraint-validator | 3 | System design |
| Implementation | coder-test-driven, tester-tdd-master, debugger-targeted | 3 | Code delivery |
| Quality | ruler-quality-evaluator, bmo-holistic-intent-verifier, sample-code-quality-checker | 3 | Final validation |
| **Total Active** | | **6-9 per phase** | Manageable cognitive load |

**Inactive agents** remain registered for future use but aren't delegated to unless explicitly needed.

### 4. MCP Server Configuration Fix

**Location**: `C:\Users\jazbo\AppData\Roaming\Roo-Code\mcp_settings.json`

**Current Problem**:
```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": ["path/to/index.js"],
      "env": {
        // Missing AGENTS_DIR and MEMORY_DB
      }
    }
  }
}
```

**Solution**:
```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": ["C:\\Users\\jazbo\\AppData\\Roaming\\Roo-Code\\MCP\\custom-agents-orchestrator\\build\\index.js"],
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

**Required MCP Server Code Fix** (`index.ts`):
```typescript
// Add absolute path fallback
const agentsDir = process.env.AGENTS_DIR || 
  path.resolve(__dirname, '../../agents');
const memoryDb = process.env.MEMORY_DB || 
  path.resolve(__dirname, '../../memory.db');

// Add validation with helpful errors
if (!fs.existsSync(agentsDir)) {
  console.error(`ERROR: AGENTS_DIR not found at ${agentsDir}`);
  console.error(`Set AGENTS_DIR env var or check MCP configuration`);
  process.exit(1);
}
```

### 5. Routing Header Standardization

**Every agent-to-agent communication must follow this pattern**:

In `attempt_completion`:
```
To: [target-agent-slug], From: [current-agent-slug]

[Actual result content here]
```

Example:
```
To: ruler-quality-evaluator, From: coder-test-driven

Code implementation completed for user story #42.
[... implementation details ...]
```

**For orchestrators**: Always include routing in new_task payloads:
```yaml
new_task:
  mode: code-comprehension-assistant-v2
  message: |
    To: bmo-system-model-synthesizer, From: orchestrator-sparc-architecture-phase
    
    Task: Synthesize architecture from pseudocode
    Context: [provide spec/pseudocode]
```

## Implementation Roadmap

### Week 1: Foundation
- [ ] Update MCP server configuration
- [ ] Implement 5-step task decomposition in uber-orchestrator
- [ ] Create agent selection matrix in docs
- [ ] Test with single phase (Goal Clarification)

### Week 2: Validation
- [ ] Run full SPARC cycle with 9 agents (one per phase section)
- [ ] Monitor for "thought process failure" errors
- [ ] Adjust decomposition if errors persist
- [ ] Document patterns in docs/AGENT_ORCHESTRATION_PATTERNS.md

### Week 3: Scale
- [ ] Activate additional 10-15 agents by role
- [ ] Create delegation workflows for each major task type
- [ ] Build runbooks for common error scenarios
- [ ] Update tutorial with successful examples

## Error Troubleshooting

### "Roo is having trouble..." appears when:

1. **> 5 agents delegated concurrently**
   - Solution: Use decomposition pattern, delegate sequentially

2. **Routing headers malformed**
   - Solution: Always use "To: slug, From: slug" format exactly

3. **AGENTS_DIR/MEMORY_DB not configured**
   - Solution: Apply MCP configuration fix above

4. **Context exceeds 100K tokens**
   - Solution: Split into phases, use references instead of full content

5. **Multiple overlapping new_task calls**
   - Solution: Ensure sequential completion, check memory bank before next step

## Best Practices

### DO:
- ✅ Provide explicit step-by-step instructions
- ✅ Use 3-5 step task decomposition
- ✅ Include routing headers in all completions
- ✅ Update memory bank between phases
- ✅ Group agents by SPARC phase
- ✅ Test single agent before orchestration

### DON'T:
- ❌ Delegate to all 46 agents simultaneously
- ❌ Use vague instructions ("research X", "analyze Y")
- ❌ Omit routing headers from completion messages
- ❌ Skip memory bank updates between agent handoffs
- ❌ Assume agents know context without explicit file references
- ❌ Use relative paths in MCP configuration

## Quick Reference: Minimal Working Example

```yaml
Task: Implement new feature for trading system

Step 1: Goal Clarification (5 min)
  Agent: uber-orchestrator
  Instructions: 
    - Read user requirements
    - Ask 2-3 clarification questions
    - Produce requirements.md
  Completion: 
    "To: orchestrator-sparc-specification-phase, From: uber-orchestrator
     Requirements clarified and documented."

Step 2: Specification (10 min)
  Agent: orchestrator-sparc-specification-phase
  Instructions:
    - Read requirements.md
    - Delegate to spec-writer-comprehensive
    - Collect output
  Completion:
    "To: orchestrator-sparc-pseudocode-phase, From: orchestrator-sparc-specification-phase
     Specification complete: spec.md"

Step 3: [Continue sequentially...]

Result: No "thought process failure", clear delegation chain, documented handoffs
```

## Configuration Checklist

- [ ] MCP server environment variables set
- [ ] Agent YAML files in agents/ directory (46 total)
- [ ] memory.db accessible and writable
- [ ] memory-bank/ files synchronized
- [ ] 5-step decomposition implemented in uber-orchestrator.yaml
- [ ] Routing headers enforced in all completions
- [ ] User instructions include explicit step numbers
- [ ] Testing started with Phase 1 agents only

## Metrics for Success

✅ **No "thought process failure" errors in 10 consecutive tasks**
✅ **Agent delegation completes within expected token limits**
✅ **Memory bank updates captured for all phase transitions**
✅ **Routing headers present in 100% of inter-agent communications**
✅ **Sub-10 minute execution per SPARC phase**

---

**Next Action**: Apply MCP configuration fix and update uber-orchestrator.yaml with 5-step decomposition pattern. Test with orchestrator-goal-clarification agent only before proceeding to full SPARC cycle.
