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

from typing import Type

from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_explore_v1 import GetExploreV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_explore_v1 import GetExploreV1Results


class GetExploreToolInput(BaseModel):
    """Input for the GetExploreTool tool."""
    project_uuid: str = Field(description="The UUID of the project. This is not the project name.")
    explore_id: str = Field(description="The ID of the explore to retrieve.")


class GetExplore:
    """Controller for the GetExplore tool"""

    name: str = "get_explore"
    description: str = "Get a specific explore (table) in a project."
    input_schema: Type[BaseModel] = GetExploreToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def call(self, project_uuid: str, explore_id: str) -> GetExploreV1Results:
        """Get a specific explore in a project"""
        response = GetExploreV1(lightdash_client=self.lightdash_client).call(project_uuid, explore_id)
        return response.results

    async def acall(self, project_uuid: str, explore_id: str) -> GetExploreV1Results:
        """Get a specific explore in a project asynchronously"""
        response = await GetExploreV1(lightdash_client=self.lightdash_client).acall(
            project_uuid, explore_id
        )
        return response.results
