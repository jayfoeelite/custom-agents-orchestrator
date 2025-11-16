# Agent Automation V2 - Setup Instructions

## IMMEDIATE ACTION REQUIRED

### Step 1: Configure Anthropic API Key

**CRITICAL**: The API key must be set before V2 automation can function.

#### Option A: Environment Variable (Recommended)
```bash
# Windows (PowerShell - Persistent)
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'YOUR_ANTHROPIC_API_KEY_HERE', 'User')

# Verify
$env:ANTHROPIC_API_KEY
```

#### Option B: MCP Configuration File
Edit `C:\Users\jazbo\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json`:

```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": ["C:\\Users\\jazbo\\AppData\\Roaming\\Roo-Code\\MCP\\custom-agents-orchestrator\\build\\index.js"],
      "env": {
        "ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE",
        "AGENTS_DIR": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\agents",
        "MEMORY_DB": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\memory.db"
      }
    }
  }
}
```

### Step 2: Install Agent SDK

```bash
cd C:\Users\jazbo\AppData\Roaming\Roo-Code\MCP\custom-agents-orchestrator
npm install @anthropic-ai/claude-agent-sdk
```

### Step 3: Verify Installation

Create test file `test-api-key.js`:
```javascript
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

async function test() {
  try {
    const message = await client.messages.create({
      model: 'claude-3-haiku-20240307',
      max_tokens: 100,
      messages: [{ role: 'user', content: 'Say "API key works!"' }]
    });
    console.log('✅ API Key Valid:', message.content[0].text);
  } catch (error) {
    console.error('❌ API Key Error:', error.message);
  }
}

test();
```

Run: `node test-api-key.js`

Expected output: `✅ API Key Valid: API key works!`

### Step 4: Enable V2 Mode

Set feature flag in MCP server config or create `.env` file:
```
AUTOMATION_MODE=V2
```

### Step 5: Restart RooCode

Close and restart RooCode to load new MCP configuration.

### Step 6: Test V2 Execution

Use the `execute_agent_mode` MCP tool:
```javascript
// From uber-orchestrator or any mode in RooCode
await mcpClient.callTool('execute_agent_mode', {
  modeSlug: 'ask',
  taskDescription: 'What is 2+2?',
  contextFiles: []
});
```

Expected: Agent executes autonomously and returns result with routing headers.

---

## Security Notes

⚠️ **API Key Security**:
- Never commit API key to version control
- Consider using environment variables over config files 
- Rotate key if accidentally exposed
- Monitor usage at https://console.anthropic.com/

## Cost Monitoring

- Check usage: https://console.anthropic.com/settings/billing
- Expected cost: ~$0.08 per full workflow
- Set up billing alerts at $5/$10/$20 thresholds

## Troubleshooting

**"API key not found"**:
- Verify environment variable is set: `echo %ANTHROPIC_API_KEY%`
- Restart terminal/RooCode after setting env var
- Check MCP server logs for errors

**"Rate limit exceeded"**:
- Default limits: 50,000 tokens/minute for Haiku
- Built-in retry logic will handle this automatically
- Monitor at console.anthropic.com

**"Invalid API key"**:
- Verify key starts with `sk-ant-api03-`
- Check for typos or truncation
- Regenerate key if needed at console.anthropic.com

---

## Next Steps

After setup complete:
1. Follow `docs/project_plan.md` Phase 2: Core Agent Execution Engine
2. Implement `AgentExecutor` class
3. Add `execute_agent_mode` MCP tool
4. Run integration tests
5. Deploy to production

**Implementation Mode**: Switch to `code` mode to begin development
**Reference**: `docs/project_plan.md` for complete implementation guide