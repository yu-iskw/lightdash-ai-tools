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

import argparse  # Importing argparse to fix the undefined variable error
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils import print_stream

from lightdash_ai_tools.langchain.tools.get_project import GetProject
from lightdash_ai_tools.lightdash.client import LightdashClient


def main(project_uuid: str):
    lightdash_url = os.getenv("LIGHTDASH_URL")
    lightdash_api_key = os.getenv("LIGHTDASH_API_KEY")
    if not lightdash_url or not lightdash_api_key:
        raise ValueError("Environment variables LIGHTDASH_URL and LIGHTDASH_API_KEY must be set.")

    # Create Lightdash client
    client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )

    # Create the tool
    get_project_tool = GetProject(lightdash_client=client)
    tools = [get_project_tool]

    # Create the LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Run the tool calls
    llm = ChatOpenAI(model="gpt-4o-mini")
    question = f"What is the project name of the project with uuid {project_uuid}?"
    tool_calls = llm.bind_tools(tools).invoke(question).tool_calls
    for tool_call in tool_calls:
        result = tools[0].invoke(tool_call["args"])
        print(result)

    # Run the agent
    agent = create_react_agent(llm, tools)
    messages = [
      HumanMessage(content=question),
      ]
    events = agent.stream({"messages": messages}, stream_mode="values")
    print_stream(events)

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_uuid", type=str, required=True)
    args = parser.parse_args()
    main(args.project_uuid)