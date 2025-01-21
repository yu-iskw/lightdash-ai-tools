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

from typing import List, Optional, Type

from pydantic import BaseModel

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_members_v1 import (
    OrganizationMemberModel,
)
from lightdash_ai_tools.lightdash.services.list_organization_members_v1 import (
    ListOrganizationMembersV1Service,
)


class GetOrganizationMembersToolInput(BaseModel):
    """Input for the GetOrganizationMembersTool tool."""
    page_size: Optional[int] = 10


class GetOrganizationMembers:
    """Controller for the GetOrganizationMembers tool"""

    name: str = "get_organization_members"
    description: str = "Get all members of the current user's organization"
    input_schema: Type[BaseModel] = GetOrganizationMembersToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client
        self.service = ListOrganizationMembersV1Service(lightdash_client=lightdash_client)

    def call(
        self,
        page_size: int = 100
    ) -> List[OrganizationMemberModel]:
        """
        Call the controller to get all organization members

        :param page_size: Number of results per page
        :return: List of organization members
        """
        return self.service.get_all_members(page_size=page_size)

    async def acall(
        self,
        page_size: int = 100
    ) -> List[OrganizationMemberModel]:
        """
        Async call the controller to get all organization members

        :param page_size: Number of results per page
        :return: List of organization members
        """
        return await self.service.aget_all_members(page_size=page_size)
