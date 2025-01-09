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

    def __init__(self, client: LightdashClient):
        """
        Initialize the service.

        Args:
            client: Lightdash client for making API calls
        """
        self._client = client

    def get_all_members(
        self,
        page_size: Optional[int] = None
    ) -> List[OrganizationMemberModel]:
        """
        Get all members of the organization.

        Returns:
            List of organization members
        """
        all_members = []
        page = 1
        api_call = ListOrganizationMembersV1(client=self._client)
        while True:
            response: ListOrganizationMembersV1Response = api_call.call(
                page=page,
                page_size=page_size,
            )
            if len(response.results.data) == 0:
              break
            all_members.extend(response.results.data)
            page += 1
        return all_members
