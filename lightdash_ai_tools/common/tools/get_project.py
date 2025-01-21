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

from lightdash_ai_tools.lightdash.api.get_project_v1 import GetProjectV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_project_v1 import GetProjectResults


class GetProjectToolInput(BaseModel):
    """Input for the GetProject tool."""
    project_uuid: str = Field(description="The UUID of the project to fetch. That isn't the project name.")


class GetProject:
    """Controller for the GetProject tool"""

    name: str = "get_project"
    description: str = "Get the project details associated with the given UUID."
    input_schema: Type[BaseModel] = GetProjectToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def __call__(self, project_uuid: str) -> GetProjectResults:
        """Call the controller"""
        response = GetProjectV1(lightdash_client=self.lightdash_client).call(project_uuid)
        return response.results
