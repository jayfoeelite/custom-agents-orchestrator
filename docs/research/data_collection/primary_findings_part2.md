# Primary Research Findings - Part 2: SDK Integration Patterns

## Data Source
**Search Query**: "@anthropic-ai/sdk TypeScript usage examples agent automation"
**Date**: 2024-11-16
**Primary Sources**:
- https://github.com/anthropics/anthropic-sdk-typescript
- https://github.com/anthropics/claude-agent-sdk-typescript
- https://docs.claude.com/en/api/agent-sdk/typescript
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk

## CRITICAL DISCOVERY: Two Distinct SDK Options

### Option 1: @anthropic-ai/sdk (Core Messages API)
**Purpose**: Direct API interaction for chat/completions
**Best For**: Simple request-response patterns
**Package**: `@anthropic-ai/sdk`
**Current Version**: 0.6.2+

**Basic Usage Pattern**:
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await anthropic.messages.create({
  model: 'claude-3-haiku-20240307',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Your prompt here' }
  ]
});
```

**Capabilities**:
- Direct message creation
- Streaming responses
- Tool/function calling support
- Request ID tracking for debugging
- Automatic retry logic (2 attempts with exponential backoff)

### Option 2: @anthropic-ai/claude-agent-sdk (RECOMMENDED)
**Purpose**: **"Create autonomous agents that can understand codebases, edit files, run commands, and execute complex workflows"**
**Best For**: Multi-step agent automation with tool execution
**Package**: `@anthropic-ai/claude-agent-sdk`
**Current Version**: 0.1.42
**GitHub**: https://github.com/anthropics/claude-agent-sdk-typescript

**Key Features for Our Use Case**:
1. **Session Management**: Maintains conversation context across multiple agent interactions
2. **Built-in Tools**: File operations, Bash execution, web search
3. **Model Context Protocol (MCP)**: Attach custom external tools (perfect for our existing MCP server!)
4. **Tool Permission System**: Control which tools agents can access
5. **Streaming and non-streaming modes**: Flexible response handling
6. **Visual Feedback Support**: Screenshots/renders for validation

**Architecture**:
```typescript
type SDKAssistantMessage = {
  type: 'assistant';
  uuid: UUID;
  session_id: string;
  message: APIAssistantMessage;  // From Anthropic SDK
  parent_tool_use_id: string | null;
}
```

## Recursive Abstraction - Pattern Analysis

### Pattern 1: SDK Layering Strategy
**Core SDK (Low-level)** → **Agent SDK (High-level)**

The Agent SDK is built ON TOP of the core SDK, providing agent-specific abstractions:
- Session persistence
- Tool orchestration
- Workflow management
- Error recovery

**Implication for Our Architecture**: 
- We should use Agent SDK as primary interface
- Agent SDK already handles many orchestration concerns we'd otherwise build ourselves
- MCP integration path already exists!

### Pattern 2: MCP Integration Pattern
**Direct Quote from docs**: "The Model Context Protocol (MCP) to attach custom external tools"

**Critical Insight**: The Agent SDK has BUILT-IN support for MCP!
- Our existing Custom Agents Orchestrator MCP server can be directly integrated
- No need to wrap tools in custom interfaces
- Agent SDK handles tool discovery and invocation

**Architecture Simplification**:
```
Current (V1 - Simulation):
RooCode → MCP Server → Delegation Payload (requires manual execution)

Proposed (V2 - Automated):
RooCode → MCP Server → Agent SDK → Claude API → Executes Agent Mode → Returns Result
```

### Pattern 3: Session-Based Conversation Flow
**Session Management Feature**:
- Each agent delegation creates a session_id
- Parent-child relationship tracking via parent_tool_use_id
- Context preserved across multiple interactions
- Perfect for our SPARC workflow where agents build on previous outputs

**Use Case Mapping**:
```
Uber-Orchestrator Session:
  ├─ Goal Clarification Session (child)
  ├─ Specification Phase Session (child, references Goal Clarification)
  ├─ Pseudocode Phase Session (child, references Specification)
  └─ ...continuing workflow
```

### Pattern 4: Built-in Feedback Loops
**Quote**: "When generating an email, you may want Claude to check that the email address is valid (if not, throw an error)"

**Validation Pattern**:
- Agent SDK supports throwing errors/warnings during execution
- TypeScript generation with linting for multi-layer feedback
- Visual feedback for UI tasks

**Application to Our System**:
- Agents can validate their own outputs before returning
- Devils-advocate checks can be automated validation steps
- RULER quality evaluation can be integrated as feedback mechanism

## Technology Stack Decision - Emerging Clarity

### Simplicity Mandate Alignment

**INTEGRATED PLATFORM APPROACH** (Recommended):
```
Single Technology Stack:
- @anthropic-ai/claude-agent-sdk (includes core SDK)
- Claude 3 Haiku for cost efficiency
- MCP for tool integration (already built-in)
- TypeScript for type safety
```

**Benefits**:
1. **Minimal Dependencies**: One primary package handles entire workflow
2. **Built-in MCP Support**: No custom tool wrapper needed
3. **Session Management**: Conversation context handled automatically
4. **Error Handling**: Retry logic and failure recovery included
5. **Official Support**: Maintained by Anthropic directly

**Vs. Composable Approach** (Why we reject it):
```
Multiple Components:
- Core SDK + custom orchestration layer
- Separate session management
- Custom MCP integration
- Custom error handling
```
This violates Simplicity Mandate - more complex, more failure points

## Implementation Architecture (Preliminary)

### Enhanced MCP Server V2 Structure
```typescript
// Enhanced index.ts with Agent SDK
import { createAgent } from '@anthropic-ai/claude-agent-sdk';
import Anthropic from '@anthropic-ai/sdk';

class AgentOrchestrator {
  private agentSessions: Map<string, AgentSession>;
  
  async executeAgentMode(
    modeSlug: string,
    taskDescription: string,
    contextFiles: string[]
  ): Promise<AgentResult> {
    // 1. Load mode definition from YAML
    const modeConfig = await this.loadModeConfig(modeSlug);
    
    // 2. Create agent session with SDK
    const agent = createAgent({
      model: 'claude-3-haiku-20240307',  // Use cheapest model
      apiKey: process.env.ANTHROPIC_API_KEY,
      tools: this.mcpTools,  // Our existing MCP tools
      systemPrompt: modeConfig.customInstructions
    });
    
    // 3. Execute task with streaming
    const result = await agent.execute({
      input: taskDescription,
      context: contextFiles
    });
    
    // 4. Parse and validate response
    return this.validateResponse(result, modeConfig);
  }
}
```

### Cost Optimization Strategy
**With Agent SDK + Haiku**:
- Session context reuse reduces redundant token usage
- Built-in caching for repeated prompts (90% savings)
- Haiku pricing: $0.25 input / $1.25 output per 1M tokens

**Projected Savings**:
- Prompt caching on mode definitions: ~5000 tokens/agent call
- Without caching: 5000 * $0.25/1M = $0.00125
- With caching: 5000 * $0.025/1M = $0.000125 (90% reduction)
- **Per workflow savings**: ~$0.01 - $0.02

## Knowledge Gaps Identified

1. **Agent SDK MCP Integration Details**: How exactly to register our MCP server tools?
2. **Session Persistence**: Where are sessions stored? Can we persist to memory.db?
3. **Error Recovery**: What happens if an agent fails mid-workflow?
4. **Rate Limiting**: How does Agent SDK handle API rate limits?
5. **Streaming Handling**: Best practices for real-time status updates to user

## Next Research Steps

1. Search for Agent SDK MCP integration examples
2. Research multi-agent orchestration patterns with Agent SDK
3. Investigate session persistence and recovery strategies
4. Explore cost optimization with prompt caching specifics

## Citations
1. Claude Agent SDK TypeScript Repository: https://github.com/anthropics/claude-agent-sdk-typescript
2. Agent SDK Documentation: https://docs.claude.com/en/api/agent-sdk/typescript
3. Building Agents Engineering Post: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
4. Core SDK Repository: https://github.com/anthropics/anthropic-sdk-typescript
5. Agent SDK Tutorial: https://skywork.ai/blog/how-to-use-claude-agent-sdk-step-by-step-ai-agent-tutorial
6. Bind IDE Guide: https://blog.getbind.co/2025/10/03/how-to-create-agents-with-claude-agents-sdk/

---
**Status**: Research phase progressing. Agent SDK discovery significantly simplifies architectural approach.