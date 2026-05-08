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

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Prefer dedicated CONFLUENCE_* vars if set, otherwise derive from the Jira ones.
CONFLUENCE_URL = (
    os.getenv("CONFLUENCE_URL")
    or os.getenv("CONFLUENCE_BASE_URL")
    or (f"{JIRA_URL.rstrip('/')}/wiki" if JIRA_URL else None)
)
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL") or JIRA_EMAIL
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN") or JIRA_API_TOKEN

_confluence_env = {
    "CONFLUENCE_URL": CONFLUENCE_URL,
    "CONFLUENCE_USERNAME": CONFLUENCE_EMAIL,
    "CONFLUENCE_API_TOKEN": CONFLUENCE_API_TOKEN,
} if CONFLUENCE_URL and CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN else None

confluence_agent = Agent(
    model='gemini-2.5-pro',
    name='confluence_agent',
    description='An assistant for searching, reading, and managing Confluence pages and spaces.',
    instruction=instruction,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=50000,
        http_options=types.HttpOptions(
            retry_options=HttpRetryOptions(initial_delay=2)
        )
    ),
    tools=[McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='uvx',
                args=['mcp-atlassian'],
                env=_confluence_env,
            ),
            timeout=300
        ),
    )]
)
