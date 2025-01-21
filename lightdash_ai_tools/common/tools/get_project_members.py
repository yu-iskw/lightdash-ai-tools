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

from lightdash_ai_tools.lightdash.api.get_project_access_list_v1 import (
    GetProjectAccessListV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_project_access_list_v1 import (
    GetProjectAccessListV1Results,
)


class GetProjectMembersToolInput(BaseModel):
    """Input for the GetProjectMembersTool tool."""
    project_uuid: str = Field(description="The UUID of the project to get members for. That isn't the project name.")


class GetProjectMembers:
    """Controller for the GetProjectMembers tool"""

    name: str = "get_project_members"
    description: str = "Get members of a project"
    input_schema: Type[BaseModel] = GetProjectMembersToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def call(self, project_uuid: str) -> List[GetProjectAccessListV1Results]:
        """Call the controller"""
        service = GetProjectAccessListV1(lightdash_client=self.lightdash_client)
        return service.call(project_uuid=project_uuid)

    async def acall(self, project_uuid: str) -> List[GetProjectAccessListV1Results]:
        """Async call the controller"""
        service = GetProjectAccessListV1(lightdash_client=self.lightdash_client)
        return await service.acall(project_uuid=project_uuid)
