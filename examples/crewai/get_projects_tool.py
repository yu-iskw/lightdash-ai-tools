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

from crewai import LLM, Agent, Crew, Task

from lightdash_ai_tools.crewai.tools.get_projects import GetProjectsTool
from lightdash_ai_tools.lightdash.client import LightdashClient


def main():
    lightdash_url = os.getenv("LIGHTDASH_URL")
    lightdash_api_key = os.getenv("LIGHTDASH_API_KEY")
    lightdash_client = LightdashClient(
        base_url=lightdash_url,
        token=lightdash_api_key,
    )
    get_projects_tool = GetProjectsTool(lightdash_client=lightdash_client)

    llm = LLM(
      model="gemini-1.5-pro",
      temperature=0.1,
    )
    lightdash_expert = Agent(
        role="Lightdash Expert",
        goal="Get all projects in the organization.",
        backstory="You are an expert in Lightdash.",
        tools=[get_projects_tool],
        allow_delegation=False,
        llm=llm,
    )

    get_projects_task = Task(
        description="Get all projects in the organization.",
        agent=lightdash_expert,
        expected_output="A list of projects in the organization.",
    )

    crew = Crew(
        agents=[lightdash_expert],
        tasks=[get_projects_task],
        planning=True,
        planning_llm=llm,
        memory=True,
        verbose=True,
    )

    result = crew.kickoff()
    print(f"The result of the task is: {result}")


if __name__ == "__main__":
    main()
