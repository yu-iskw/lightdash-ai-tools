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

from typing import List, Type

from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_explores_v1 import GetExploresV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_explores_v1 import GetExploresV1Results


class GetExploresToolInput(BaseModel):
    """Input for the GetExploresTool tool."""
    project_uuid: str = Field(description="The UUID of the project to get explores for. That isn't the project name.")

class GetExplores:
    """Controller for the GetExplores tool"""

    name: str = "get_explores"
    description: str = "Get explores (tables) in a project."
    input_schema: Type[BaseModel] = GetExploresToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def call(self, project_uuid: str) -> List[GetExploresV1Results]:
        """Call the controller"""
        response = GetExploresV1(lightdash_client=self.lightdash_client).call(project_uuid)
        return response.results

    async def acall(self, project_uuid: str) -> List[GetExploresV1Results]:
        """Call the controller asynchronously"""
        response = await GetExploresV1(lightdash_client=self.lightdash_client).acall(project_uuid)
        return response.results
