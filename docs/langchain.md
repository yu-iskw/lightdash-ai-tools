# Lightdash AI Tools: LangChain Integration

## Overview

The Lightdash AI Tools LangChain integration provides a powerful set of tools designed to seamlessly connect Lightdash's data analytics capabilities with LangChain's AI-driven workflows. This documentation offers an in-depth look at the available tools and how to leverage them effectively.

## Prerequisites

- Python 3.10+
- Lightdash Account
- LangChain

## Installation

```bash
pip install lightdash-ai-tools[langchain]
```

## Available Tools

### 1. GetExploreTool

**Purpose:** Retrieve a specific explore (table) from a Lightdash project.

**Parameters:**

- `project_uuid` (str, required): Unique identifier of the Lightdash project
- `explore_id` (str, required): Identifier of the specific explore

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetExploreTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
explore_tool = GetExploreTool(lightdash_client=client)
explore_details = explore_tool.run(
    project_uuid="project-uuid",
    explore_id="explore-id"
)
```

### 2. GetExploresTool

**Purpose:** List all explores within a Lightdash project.

**Parameters:**

- `project_uuid` (str, required): Unique identifier of the Lightdash project

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetExploresTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
explores_tool = GetExploresTool(lightdash_client=client)
all_explores = explores_tool.run(project_uuid="project-uuid")
```

### 3. GetGroupTool

**Purpose:** Retrieve details of a specific group in the organization.

**Parameters:**

- `group_uuid` (str, required): Unique identifier of the group
- `include_members` (int, optional): Number of members to include in the response

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetGroupTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
group_tool = GetGroupTool(lightdash_client=client)
group_details = group_tool.run(
    group_uuid="group-uuid",
    include_members=10
)
```

### 4. GetOrganizationMembersTool

**Purpose:** List all members in the Lightdash organization.

**Parameters:** None

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetOrganizationMembersTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
members_tool = GetOrganizationMembersTool(lightdash_client=client)
organization_members = members_tool.run()
```

### 5. GetProjectTool

**Purpose:** Retrieve details of a specific Lightdash project.

**Parameters:**

- `project_uuid` (str, required): Unique identifier of the project

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetProjectTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
project_tool = GetProjectTool(lightdash_client=client)
project_details = project_tool.run(project_uuid="project-uuid")
```

### 6. GetProjectMembersTool

**Purpose:** List users with access to a specific project.

**Parameters:**

- `project_uuid` (str, required): Unique identifier of the project

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetProjectMembersTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
project_members_tool = GetProjectMembersTool(lightdash_client=client)
project_members = project_members_tool.run(project_uuid="project-uuid")
```

### 7. GetProjectsTool

**Purpose:** List all projects in the organization.

**Parameters:** None

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetProjectsTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
projects_tool = GetProjectsTool(lightdash_client=client)
all_projects = projects_tool.run()
```

### 8. GetSpacesInProjectTool

**Purpose:** List all spaces within a specific project.

**Parameters:**

- `project_uuid` (str, required): Unique identifier of the project

**Example:**

```python
from lightdash_ai_tools.langchain.tools import GetSpacesInProjectTool
from lightdash_ai_tools.client import LightdashClient

client = LightdashClient(base_url="...", token="...")
spaces_tool = GetSpacesInProjectTool(lightdash_client=client)
project_spaces = spaces_tool.run(project_uuid="project-uuid")
```

## Advanced Usage: Creating an AI Agent

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.langchain.agents import create_react_agent
from lightdash_ai_tools.client import LightdashClient

# Initialize Lightdash client
client = LightdashClient(base_url="...", token="...")

# Create AI agent
llm = ChatGoogleGenerativeAI(model="gemini-pro")
tools = get_all_readable_tools(lightdash_client=client)
agent = create_react_agent(llm, tools)

# Query the agent
response = agent.invoke("What are our top 5 customers?")
```

## Error Handling

All tools include robust error handling. Catch `ToolException` for detailed error information:

```python
from lightdash_ai_tools.langchain.tools import GetProjectTool, ToolException

try:
    project_details = project_tool.run(project_uuid="invalid-uuid")
except ToolException as e:
    print(f"Error retrieving project: {e}")
```

## Best Practices

1. Always use environment variables for sensitive credentials
2. Handle potential API errors gracefully
3. Implement proper logging and monitoring
4. Respect Lightdash API rate limits

## Contributing

Contributions are welcome! Please submit pull requests or open issues on our GitHub repository.

## License

Apache License 2.0
