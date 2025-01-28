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

import os

from crewai import Agent, Crew, Task

from lightdash_ai_tools.crewai.tools import get_all_readable_crewai_tools
from lightdash_ai_tools.lightdash.client import LightdashClient


class LightdashInvestigationCrew():
    """Crew that investigates Lightdash resources."""

    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs

    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result

    def user_proxy_agent(self) -> Agent:
        return Agent(
            role="User Proxy",
            goal="Understand user requests and manage the investigation.",
            backstory="You are an interface between the user and the Lightdash system.",
            allow_delegation=True,
        )

    def lightdash_investigator_agent(self, tools) -> Agent:
        return Agent(
            role="Lightdash Investigator",
            goal="Retrieve information from Lightdash using the provided tools.",
            backstory="You are an expert in using Lightdash tools.",
            tools=tools,
            allow_delegation=False,
        )

    def tool_fixer_agent(self) -> Agent:
        return Agent(
            role="Tool Fixer",
            goal="Analyze failed tool calls and suggest corrections.",
            backstory="You are an expert in debugging tool calls.",
            allow_delegation=False,
        )

    def initial_task(self, tools) -> Task:
        return Task(
            description="Initial user query will be processed here.",
            agent=self.user_proxy_agent(),
            tools=tools,
            expected_output="A list of projects in the organization.",
        )

    def crew(self, tools) -> Crew:
        return Crew(
            agents=[
                self.user_proxy_agent(),
                self.lightdash_investigator_agent(tools),
                self.tool_fixer_agent(),
            ],
            tasks=[self.initial_task(tools)],
            verbose=True
        )


def main():
    lightdash_url = os.getenv("LIGHTDASH_URL")
    lightdash_api_key = os.getenv("LIGHTDASH_API_KEY")
    if not lightdash_url or not lightdash_api_key:
        raise ValueError("Environment variables LIGHTDASH_URL and LIGHTDASH_API_KEY must be set.")
    lightdash_client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )
    tools = get_all_readable_crewai_tools(lightdash_client=lightdash_client)

    crew = LightdashInvestigationCrew().crew(tools)
    crew.kickoff()


if __name__ == "__main__":
    main()
