# Decision Log

## Architectural Decisions

### [2025-11-14 20:36:00] - Memory Bank Structure Creation
**Decision**: Created Memory Bank with standard file structure (productContext.md, activeContext.md, systemPatterns.md, decisionLog.md, progress.md)

**Rationale**: 
- User requested Memory Bank creation before agent validation
- Follows memory_bank_strategy guidelines from custom instructions
- Provides foundation for tracking project context throughout development

**Implications**:
- All future significant changes will be tracked in Memory Bank
- Cross-session context preservation enabled
- Decision traceability established

### [2025-11-14 20:36:00] - Agent Definition Format: YAML
**Decision**: Agent modes are defined in YAML format in the agents/ directory

**Rationale**:
- 45 existing YAML files identified in agents/ directory
- YAML provides human-readable, structured configuration
- Easy to parse and validate programmatically
- Supports complex nested structures needed for comprehensive agent definitions

**Implications**:
- Validation tooling should be YAML-aware
- Schema validation can ensure consistency
- Version control friendly format

### [2025-11-14 20:36:00] - State Management via SQLite
**Decision**: Project uses memory.db SQLite database with project_memory table for state management

**Rationale**:
- Provides persistent, queryable project state
- Signal Interpretation Framework requires structured data storage
- Supports complex queries for context retrieval
- Lightweight, serverless, single-file deployment

**Implications**:
- orchestrator-state-scribe agent responsible for all database operations
- Comprehensive audit trail built into database structure
- Query performance considerations for large projects

---
[2025-11-14 20:36:00] - Initial decision log created during Memory Bank initialization

### [2025-11-14 20:45:00] - Validation Tooling Architecture
**Decision**: Implemented Python-based validation and analysis tooling with JSON Schema

**Rationale**:
- Python chosen for cross-platform compatibility and rich ecosystem (jsonschema, PyYAML, graphviz)
- JSON Schema provides industry-standard validation with clear error messages
- Separate tools (validate-agents.py, generate-dependency-graph.py) follow single-responsibility principle
- Mermaid format prioritized for diagram output (no external dependencies, works in GitHub/GitLab)

**Implications**:
- Users need Python 3.7+ installed
- Graphviz optional for PNG/SVG output but not required
- Tools can be integrated into CI/CD pipelines
- Pre-commit hooks can enforce validation

### [2025-11-14 20:45:00] - Versioning Strategy: Optional but Recommended
**Decision**: Made `version` field optional in schema but strongly recommended

**Rationale**:
- Existing 45 agents don't have version fields; making it required would break validation
- Semantic versioning (X.Y.Z) provides clear upgrade paths
- Optional field allows gradual adoption without forcing immediate migration

**Implications**:
- New agents should include version field
- Existing agents can be versioned incrementally
- Future migration tool could add default versions (1.0.0) to all agents

### [2025-11-14 20:45:00] - Dependency Extraction via Regex Pattern Matching
**Decision**: Used regex patterns to extract delegation relationships from customInstructions

**Rationale**:
- customInstructions is free-form text, not structured data
- Patterns like "delegate to agent-slug" and "new_task to agent-slug" are consistent
- Automatic extraction reduces manual maintenance burden

**Implications**:
- Delegation patterns must follow conventions for auto-detection
- Manual review of generated graphs recommended to verify accuracy
- Future enhancement could use explicit dependencies field in YAML

---
[2025-11-14 20:45:00] - Validation tooling architectural decisions documented


### [2025-11-16 14:26:00] - MCP Server Architecture for Custom Agent Delegation
**Decision**: Created Custom Agents Orchestrator MCP Server to enable uber-orchestrator mode delegation

**Rationale**:
- RooCode's `new_task` tool only supports 4 default modes (code, ask, architect, debug)
- 46 custom agent modes in `agents/` directory cannot be delegated to automatically
- MCP server provides bridge between RooCode and custom mode ecosystem
- Enables discovery, inspection, and structured delegation of custom modes

**Implementation**:
- Server location: `C:\Users\jazbo\AppData\Roaming\Roo-Code\MCP\custom-agents-orchestrator`
- Language: TypeScript with Node.js
- Dependencies: @modelcontextprotocol/sdk, js-yaml, better-sqlite3, zod
- Tools provided: list_agent_modes, get_mode_definition, delegate_to_mode, query_project_state
- Configuration: Added to mcp_settings.json with AGENTS_DIR and MEMORY_DB env vars

**Implications**:
- Uber-orchestrator can now discover all 46 custom modes
- Can query project state from memory.db
- Can create structured delegation payloads with routing headers
- V1 is simulation-only (requires manual mode switching)
- V2 will require AI API integration for actual execution
- Establishes foundation for full SPARC automation

### [2025-11-16 14:40:00] - V2 Automation Architecture: Claude Agent SDK + Haiku
**Decision**: Selected @anthropic-ai/claude-agent-sdk with Claude 3 Haiku as the technology stack for implementing full agent automation

**Rationale**:
- **Simplicity Mandate Compliance**: Single integrated platform, minimal architectural complexity
- **Cost Leadership**: Haiku is cheapest model at $0.25 input / $1.25 output per 1M tokens
- **Feature Complete**: Agent SDK provides session management, MCP integration, tool calling, error handling, and retry logic out-of-box
- **MCP Compatibility**: Native support for Model Context Protocol allows direct integration with existing custom-agents-orchestrator MCP server
- **Proven Technology**: Official Anthropic SDK with active support and documentation
- **Cost Efficiency**: Projected $1.60/month for 20 workflows vs $19.60 for Sonnet, $97.60 for Opus

**Technology Stack Selected**:
```
Core: @anthropic-ai/claude-agent-sdk (v0.1.42+)
Model: Claude 3 Haiku (claude-3-haiku-20240307)
Integration: Existing Custom Agents Orchestrator MCP Server
Infrastructure: memory.db (SQLite), 46 agent YAML definitions
```

**Alternatives Considered & Rejected**:
1. **Custom orchestration layer with core SDK**: Rejected due to unnecessary complexity, 40-60 hour implementation vs 10-15 hours for Agent SDK
2. **Hybrid Haiku/Sonnet approach**: Deferred to Phase 2 based on quality monitoring results

**Implementation Approach**:
- Phase 1 (V2.0): Haiku-only implementation
- Phase 1.5: 2-week quality monitoring period
- Phase 2 (V2.1): Upgrade to Sonnet for complex agents only if quality issues >10%

**Implications**:
- Requires ANTHROPIC_API_KEY environment variable
- Adds execute_agent_mode tool to MCP server
- Enables 90:1 reduction in manual steps (90 manual actions → 1 per workflow)
- Monthly operational cost: $1.60 (vs current $0 but high manual labor)
- Feature flag system allows V1 fallback if V2 encounters issues
- Backward compatible with existing simulation mode
- Estimated implementation: 16 hours over 2-3 weeks

**Success Metrics**:
- Agent task completion rate >95%
- Routing header compliance >99%  
- Average cost per workflow <$0.10
- Manual intervention rate <5%

**Risk Mitigation**:
- V1 simulation mode remains as fallback
- Comprehensive testing before production deployment
- Quality monitoring triggers upgrade to Sonnet if needed
- Built-in retry logic and error handling

[2025-11-16 20:55:30] - Created a public webpage to provide project details and usage instructions.
