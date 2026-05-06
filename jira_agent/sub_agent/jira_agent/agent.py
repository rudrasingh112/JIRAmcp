from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from .prompt import instruction
from google.genai import types
from google.genai.types import HttpRetryOptions
import os
import dotenv

dotenv.load_dotenv()

# Load environment variables
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_CLOUD_ID = os.getenv("JIRA_CLOUD_ID")

jira_agent = Agent(
    model='gemini-2.5-pro',
    name='jira_agent',
    description='A helpful assistant for user questions.',
    instruction=instruction,
    generate_content_config= types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=50000,
        http_options=types.HttpOptions(
            retry_options=HttpRetryOptions(initial_delay=2))

        ),
    tools=[McpToolset(
            connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command='npx',
                        args=[
                        '-y',  # Auto-confirm npx install
                        'mcp-remote',
                        'https://mcp.atlassian.com/v1/sse'
                        ],
                        env={
                        'ATLASSIAN_EMAIL': JIRA_EMAIL,
                        'ATLASSIAN_API_TOKEN': JIRA_API_TOKEN,
                        'ATLASSIAN_CLOUD_ID': JIRA_CLOUD_ID
                        } if JIRA_EMAIL and JIRA_API_TOKEN and JIRA_CLOUD_ID else None
                ),
                timeout=300
            ),
            #tool_filter=['getConfluenceSpaces', 'getConfluencePage',] # Example how to filter tools - only the listed ones are then allowed.
        )]
    )