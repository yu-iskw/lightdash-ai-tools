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

from typing import List, Optional

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import (
    Group,
    ListGroupsInOrganizationV1Response,
)
from lightdash_ai_tools.lightdash.services.list_groups_in_organization import (
    ListGroupsInOrganizationService,
)


class GetGroupsInOrganizationController:
    """
    Controller for managing group listing operations in the organization
    """
    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the controller with a Lightdash API client

        :param lightdash_client: Authenticated Lightdash API client
        """
        self.lightdash_client = lightdash_client

    def __call__(
        self,
        page: Optional[float] = None,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> ListGroupsInOrganizationV1Response:
        """
        List groups with optional filtering and pagination

        :param page: Page number for pagination
        :param page_size: Number of results per page (default: 100)
        :param include_members: Number of members to include in group details
        :param search_query: Search query to filter groups
        :return: ListGroupsResponse containing groups
        """
        service = ListGroupsInOrganizationService(lightdash_client=self.lightdash_client)
        return service.get_all_groups(
            page_size=page_size,
            include_members=include_members,
            search_query=search_query
        )

    def list_all_groups(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> List[Group]:
        """
        Retrieve all groups across all pages

        :param page_size: Number of results per page (default: 100)
        :param include_members: Number of members to include in group details
        :param search_query: Search query to filter groups
        :return: List of all groups
        """
        service = ListGroupsInOrganizationService(lightdash_client=self.lightdash_client)
        return service.get_all_groups(
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
        all_groups = self.list_all_groups()
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
        all_groups = self.list_all_groups()

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
