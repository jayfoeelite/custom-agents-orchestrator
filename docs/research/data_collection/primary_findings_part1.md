# Primary Research Findings - Part 1: Anthropic Model Pricing

## Data Source
**Search Query**: "Anthropic Claude API pricing 2024 models cost per million tokens"
**Date**: 2024-11-16
**Primary Sources**: 
- https://docs.claude.com/en/docs/about-claude/pricing
- https://www.anthropic.com/pricing
- https://www.anthropic.com/claude/sonnet

## Claude Model Pricing Matrix (2024-2025)

### Claude 3 Family

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window | Notes |
|-------|----------------------|------------------------|----------------|-------|
| **Claude 3 Haiku** | $0.25 | $1.25 | 200K | **CHEAPEST MODEL** |
| Claude 3 Sonnet | $3.00 | $15.00 | 200K | Balanced performance |
| Claude 3 Opus | $15.00 | $75.00 | 200K | Highest capability |

### Claude 3.5 Family

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window | Notes |
|-------|----------------------|------------------------|----------------|-------|
| Claude 3.5 Sonnet | $3.00 | $15.00 | 200K | Latest balanced model |

### Claude 4 Family (2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Thinking Tokens | Context Window |
|-------|----------------------|------------------------|-----------------|----------------|
| Claude 4.1 Opus | $20.00 | $80.00 | $40.00 | 200K+ |

## Key Findings - Recursive Abstraction

### Pattern 1: Cost Tiers
**Observation**: Three clear pricing tiers across Claude family
- **Budget Tier**: Haiku ($0.25/$1.25) - 94% cheaper than Opus
- **Balanced Tier**: Sonnet/3.5 Sonnet ($3/$15) - 80% cheaper than Opus
- **Premium Tier**: Opus ($15/$75) - Maximum capabilities

**Implication**: For agent orchestration tasks, starting with Haiku provides significant cost savings while testing automation viability.

### Pattern 2: Cost Optimization Features
**Prompt Caching**: 
- Source: Sonnet 4.5 page mentions "up to 90% cost savings with prompt caching"
- Mechanism: Reuse of previous prompt context
- Use Case: Repetitive agent instructions, mode definitions

**Batch Processing**:
- Source: "50% cost savings with batch processing"
- Use Case: Non-urgent agent delegations that can be queued

### Pattern 3: New Cost Category - "Thinking Tokens"
**Claude 4.1 Introduction**: Thinking tokens ($40/1M) charged when model uses external tools/functions
- **Critical for Agent Automation**: Our use case involves tool calling (MCP tools, delegation)
- **Cost Impact**: Additional 50-100% overhead on tool-heavy tasks
- **Status**: Only on Claude 4.1 currently, may expand to other models

## Cost Projections for Agent Orchestration

### Assumptions for Single SPARC Workflow
Based on task analysis:
- Uber-orchestrator initial planning: ~5,000 input tokens
- Each agent delegation: ~3,000 input + 2,000 output tokens
- Number of agent calls per workflow: 10-15 (Goal Clarification → Specification → Pseudocode → Architecture → Refinement x3 → Testing → Documentation → Triangulation checks)
- Total tokens per workflow: ~75,000 input + 50,000 output

### Cost Per Workflow by Model

**Claude 3 Haiku** (Recommended Budget):
- Input: 75K tokens × $0.25 / 1M = $0.01875
- Output: 50K tokens × $1.25 / 1M = $0.0625
- **Total per workflow: ~$0.08**
- **Monthly (20 workflows): ~$1.60**

**Claude 3.5 Sonnet** (Balanced):
- Input: 75K × $3 / 1M = $0.225
- Output: 50K × $15 / 1M = $0.75
- **Total per workflow: ~$0.98**
- **Monthly (20 workflows): ~$19.60**

**Claude 3 Opus** (Premium):
- Input: 75K × $15 / 1M = $1.125
- Output: 50K × $75 / 1M = $3.75
- **Total per workflow: ~$4.88**
- **Monthly (20 workflows): ~$97.60**

## Critical Decision Point

**RECOMMENDATION: Start with Claude 3 Haiku**

**Rationale**:
1. **Cost Efficiency**: 98% cheaper than Opus, 92% cheaper than Sonnet
2. **Sufficient Capability**: For structured agent task delegation parsing and routing
3. **Fallback Strategy**: Can hybrid - use Haiku for orchestration, Sonnet for complex reasoning when needed
4. **Testing Viability**: Low cost enables extensive testing and iteration
5. **200K Context Window**: Sufficient for agent mode definitions and conversation history

**Risk Mitigation**:
- Monitor Haiku performance on agent task parsing accuracy
- Create quality gates: if Haiku fails validation >10%, escalate to Sonnet
- Document failure patterns to inform model selection rules

## Free Tier Status

**Search Result Analysis**: No explicit free tier mentioned in current pricing
**Secondary Finding**: Some blog posts reference "Free" tier but seems to be for claude.com web interface, not API
**Conclusion**: No API free tier currently available; must budget for token costs

## Citations
1. Anthropic Pricing Documentation: https://docs.claude.com/en/docs/about-claude/pricing
2. Official Pricing Page: https://www.anthropic.com/pricing  
3. Sonnet 4.5 Page: https://www.anthropic.com/claude/sonnet
4. API Pricing Guide (Third-party): https://apidog.com/blog/claude-api-cost/
5. Cost Optimization Analysis: https://www.finout.io/blog/anthropic-api-pricing
6. 2025 Pricing Guide: https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration

---
**Next Research Steps**:
1. Validate Haiku's capability for agent orchestration tasks
2. Research @anthropic-ai/sdk integration patterns
3. Investigate AI-to-AI communication best practices
4. Design executeAgentMode() architecture