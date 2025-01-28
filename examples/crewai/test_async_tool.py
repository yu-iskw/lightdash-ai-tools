# Copyright 2025 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

import litellm
from crewai import LLM, Agent, Crew, Task
from crewai.tools import tool


@tool
async def async_custom_tool(input_data: str) -> str:
    """
    An async custom tool that performs a sample asynchronous task.
    Args:
        input_data (str): The input data for the tool.

    Returns:
        str: The result of the async operation.
    """
    await asyncio.sleep(2)  # Simulate an async operation like an API call
    return f"Processed asynchronously: {input_data}"


async def async_custom_tool_2(input_data: str) -> str:
    """
    An async custom tool that performs a sample asynchronous task.
    """
    await asyncio.sleep(2)  # Simulate an async operation like an API call
    return f"Processed asynchronously: {input_data}"


async def main():
    litellm.set_verbose = True
    llm = LLM(
      model="gemini-1.5-pro",
      temperature=0.1,
    )
    async_agent = Agent(
        role="Async Worker",
        goal="Perform tasks asynchronously using custom tools.",
        verbose=True,
        memory=True,
        backstory="You are a modern worker, adept at using asynchronous operations.",
        tools=[async_custom_tool],
        llm=llm,
    )


    async_task = Task(
        description="Use the async tool to process the input data efficiently.",
        expected_output="A string processed asynchronously by the tool.",
        agent=async_agent,
        tools=[async_custom_tool],
        async_execution=True,
        human_input=True,
    )

    crew = Crew(
        agents=[async_agent],
        tasks=[async_task],
        memory=True,
        verbose=True,
    )

    result = await crew.kickoff_async()
    print(f"The result of the task is: {result}")


if __name__ == "__main__":
    asyncio.run(main())
