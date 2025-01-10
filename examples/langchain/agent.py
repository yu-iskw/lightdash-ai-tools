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

# How to use the script
# $ export LIGHTDASH_URL=https://your-lightdash-instance.com
# $ export LIGHTDASH_API_KEY=your-api-key
# $ python examples/langchain/agent.py --question "What role does Amy have in all projects?"

import argparse
import os

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.prebuilt import create_react_agent

from lightdash_ai_tools.langchain.tools import get_all_readable_tools
from lightdash_ai_tools.lightdash.client import LightdashClient


def main(question: str):
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
    llm = ChatVertexAI(model_name="gemini-1.5-flash")
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


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", type=str, required=True)
    args = parser.parse_args()
    main(question=args.question)
