from google.adk.agents.llm_agent import Agent
from google.genai import types
from google.genai.types import HttpRetryOptions

from jira_agent.sub_agent.jira_agent.agent import jira_agent
from jira_agent.sub_agent.confluence_agent.agent import confluence_agent
from jira_agent.sub_agent.poc_agent.agent import poc_agent
from .prompt import root_agent_instruction

import dotenv
import os

dotenv.load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")

def extract_text_from_uploaded_file(file_path: str) -> str:
    """
    A placeholder function to extract text from an uploaded file.
    In a real implementation, this would handle various file types (e.g., .txt, .docx, .pdf).
    
    Args:
        file_path: The path to the uploaded file.
    
    Returns:
        str: The extracted text from the file.
    """
    with open(file_path, 'r') as file:
        return file.read()

root_agent = Agent(
    model='gemini-2.5-pro',
    name='root_agent',
    description='Meeting notes understanding and formatting agent',
    instruction=root_agent_instruction,
    sub_agents=[jira_agent, confluence_agent, poc_agent],
    generate_content_config= types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=50000,
        http_options=types.HttpOptions(
            retry_options=HttpRetryOptions(initial_delay=2)
        )
    ),
    tools=[extract_text_from_uploaded_file]
)

app = root_agent

__all__ = ['root_agent', 'app']
