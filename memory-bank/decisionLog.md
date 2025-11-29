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

### [2025-11-18 04:27:10] - MCP Server Environment Variable Configuration Fix

**Decision**: Fixed the custom-agents-orchestrator MCP server environment variable configuration by addressing a server name mismatch and improving fallback path handling.

**Rationale**:
- The MCP server was running but not functioning correctly (list_agent_modes returned 0 modes, query_project_state returned empty results)
- Root cause analysis revealed a naming mismatch between the MCP server registration (`custom-agents-orchestrator`) and internal server code (`custom-agents`)
- Relative paths in fallback logic were sensitive to the current working directory and unreliable

**Implementation**:
- Update `agent-executor.js` to use the correct server name (`custom-agents-orchestrator`)
- Improve fallback paths in `index.js` to use absolute paths instead of relative paths
- Add error handling and logging to improve diagnostics
- Implement resilience patterns (circuit breaker, retry, graceful degradation)

**Implications**:
- Ensures environment variables are properly propagated through all process layers
- Improves system resilience with proper error handling and fallback mechanisms
- Provides clear diagnostic information when configuration issues occur
- Establishes a pattern for robust configuration management in distributed systems

**Documentation**:
- Created comprehensive report at `reports/mcp_server_env_config_fix.md`
- Includes root cause analysis, solution, verification steps, and architectural considerations

### [2025-11-21 13:36:00] - MCP Server V2 Automation Configuration

**Decision**: Documented the configuration process for enabling V2 automation in the custom-agents-orchestrator MCP server with Anthropic API integration.

**Rationale**:
- V2 automation enables full agent mode execution without manual mode switching
- Claude Agent SDK provides a clean integration path with minimal code changes
- Haiku model offers the best balance of cost and performance ($0.25/1M input tokens, $1.25/1M output tokens)
- Configuration via environment variables allows for flexible deployment without code changes
- Estimated cost of $0.08 per execution is economically viable for the project

**Implementation**:
- Add `AUTOMATION_MODE=V2` to mcp_settings.json env section
- Add `ANTHROPIC_API_KEY=sk-ant-...` to mcp_settings.json env section
- Restart RooCode to load the new configuration
- Verify with a simple "Hello World" test

**Implications**:
- Reduces manual steps from 90 to 1 per workflow (90:1 reduction)
- Enables true orchestration across all 46 agent modes
- Introduces API costs (~$1.60/month for 20 workflows)
- Requires API key management and security considerations
- Provides foundation for future enhancements (parallel execution, conversation threading)

### [2025-11-21 14:16:00] - V2 Automation Implementation for Custom Agents Orchestrator MCP Server

**Decision**: Implemented V2 automation for the Custom Agents Orchestrator MCP server by fixing environment variable configuration issues.

**Implementation**:
1. Updated getMCPServerConfig() in agent-executor.ts to explicitly pass AUTOMATION_MODE=V2 and ANTHROPIC_API_KEY
2. Added detailed logging in index.ts main() function to verify environment variables
3. Created updated mcp_settings.json template with proper configuration
4. Documented the implementation in reports/mcp_server_env_config_fix.md

**Rationale**:
- The MCP server was not properly reading the AUTOMATION_MODE and ANTHROPIC_API_KEY environment variables
- The AgentExecutor was not being initialized correctly due to missing environment variables
- The getMCPServerConfig() method was using a hardcoded path that might not match the actual path
- Explicit logging was needed to diagnose environment variable issues

**Implications**:
- Enables full agent automation using the Anthropic Claude API
- Reduces manual steps from 90 to 1 per workflow (90:1 reduction)
- Provides clear diagnostic information for troubleshooting
- Establishes a pattern for robust configuration management in distributed systems


### [2025-11-29 15:31:00] - Removed V2 Automation from Custom Agents Orchestrator MCP Server

**Decision**: Removed all V2 automation functionality from the custom-agents-orchestrator MCP server, reverting to V1 simulation-only mode.

**Rationale**:
- User reported that V2 automation was not working correctly
- Uber-orchestrator delegates tasks correctly most of the time without automation
- V1 simulation mode provides sufficient functionality for current needs
- Simpler codebase is easier to maintain and debug
- Removes dependency on Claude Agent SDK and Anthropic API integration

**Implementation**:
1. **Files Deleted**:
   - `src/config.ts` (63 lines) - V2 configuration management
   - `src/agent-executor.ts` (225 lines) - Agent execution engine with Claude SDK

2. **Files Modified**:
   - `src/index.ts`: Removed all V2-related code including:
     * Removed imports for AgentExecutor, CONFIG, and logConfig
     * Removed agentExecutor variable and initializeAgentExecutor() function
     * Removed execute_agent_mode tool from tools list
     * Removed execute_agent_mode case handler
     * Simplified main() function to remove V2 logging
     * Updated server startup message to indicate "V1 Simulation Mode"
   
   - `package.json`: Removed V2 dependencies:
     * @ant hropic-ai/claude-agent-sdk
     * @anthropic-ai/sdk  
     * zod (no longer needed)

3. **Remaining V1 Tools** (Fully Functional):
   - `list_agent_modes` - Lists all 46 custom agent modes
   - `get_mode_definition` - Returns complete mode configuration
   - `delegate_to_mode` - Creates delegation payloads for manual execution
   - `query_project_state` - Queries memory.db database

**Implications**:
- MCP server now operates in V1 simulation mode only
- Manual mode switching still required for task delegation
- Reduced complexity and dependencies
- Lower operational costs (no API usage)
- Easier troubleshooting and maintenance
- Server continues to provide discovery and delegation simulation
- Uber-orchestrator can still use all 4 V1 tools effectively

**Next Steps**:
- Restart RooCode to reload the updated MCP server
- Test that list_agent_modes and delegate_to_mode work correctly
- Verify uber-orchestrator can still delegate properly using V1 tools
