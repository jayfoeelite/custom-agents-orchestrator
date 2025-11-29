# MCP Server V2 Automation Implementation Verification

This document outlines the exact steps to verify that the MCP server V2 automation has been successfully implemented and is functioning correctly.

## RooCode Restart Procedure

After editing the mcp_settings.json file to add the AUTOMATION_MODE and ANTHROPIC_API_KEY environment variables, you need to restart RooCode to load the new configuration:

1. **Save all open files** in RooCode
2. **Close RooCode** completely (including all windows)
3. **Wait 5 seconds** to ensure all processes are terminated
4. **Restart RooCode** by opening it again
5. **Open the AI Agents project** if it's not automatically opened

## Confirming MCP Server Reload

To confirm that the MCP server has reloaded with the new environment variables:

1. **Check the RooCode console output** for the following messages:
   ```
   Custom Agents Orchestrator MCP Server running
   Agents directory: c:\Users\jazbo\Documents\develop\AI Agents\agents
   Memory database: c:\Users\jazbo\Documents\develop\AI Agents\memory.db
   Loaded 46 agent modes
   Automation mode: V2
   API Key: ***Set***
   ```

2. **Verify the MCP server is connected** by checking the "Connected MCP Servers" section in the RooCode interface. You should see "custom-agents-orchestrator" listed with its available tools.

3. **Test basic connectivity** with a simple tool call:
   ```typescript
   use_mcp_tool('custom-agents-orchestrator', 'list_agent_modes', {})
   ```
   This should return a list of available agent modes. If it works, the server is running and connected.

## HELLO WORLD Test Execution

To verify that the V2 automation is working correctly, run the HELLO WORLD test:

1. **Execute the test command** in RooCode:
   ```typescript
   use_mcp_tool('custom-agents-orchestrator', 'execute_agent_mode', {
     "mode_slug": "orchestrator-goal-clarification",
     "task_description": "This is a simple test to verify V2 automation is working correctly. Please respond with 'AUTOMATION WORKING OK' followed by the current timestamp."
   })
   ```

2. **Wait for the response** - This may take a few seconds as it connects to the Anthropic API and executes the agent mode.

3. **Check the response format** - You should receive a JSON response with:
   - `"success": true`
   - `"modeSlug": "orchestrator-goal-clarification"`
   - `"response"` containing "AUTOMATION WORKING OK" and a timestamp
   - `"sessionId"` with a unique session ID
   - `"tokensUsed"` with input and output token counts

4. **Verify routing headers** - The response should include proper routing headers:
   ```
   To: uber-orchestrator, From: orchestrator-goal-clarification
   ```

## Troubleshooting Common Issues

If you encounter issues during verification, check the following:

### 1. MCP Server Not Loading

**Symptoms:**
- No "Custom Agents Orchestrator MCP Server running" message in console
- `list_agent_modes` returns an error about the server not being connected

**Solutions:**
- Check that mcp_settings.json exists and has the correct format
- Verify the path to the server's index.js file is correct
- Ensure RooCode has permission to access the file
- Try restarting RooCode again

### 2. V1 Simulation Mode Still Active

**Symptoms:**
- `execute_agent_mode` returns a message about V2 automation not being enabled
- Console shows "Automation mode: V1" instead of "V2"

**Solutions:**
- Double-check the mcp_settings.json file to ensure `"AUTOMATION_MODE": "V2"` is set correctly (case-sensitive)
- Verify that RooCode is using the updated mcp_settings.json file
- Check for any error messages during server startup that might indicate configuration issues

### 3. API Key Issues

**Symptoms:**
- Error message about missing or invalid ANTHROPIC_API_KEY
- Authentication errors when trying to use `execute_agent_mode`

**Solutions:**
- Verify the API key format (should start with `sk-ant-`)
- Check that the API key is correctly set in mcp_settings.json
- Ensure the API key has not expired or been revoked
- Try generating a new API key if necessary

### 4. Agent Mode Execution Failures

**Symptoms:**
- `execute_agent_mode` returns a success: false response
- Error messages about mode not found or execution failure

**Solutions:**
- Verify that the specified mode exists in the agents directory
- Check that the AGENTS_DIR environment variable is correctly set
- Try with a different agent mode to see if the issue is specific to one mode
- Check for any rate limiting or quota issues with the Anthropic API

## Next Steps After Successful Verification

Once you've successfully verified that the V2 automation is working:

1. **Try more complex tasks** with different agent modes
2. **Test with context files** to ensure they're properly passed to the agent
3. **Monitor token usage** to understand the cost implications
4. **Consider setting up monitoring** for API usage and errors
5. **Document any customizations** made to the configuration

By following these verification steps, you can ensure that the MCP server V2 automation is properly configured and functioning as expected.