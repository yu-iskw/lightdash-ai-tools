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
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import Group
from lightdash_ai_tools.lightdash.services.list_groups_in_organization_v1 import (
    ListGroupsInOrganizationV1Service,
)


class GetGroupsInOrganizationToolInput(BaseModel):
    """Input for the GetGroupsInOrganizationTool tool."""
    # page_size: Optional[float] = Field(
    #     default=100,
    #     description="Number of results per page. Defaults to 100."
    # )
    # include_members: Optional[float] = Field(
    #     default=None,
    #     description="Number of members to include in the group details"
    # )
    # search_query: Optional[str] = Field(
    #     default=None,
    #     description="Optional search query to filter groups"
    # )




class GetGroupsInOrganization:
    """
    Controller for managing group listing operations in the organization
    Supports both synchronous and asynchronous operations
    """
    name: str = "get_groups_in_organization"
    description: str = "Retrieve all groups in the current user's organization"
    input_schema: Type[BaseModel] = GetGroupsInOrganizationToolInput

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the controller with a Lightdash API client

        :param lightdash_client: Authenticated Lightdash API client
        """
        self.client = lightdash_client
        self.service = ListGroupsInOrganizationV1Service(lightdash_client=lightdash_client)

    def call(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> List[Group]:
        """
        Execute the synchronous group listing operation

        :param page_size: Number of results per page
        :param include_members: Number of members to include
        :param search_query: Search query to filter groups
        :return: List of groups
        """
        return self.service.get_all_groups(
            page_size=page_size,
            include_members=include_members,
            search_query=search_query
        )

    async def acall(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> List[Group]:
        """
        Execute the asynchronous group listing operation

        :param page_size: Number of results per page
        :param include_members: Number of members to include
        :param search_query: Search query to filter groups
        :return: List of groups
        """
        return await self.service.get_all_groups_async(
            page_size=page_size,
            include_members=include_members,
            search_query=search_query
        )

    def get_group_details(self, group_uuid: str) -> Optional[Group]:
        """
        Get details of a specific group by its UUID

        :param group_uuid: UUID of the group to retrieve
        :return: Group details or None if not found
        """
        all_groups = self.call()
        return next((group for group in all_groups if group.uuid == group_uuid), None)

    def filter_groups(
        self,
        name_contains: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> List[Group]:
        """
        Filter groups based on specific criteria

        :param name_contains: Filter groups whose name contains this substring
        :param created_by: Filter groups created by a specific user UUID
        :return: Filtered list of groups
        """
        all_groups = self.call()

        filtered_groups = all_groups

        if name_contains:
            filtered_groups = [
                group for group in filtered_groups
                if name_contains.lower() in group.name.lower()
            ]

        if created_by:
            filtered_groups = [
                group for group in filtered_groups
                if group.createdByUserUuid == created_by
            ]

        return filtered_groups
