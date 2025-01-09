# lightdash-ai-tools

AI tools for Lightdash API

## Installation

```bash
# Install lightdash-ai-tools for LangChain
pip install lightdash-ai-tools[langchain]
```

## Supported AI Frameworks

- [x] [LangChain](https://docs.langchain.com/)
- [ ] [AutoGen](https://microsoft.github.io/autogen/stable//index.html)
- [ ] [CrewAI](https://www.crewai.com/)
- [ ] [Phidata](https://www.phidata.com/)

## Examples

### LangChain

An example of react agent with LangChain is available in the [examples/langchain/agent.py](examples/langchain/agent.py) file.

```python
    # Create Lightdash client
    lightdash_url = os.getenv("LIGHTDASH_URL")
    lightdash_api_key = os.getenv("LIGHTDASH_API_KEY")
    if not lightdash_url or not lightdash_api_key:
        raise ValueError("Environment variables LIGHTDASH_URL and LIGHTDASH_API_KEY must be set.")
    client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )

    # Create the agent with the tools
    llm = ChatOpenAI(model="gpt-4o")
    tools = get_all_readable_tools(lightdash_client=client)
    agent = create_react_agent(llm, tools)

    # Run the agent
    messages = [
      HumanMessage(content=question),
      ]
    events = agent.stream({"messages": messages}, stream_mode="values")
    for s in events:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
```
