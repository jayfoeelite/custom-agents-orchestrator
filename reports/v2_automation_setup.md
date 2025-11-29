# MCP Server V2 Automation Setup Guide

## Current Configuration Analysis

The custom-agents-orchestrator MCP server is currently running in V1_SIMULATION mode, which means it can only create delegation payloads but cannot execute agent modes autonomously. To enable full automation with the Anthropic Claude API, we need to configure two critical environment variables:

1. `AUTOMATION_MODE=V2`
2. `ANTHROPIC_API_KEY=your_api_key`

### Current Environment Variable Usage

After analyzing the source code, I found that:

- In `src/config.ts`, the `CONFIG` object loads environment variables with defaults:
  ```typescript
  export const CONFIG: V2Config = {
    AUTOMATION_MODE: (process.env.AUTOMATION_MODE as 'V1' | 'V2') || 'V1',
    DEFAULT_MODEL: process.env.DEFAULT_MODEL || 'claude-3-haiku-20240307',
    MAX_RETRIES: parseInt(process.env.MAX_RETRIES || '2', 10),
    ENABLE_CACHING: process.env.ENABLE_CACHING !== 'false', // Default true
    ENABLE_STREAMING: process.env.ENABLE_STREAMING !== 'false', // Default true
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  };
  ```

- The `validateConfig()` function checks if V2 mode is enabled but API key is missing:
  ```typescript
  export function validateConfig(): void {
    if (CONFIG.AUTOMATION_MODE === 'V2' && !CONFIG.ANTHROPIC_API_KEY) {
      throw new Error(
        'ANTHROPIC_API_KEY environment variable is required when AUTOMATION_MODE=V2. ' +
        'Please set the API key in your environment or MCP configuration.'
      );
    }
  }
  ```

- In `src/agent-executor.ts`, the `AgentExecutor` class uses the Claude Agent SDK to execute agent modes:
  ```typescript
  async executeAgentMode(params: AgentExecutionParams): Promise<AgentExecutionResult> {
    // Uses Claude Agent SDK's query function with MCP integration
    for await (const message of query({
      prompt: params.taskDescription,
      options: {
        model: CONFIG.DEFAULT_MODEL,
        mcpServers: this.getMCPServerConfig(),
        allowedTools: this.getAllowedTools(),
        systemPrompt: params.modeConfig.customInstructions
      }
    })) {
      // ...
    }
    // ...
  }
  ```

- The `execute_agent_mode` tool in `src/index.ts` checks if V2 mode is enabled:
  ```typescript
  // Check if V2 mode is enabled
  if (CONFIG.AUTOMATION_MODE !== 'V2') {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          mode: "V1_SIMULATION",
          message: "V2 automation is not enabled. Set AUTOMATION_MODE=V2 environment variable to enable automated execution.",
          help: "Current mode only supports delegation simulation. Use delegate_to_mode for V1 functionality."
        }, null, 2)
      }]
    };
  }
  ```

## MCP Settings Configuration

The MCP server is configured in `mcp_settings.json`. Based on the documentation in the README.md and USAGE_GUIDE.md files, we need to add the environment variables to the existing configuration.

### Current mcp_settings.json Structure

```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": ["C:\\Users\\jazbo\\AppData\\Roaming\\Roo-Code\\MCP\\custom-agents-orchestrator\\build\\index.js"],
      "env": {
        "AGENTS_DIR": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\agents",
        "MEMORY_DB": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\memory.db"
      },
      "disabled": false,
      "alwaysAllow": [],
      "disabledTools": []
    }
  }
}
```

### Updated mcp_settings.json with V2 Automation

```json
{
  "mcpServers": {
    "custom-agents-orchestrator": {
      "command": "node",
      "args": ["C:\\Users\\jazbo\\AppData\\Roaming\\Roo-Code\\MCP\\custom-agents-orchestrator\\build\\index.js"],
      "env": {
        "AGENTS_DIR": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\agents",
        "MEMORY_DB": "c:\\Users\\jazbo\\Documents\\develop\\AI Agents\\memory.db",
        "AUTOMATION_MODE": "V2",
        "ANTHROPIC_API_KEY": "sk-ant-your-api-key-here"
      },
      "disabled": false,
      "alwaysAllow": [],
      "disabledTools": []
    }
  }
}
```

## Step-by-Step Configuration Instructions

1. **Obtain an Anthropic API Key**
   - Sign up at [Anthropic's website](https://www.anthropic.com/)
   - Navigate to the API section and create a new API key
   - Copy the API key (it starts with `sk-ant-`)

2. **Locate the mcp_settings.json File**
   - The file should be in `C:\Users\jazbo\AppData\Roaming\Roo-Code\mcp_settings.json`
   - If it doesn't exist, create it with the structure shown above

3. **Edit mcp_settings.json**
   - Add the `AUTOMATION_MODE` and `ANTHROPIC_API_KEY` environment variables to the `env` section
   - Make sure to replace `"sk-ant-your-api-key-here"` with your actual Anthropic API key

4. **Save the File**
   - Ensure the JSON is properly formatted with no syntax errors
   - Save the file in the same location

5. **Restart RooCode**
   - Close and reopen RooCode to reload the MCP server with the new configuration
   - This is necessary for the environment variables to take effect

## Verifying AUTOMATION_MODE=V2 Was Loaded

After restarting RooCode, you can verify that the V2 automation mode was loaded correctly by:

1. **Check RooCode Console Output**
   - Look for the line: `Custom Agents Orchestrator MCP Server running`
   - Followed by: `Automation mode: V2`
   - And: `API Key: ***Set***`

2. **Test with list_agent_modes Tool**
   - Use the `list_agent_modes` tool to verify the server is running:
   ```
   use_mcp_tool('custom-agents-orchestrator', 'list_agent_modes', {})
   ```
   - If it returns a list of modes, the server is running correctly

3. **Test V2 Automation Mode**
   - Try using the `execute_agent_mode` tool with a simple task:
   ```
   use_mcp_tool('custom-agents-orchestrator', 'execute_agent_mode', {
     "mode_slug": "orchestrator-goal-clarification",
     "task_description": "AUTOMATION WORKING OK"
   })
   ```
   - If V2 mode is enabled and the API key is valid, it should return a successful response
   - If not, it will return an error message indicating what's wrong

## Troubleshooting

### Common Issues

1. **"V2 automation is not enabled" Error**
   - Ensure `AUTOMATION_MODE` is set to `"V2"` (case-sensitive)
   - Restart RooCode after making changes

2. **"ANTHROPIC_API_KEY environment variable is required" Error**
   - Ensure the API key is correctly set in mcp_settings.json
   - Check that the API key format is correct (starts with `sk-ant-`)

3. **"Agent Executor not initialized" Error**
   - This indicates a problem with the API key or initialization
   - Check the RooCode console for more detailed error messages

4. **No Response from execute_agent_mode**
   - Ensure the Claude API is accessible from your network
   - Check if your API key has sufficient quota/credits

### Checking Environment Variables

If you're unsure whether the environment variables are being loaded correctly, you can modify the MCP server code to log them:

1. Add logging in `src/index.ts`:
   ```typescript
   console.error(`AUTOMATION_MODE: ${process.env.AUTOMATION_MODE}`);
   console.error(`ANTHROPIC_API_KEY: ${process.env.ANTHROPIC_API_KEY ? '***Set***' : 'Not Set'}`);
   ```

2. Rebuild the server:
   ```
   cd C:\Users\jazbo\AppData\Roaming\Roo-Code\MCP\custom-agents-orchestrator
   npm run build
   ```

3. Restart RooCode and check the console output