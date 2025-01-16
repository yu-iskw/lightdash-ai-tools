## Design Document: Multi-Agent System for Lightdash Investigation with Human-in-the-Loop

### 1. Introduction

This document outlines the design for a multi-agent system using CrewAI to interact with Lightdash via LangChain tools. The system will enable users to investigate Lightdash resources (projects, spaces, groups, explores, etc.) through a chat interface, incorporating human-in-the-loop for guidance and error correction.

### 2. System Goals

- **Resource Investigation:** Allow users to explore Lightdash resources using natural language queries.
- **Tool Utilization:** Effectively leverage LangChain tools for Lightdash to retrieve information.
- **Human-in-the-Loop:** Enable users to guide the investigation, provide context, and correct errors.
- **Error Handling:** Implement a mechanism for agents to handle tool call failures and request human assistance.
- **Chat Interface Integration:** Seamlessly integrate the multi-agent system with a chat interface (like ChatGPT).

### 3. Agent Roles and Responsibilities

We will define the following agent roles:

- **User Proxy Agent:**
  - **Role:** Acts as the interface between the user and the system.
  - **Goal:** Understand user requests and translate them into actionable tasks for other agents.
  - **Responsibilities:**
    - Receive user input from the chat interface.
    - Parse user intent and identify the required information.
    - Delegate tasks to the appropriate agents.
    - Present results to the user in a clear and concise manner.
    - Handle user feedback and adjust the investigation accordingly.
- **Lightdash Investigator Agent:**
  - **Role:** Responsible for interacting with Lightdash using the provided tools.
  - **Goal:** Retrieve the requested information from Lightdash.
  - **Responsibilities:**
    - Receive tasks from the User Proxy Agent.
    - Select and execute the appropriate LangChain tools.
    - Handle tool call failures and request human assistance if needed.
    - Format the retrieved data for the User Proxy Agent.
- **Tool Fixer Agent:**
  - **Role:** Specialized in fixing tool call failures.
  - **Goal:** Analyze failed tool calls and suggest corrections.
  - **Responsibilities:**
    - Receive failed tool call information from the Lightdash Investigator Agent.
    - Analyze the error message and the tool call arguments.
    - Suggest corrections to the tool call arguments or the tool itself.
    - Request human assistance if the error cannot be resolved automatically.

### 4. Tool Utilization

The system will utilize the following LangChain tools for Lightdash, as provided by `get_all_readable_tools`:

- `GetProjectTool`: Get details of a specific project.
- `GetProjectsTool`: Get all projects in the organization.
- `GetSpacesInProjectTool`: Get spaces within a project.
- `GetOrganizationMembersTool`: Get all members of the organization.
- `GetProjectMembersTool`: Get members of a specific project.
- `GetExploresTool`: Get explores (tables) within a project.
- `GetExploreTool`: Get details of a specific explore.
- `GetGroupsInOrganizationTool`: Get all groups in the organization.
- `GetGroupTool`: Get details of a specific group.

### 5. Workflow

1. **User Input:** The user sends a query through the chat interface (e.g., "List all projects," "Show me the members of project X," "What are the explores in project Y?").
2. **User Proxy Agent:** The User Proxy Agent receives the query, parses the intent, and creates a task for the Lightdash Investigator Agent.
3. **Lightdash Investigator Agent:**
   - The agent receives the task from the User Proxy Agent.
   - The agent selects the appropriate tool based on the task.
   - The agent executes the tool with the necessary arguments.
   - If the tool call is successful, the agent formats the results and sends them to the User Proxy Agent.
   - If the tool call fails, the agent creates a task for the Tool Fixer Agent with the error message and the tool call information.
4. **Tool Fixer Agent:**
   - The agent receives the task from the Lightdash Investigator Agent.
   - The agent analyzes the error and suggests corrections.
   - If the error can be fixed, the agent sends the corrected tool call back to the Lightdash Investigator Agent.
   - If the error cannot be fixed, the agent requests human assistance through the User Proxy Agent.
5. **Human-in-the-Loop:**
   - If human assistance is requested, the User Proxy Agent presents the error and the suggested corrections to the user.
   - The user can provide feedback, correct the tool call, or provide additional context.
   - The User Proxy Agent relays the user's input to the Lightdash Investigator Agent.
6. **Iteration:** The process repeats until the user's query is satisfied.
7. **User Output:** The User Proxy Agent presents the final results to the user through the chat interface.

### 6. Implementation Details

- **CrewAI Setup:** Define the agents with their respective roles, goals, and tools.
- **LangChain Integration:** Initialize the Lightdash client and load the tools using `get_all_readable_tools`.
- **Chat Interface:** Integrate the CrewAI system with a chat interface (e.g., using a library like `streamlit` or `gradio`).
- **Error Handling:** Implement try-except blocks in the Lightdash Investigator Agent to catch tool call failures.
- **Tool Fixer Logic:** Implement logic in the Tool Fixer Agent to analyze error messages and suggest corrections. This might involve pattern matching, argument validation, or using a language model to generate suggestions.
- **Human Interaction:** Design a clear and intuitive way for the user to interact with the system, provide feedback, and correct errors.

### 7. Example Code Snippet (Conceptual)

```python
from crewai import Agent, Crew, Task
from langchain_core.tools import BaseTool
from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.lightdash.client import LightdashClient

# Initialize Lightdash client (replace with your actual credentials)
lightdash_client = LightdashClient(
    api_url="YOUR_LIGHTDASH_API_URL",
    api_key="YOUR_LIGHTDASH_API_KEY"
)

# Load Lightdash tools
tools = get_all_readable_tools(lightdash_client)

# Define agents
user_proxy_agent = Agent(
    role="User Proxy",
    goal="Understand user requests and manage the investigation.",
    backstory="You are an interface between the user and the Lightdash system.",
    allow_delegation=True,
)

lightdash_investigator_agent = Agent(
    role="Lightdash Investigator",
    goal="Retrieve information from Lightdash using the provided tools.",
    backstory="You are an expert in using Lightdash tools.",
    tools=tools,
    allow_delegation=True,
)

tool_fixer_agent = Agent(
    role="Tool Fixer",
    goal="Analyze failed tool calls and suggest corrections.",
    backstory="You are an expert in debugging tool calls.",
    allow_delegation=False,
)

# Define tasks
initial_task = Task(
    description="Initial user query will be processed here.",
    agent=user_proxy_agent
)

# Create crew
crew = Crew(
    agents=[user_proxy_agent, lightdash_investigator_agent, tool_fixer_agent],
    tasks=[initial_task],
    verbose=True
)

# Run crew
result = crew.kickoff()
print(result)
```

### 8. Future Enhancements

- **Write Tools:** Implement write tools to allow users to modify Lightdash resources.
- **Caching:** Implement caching to improve performance and reduce API calls.
- **Advanced Error Handling:** Implement more sophisticated error handling and recovery mechanisms.
- **Context Management:** Implement context management to allow agents to remember previous interactions and user preferences.
- **Visualization:** Integrate visualization tools to present the retrieved data in a more user-friendly way.

This design document provides a comprehensive overview of the multi-agent system for Lightdash investigation. The implementation will require careful attention to detail and thorough testing to ensure the system is robust, reliable, and user-friendly.
