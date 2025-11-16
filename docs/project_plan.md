# Agent Automation V2 Implementation Plan

## Project Overview

**Goal**: Transform the Custom Agents Orchestrator from V1 (simulation-only) to V2 (fully automated AI-to-AI execution) using Claude Agent SDK with Haiku model.

**Selected Technology Stack**: @anthropic-ai/claude-agent-sdk + Claude 3 Haiku
**Target Outcome**: 90:1 reduction in manual steps, $1.60/month operational cost
**Timeline**: 2-3 weeks (10-15 development hours)

## Prerequisites

### Environment Requirements
- [x] Node.js 18+ installed
- [x] TypeScript configured
- [x] Existing MCP server (custom-agents-orchestrator) operational
- [x] 46 agent YAML files in `agents/` directory
- [x] memory.db SQLite database accessible
- [ ] ANTHROPIC_API_KEY environment variable set

### Dependencies to Add
```json
{
  "@anthropic-ai/claude-agent-sdk": "^0.1.42"
}
```

**Note**: Agent SDK includes @anthropic-ai/sdk, no separate installation needed

## Phase 1: Environment Setup & Validation

### Task 1.1: Install Claude Agent SDK
**Action**: Add dependency to MCP server project
**Command**:
```bash
cd C:\Users\jazbo\AppData\Roaming\Roo-Code\MCP\custom-agents-orchestrator
npm install @anthropic-ai/claude-agent-sdk
```

**AI-Verifiable Outcome**: 
- package.json contains `"@anthropic-ai/claude-agent-sdk": "^0.1.42"`
- node_modules/@anthropic-ai/claude-agent-sdk exists
- No installation errors

### Task 1.2: Configure API Key
**Action**: Set ANTHROPIC_API_KEY in environment

**Option A - User Level (Recommended)**:
```bash
# Windows (persistent)
setx ANTHROPIC_API_KEY "your-api-key-here"
```

**Option B - MCP Configuration**:
Add to `mcp_settings.json`:
```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key-here",
        "AGENTS_DIR": "...",
        "MEMORY_DB": "..."
      }
    }
  }
}
```

**AI-Verifiable Outcome**:
- Environment variable accessible from Node.js
- `process.env.ANTHROPIC_API_KEY` returns valid key
- No API authentication errors on test call

### Task 1.3: Create Feature Flag System
**Action**: Add V1/V2 mode toggle for gradual rollout

**File**: `src/config.ts` (new)
```typescript
export const CONFIG = {
  AUTOMATION_MODE: process.env.AUTOMATION_MODE || 'V1', // 'V1' or 'V2'
  DEFAULT_MODEL: 'claude-3-haiku-20240307',
  MAX_RETRIES: 2,
  ENABLE_CACHING: true,
  ENABLE_STREAMING: true
};
```

**AI-Verifiable Outcome**:
- Config file compiles without errors
- Can toggle between V1 and V2 modes
- Default mode is V1 (safe fallback)

## Phase 2: Core Agent Execution Engine

### Task 2.1: Create AgentExecutor Class
**Action**: Build core execution engine using Agent SDK

**File**: `src/agent-executor.ts` (new)
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';
import { CONFIG } from './config';
import type { AgentMode } from './types';

export class AgentExecutor {
  private sessionCache: Map<string, string> = new Map();
  
  async executeAgentMode(params: {
    modeSlug: string;
    taskDescription: string;
    modeConfig: AgentMode;
    contextFiles?: string[];
    parentSessionId?: string;
  }): Promise<AgentExecutionResult> {
    const messages = [];
    
    for await (const message of query({
      prompt: params.taskDescription,
      options: {
        model: CONFIG.DEFAULT_MODEL,
        mcpServers: this.getMCPServerConfig(),
        allowedTools: this.getAllowedTools(),
        systemPrompt: params.modeConfig.customInstructions,
        sessionId: params.parentSessionId
      }
    })) {
      messages.push(message);
      
      if (message.type === "progress") {
        this.emitProgress(message);
      }
    }
    
    return this.parseResult(messages, params.modeSlug);
  }
  
  private getMCPServerConfig() {
    return {
      "custom-agents": {
        command: "node",
        args: [__dirname + "/index.js"],
        env: {
          AGENTS_DIR: process.env.AGENTS_DIR,
          MEMORY_DB: process.env.MEMORY_DB
        }
      }
    };
  }
  
  private getAllowedTools(): string[] {
    return [
      "mcp__list_agent_modes",
      "mcp__get_mode_definition",
      "mcp__query_project_state"
    ];
  }
  
  private parseResult(messages: any[], modeSlug: string): AgentExecutionResult {
    const result = messages.find(m => m.type === "result");
    
    // Validate routing headers (To/From format)
    this.validateRoutingHeaders(result?.content);
    
    return {
      success: true,
      modeSlug,
      response: result?.content || "",
      sessionId: result?.session_id,
      tokensUsed: result?.usage || { input: 0, output: 0 }
    };
  }
  
  private validateRoutingHeaders(content: string): void {
    const headerRegex = /^To:\s*[\w-]+,\s*From:\s*[\w-]+/m;
    if (!headerRegex.test(content)) {
      throw new Error("Missing or invalid routing headers in agent response");
    }
  }
  
  private emitProgress(message: any): void {
    // Hook for RooCode UI updates
    console.log(`[Progress] ${message.content}`);
  }
}
```

**AI-Verifiable Outcomes**:
- File compiles with no TypeScript errors
- AgentExecutor class instantiates successfully
- Routing header validation catches malformed responses
- Session caching mechanism operational

### Task 2.2: Add execute_agent_mode MCP Tool
**Action**: Expose agent execution via MCP tool

**File**: `src/index.ts` (modify existing)
```typescript
import { AgentExecutor } from './agent-executor';
import { CONFIG } from './config';

const executor = new AgentExecutor();

// Add new tool
server.tool(
  "execute_agent_mode",
  "Execute an agent mode autonomously using Claude Agent SDK (V2 mode)",
  {
    modeSlug: z.string().describe("Agent mode slug to execute"),
    taskDescription: z.string().describe("Task for the agent to perform"),
    contextFiles: z.array(z.string()).optional().describe("File paths for context"),
    parentSessionId: z.string().optional().describe("Parent session for chaining")
  },
  async (args) => {
    // Feature flag check
    if (CONFIG.AUTOMATION_MODE !== 'V2') {
      return {
        content: [{
          type: "text",
          text: "V2 automation not enabled. Set AUTOMATION_MODE=V2 to use this feature."
        }]
      };
    }
    
    // Load mode configuration
    const modeConfig = await loadModeConfig(args.modeSlug);
    
    // Execute agent
    const result = await executor.executeAgentMode({
      modeSlug: args.modeSlug,
      taskDescription: args.taskDescription,
      modeConfig,
      contextFiles: args.contextFiles,
      parentSessionId: args.parentSessionId
    });
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);
```

**AI-Verifiable Outcomes**:
- Tool appears in `list_agent_modes` output
- Feature flag prevents execution when AUTOMATION_MODE=V1
- Tool accepts all required parameters
- Returns structured JSON result

## Phase 3: Testing & Validation

### Task 3.1: Unit Tests for AgentExecutor
**Action**: Create test suite

**File**: `src/__tests__/agent-executor.test.ts` (new)
```typescript
describe('AgentExecutor', () => {
  it('validates routing headers correctly', () => {
    // Test valid headers
    // Test invalid headers
    // Test missing headers
  });
  
  it('builds MCP server config with correct env vars', () => {
    // Verify AGENTS_DIR and MEMORY_DB passed through
  });
  
  it('handles API errors gracefully', () => {
    // Test network failures
    // Test API rate limits
    // Test invalid API keys
  });
});
```

**AI-Verifiable Outcomes**:
- All tests pass
- Code coverage >80%
- No regression in existing V1 functionality

### Task 3.2: Integration Test - Single Agent Execution
**Action**: Test execution of simple agent (e.g., ask mode)

**Test Script**: `tests/integration/single-agent.test.ts`
```typescript
test('Execute ask mode agent', async () => {
  const result = await mcpClient.callTool('execute_agent_mode', {
    modeSlug: 'ask',
    taskDescription: 'What is 2+2?',
    contextFiles: []
  });
  
  expect(result.success).toBe(true);
  expect(result.response).toContain('To:');
  expect(result.response).toContain('From: ask');
  expect(result.tokensUsed.input).toBeGreaterThan(0);
});
```

**AI-Verifiable Outcomes**:
- Test completes in <30 seconds
- Response contains valid routing headers
- Token usage tracked correctly
- Cost < $0.01 for single execution

### Task 3.3: Integration Test - Multi-Agent Workflow
**Action**: Test full SPARC workflow (simplified)

**Test Workflow**:
1. Uber-orchestrator → Goal Clarification
2. Goal Clarification → Specification Phase
3. Specification Phase → (verify chaining)

**AI-Verifiable Outlines**:
- Session IDs properly chained
- Context preserved across agents
- Total cost < $0.25
- All routing headers valid
- No manual intervention required

## Phase 4: Cost Monitoring & Optimization

### Task 4.1: Token Usage Tracking
**Action**: Add telemetry to AgentExecutor

**Enhancement**:
```typescript
export class AgentExecutor {
  private usageStats: UsageStats = {
    totalCalls: 0,
    totalInputTokens: 0,
    totalOutputTokens: 0,
    totalCost: 0
  };
  
  private calculateCost(usage: TokenUsage): number {
    const inputCost = (usage.input / 1_000_000) * 0.25;  // Haiku pricing
    const outputCost = (usage.output / 1_000_000) * 1.25;
    return inputCost + outputCost;
  }
  
  async getUsageStats(): Promise<UsageStats> {
    return this.usageStats;
  }
}
```

**AI-Verifiable Outcomes**:
- Usage stats accessible via MCP tool
- Cost calculations accurate to $0.001
- Stats persist across MCP server restarts (optional)

### Task 4.2: Implement Prompt Caching
**Action**: Enable automatic caching for mode instructions

**Configuration**:
```typescript
options: {
  model: CONFIG.DEFAULT_MODEL,
  enableCaching: CONFIG.ENABLE_CACHING, // Enable 90% savings
  cacheControl: {
    systemPrompt: { type: "ephemeral" } // Cache mode instructions
  }
}
```

**AI-Verifiable Outcomes**:
- Second execution of same mode shows 90% input token reduction
- Cache hit rate >80% after 5 agent calls
- Cost savings verified in usage stats

## Phase 5: Error Handling & Resilience

### Task 5.1: Implement Retry Logic
**Action**: Add exponential backoff for transient failures

**Enhancement**:
```typescript
private async executeWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = CONFIG.MAX_RETRIES
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries || !this.isRetryable(error)) {
        throw error;
      }
      await this.sleep(Math.pow(2, attempt) * 1000);
    }
  }
  throw new Error('Max retries exceeded');
}

private isRetryable(error: any): boolean {
  // Network errors, rate limits, 5xx responses
  return error.status >= 500 || error.code === 'RATE_LIMIT';
}
```

**AI-Verifiable Outcomes**:
- Retries occur on 529 (overloaded) responses
- Does not retry on 401 (auth) or 400 (bad request)
- Maximum 2 retries before failure
- Exponential backoff verified (1s, 2s, 4s)

### Task 5.2: Graceful Degradation to V1
**Action**: Auto-fallback if V2 fails

**Logic**:
```typescript
async executeAgentMode(params) {
  if (CONFIG.AUTOMATION_MODE === 'V2') {
    try {
      return await this.executeV2(params);
    } catch (error) {
      console.warn('V2 execution failed, falling back to V1', error);
      return this.createV1DelegationPayload(params);
    }
  }
  return this.createV1DelegationPayload(params);
}
```

**AI-Verifiable Outcomes**:
- V1 fallback triggered on V2 errors
- User notified of fallback mode
- No data loss during fallback

## Phase 6: Documentation & Deployment

### Task 6.1: Update README
**Action**: Document V2 features and usage

**Sections to Add**:
- V2 Setup Instructions
- ANTHROPIC_API_KEY configuration
- Feature flag usage
- Cost monitoring guide
- Troubleshooting

**AI-Verifiable Outcomes**:
- README >200 lines
- All code examples tested and working
- Screenshots/diagrams included

### Task 6.2: Create Migration Guide
**Action**: V1 → V2 transition documentation

**File**: `MIGRATION_V1_TO_V2.md`
**Contents**:
- Comparison table (V1 vs V2)
- Step-by-step migration
- Rollback procedure
- Cost calculator

**AI-Verifiable Outcomes**:
- Guide follows chronological steps
- Rollback tested and documented
- All commands executable

### Task 6.3: Deploy to Production
**Action**: Enable V2 in RooCode MCP settings

**Steps**:
1. Backup current MCP server
2. Deploy V2 changes
3. Set `AUTOMATION_MODE=V2` in `mcp_settings.json`
4. Restart RooCode
5. Verify with test agent call
6. Monitor for 24 hours

**AI-Verifiable Outcomes**:
- V2 mode active in production
- No errors in MCP server logs
- Test agent execution successful
- Cost tracking operational

## Phase 7: Monitoring & Optimization

### Task 7.1: Week 1 Quality Monitoring
**Action**: Track success metrics

**Metrics to Monitor**:
- Agent task completion rate (target: >95%)
- Routing header compliance (target: >99%)
- Average cost per workflow (target: <$0.10)
- Manual intervention rate (target: <5%)

**AI-Verifiable Outcomes**:
- Metrics dashboard created
- Data collected for 100+ agent executions
- No critical failures

### Task 7.2: Haiku Quality Assessment
**Action**: Determine if Sonnet upgrade needed

**Decision Criteria**:
- If quality issues >10% → Upgrade to Hybrid (Option 3)
- If quality issues <5% → Remain on Haiku
- If 5-10% → Targeted Sonnet for specific agents only

**AI-Verifiable Outcomes**:
- Quality report generated
- Decision documented with data
- If upgrading: migration plan created

## Success Criteria

### Phase 2 Complete (Core Functionality)
- ✅ execute_agent_mode tool operational
- ✅ Single agent execution successful
- ✅ Routing headers validated
- ✅ Token usage tracked

### Phase 3 Complete (Validation)
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ Multi-agent workflow validated
- ✅ Cost under budget ($0.25/test workflow)

### Phase 6 Complete (Production Ready)
- ✅ Documentation complete
- ✅ V2 deployed and stable
- ✅ Monitoring active
- ✅ No regression in V1 features

### Final Success (30 Days Post-Launch)
- ✅ 90:1 manual step reduction achieved
- ✅ Monthly costs <$5
- ✅ User satisfaction >4/5
- ✅ Zero data loss incidents

## Timeline & Effort Estimates

| Phase | Tasks | Estimated Hours | Calendar Days |
|-------|-------|----------------|---------------|
| Phase 1: Setup | 3 tasks | 2 hours | 1 day |
| Phase 2: Core Engine | 2 tasks | 5 hours | 2 days |
| Phase 3: Testing | 3 tasks | 3 hours | 2 days |
| Phase 4: Optimization | 2 tasks | 2 hours | 1 day |
| Phase 5: Resilience | 2 tasks | 2 hours | 1 day |
| Phase 6: Deployment | 3 tasks | 2 hours | 2 days |
| Phase 7: Monitoring | 2 tasks | 1 hour/week | Ongoing |
| **TOTAL** | **17 tasks** | **16 hours** | **9 days** |

**Best Case**: 1.5 weeks (full-time focus)
**Realistic**: 2-3 weeks (part-time, with reviews and iterations)
**Worst Case**: 4 weeks (includes troubleshooting delays)

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Haiku quality inadequate | Medium | Medium | Quick switch to Sonnet hybrid |
| API rate limits hit | Low | Low | Built-in retry + backoff |
| Cost overruns | Very Low | Low | Haiku provides 12x cost buffer |
| Agent SDK bugs | Low | Medium | V1 fallback + Anthropic support |
| Integration issues | Low | High | Comprehensive test suite |

## Next Actions

1. **Immediate**: User obtains ANTHROPIC_API_KEY from https://console.anthropic.com/
2. **Day 1**: Execute Phase 1 (Environment Setup)
3. **Day 2-3**: Execute Phase 2 (Core Engine Development)
4. **Day 4-5**: Execute Phase 3 (Testing & Validation)
5. **Week 2**: Complete Phases 4-6 (Optimization → Deployment)
6. **Week 3+**: Phase 7 (Monitoring & Continuous Improvement)

---

**Project Manager**: research-planner-strategic mode
**Architecture Lead**: Based on Technology Decision Matrix
**Implementation Lead**: TBD (likely coder-test-driven mode)
**Quality Assurance**: RULER quality evaluator
**Stakeholder**: User (jazbo)

**Status**: READY FOR IMPLEMENTATION ✅