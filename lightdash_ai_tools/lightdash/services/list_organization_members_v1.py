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

from typing import List

from lightdash_ai_tools.lightdash.api.list_organization_members_v1 import (
    ListOrganizationMembersV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_members_v1 import (
    ListOrganizationMembersV1Response,
    OrganizationMemberModel,
)


class ListOrganizationMembersV1Service:
    """Service for listing organization members."""

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the service.

        Args:
            lightdash_client: Lightdash client for making API calls
        """
        self.lightdash_client = lightdash_client

    def get_all_members(
        self,
        page_size: int = 100
    ) -> List[OrganizationMemberModel]:
        """
        Get all members of the organization.

        Returns:
            List of organization members
        """
        all_members: List[OrganizationMemberModel] = []
        current_page = 1
        api_call = ListOrganizationMembersV1(lightdash_client=self.lightdash_client)

        while True:
            response: ListOrganizationMembersV1Response = api_call.call(
                page=current_page,
                page_size=page_size,
            )

            # Extract members from the response
            current_members = response.results.data
            if not current_members:
                break

            all_members.extend(current_members)

            # Check if we've retrieved all pages
            total_pages = response.results.pagination.totalPageCount

            if current_page >= total_pages:
                break

            current_page += 1
        return all_members

    async def aget_all_members(
        self,
        page_size: int = 100
    ) -> List[OrganizationMemberModel]:
        """
        Asynchronously get all members of the organization.

        Returns:
            List of organization members
        """
        all_members: List[OrganizationMemberModel] = []

        all_members: List[OrganizationMemberModel] = []
        current_page = 1
        api_call = ListOrganizationMembersV1(lightdash_client=self.lightdash_client)

        while True:
            response: ListOrganizationMembersV1Response = await api_call.acall(
                page=current_page,
                page_size=page_size,
            )

            # Extract members from the response
            current_members = response.results.data
            if not current_members:
                break

            all_members.extend(current_members)

            # Check if we've retrieved all pages
            total_pages = response.results.pagination.totalPageCount

            if current_page >= total_pages:
                break

            current_page += 1
        return all_members
