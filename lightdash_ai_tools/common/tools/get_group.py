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

from typing import Optional, Type

from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_group_v1 import GetGroupV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_group_v1 import GetGroupV1Response


class GetGroupToolInput(BaseModel):
    """Input for the GetGroupTool tool."""
    group_uuid: str = Field(description="The UUID of the group to retrieve.")
    include_members: Optional[int] = Field(description="Number of members to include.")
    # offset: Optional[int] = Field(description="Offset of members to include.")

class GetGroup:
    """Controller for getting group details."""

    name: str = "get_group"
    description: str = "Get details of a specific group in the Lightdash organization"
    input_schema: Type[BaseModel] = GetGroupToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the get group controller.

        :param lightdash_client: Lightdash client for making API calls
        """
        self.lightdash_client = lightdash_client

    def call(
        self,
        group_uuid: str,
        include_members: Optional[int] = None,
        offset: Optional[int] = None
    ) -> GetGroupV1Response:
        """
        Get details of a specific group.

        :param group_uuid: Unique identifier of the group
        :param include_members: Number of members to include
        :param offset: Offset of members to include
        :return: Group details response
        """
        api = GetGroupV1(lightdash_client=self.lightdash_client)
        return api.call(group_uuid=group_uuid, include_members=include_members, offset=offset)

    async def acall(
        self,
        group_uuid: str,
        include_members: Optional[int] = None,
        offset: Optional[int] = None
    ) -> GetGroupV1Response:
        """
        Asynchronously get details of a specific group.

        :param group_uuid: Unique identifier of the group
        :param include_members: Number of members to include
        :param offset: Offset of members to include
        :return: Group details response
        """
        api = GetGroupV1(lightdash_client=self.lightdash_client)
        return await api.acall(group_uuid=group_uuid, include_members=include_members, offset=offset)
