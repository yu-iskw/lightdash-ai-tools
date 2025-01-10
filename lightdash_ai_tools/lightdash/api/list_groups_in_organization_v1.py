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

from typing import Any, Dict, Optional

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import (
    ListGroupsInOrganizationV1Response,
)


class ListGroupsInOrganizationV1(BaseLightdashApiCaller[ListGroupsInOrganizationV1Response]):
    """API call to list groups in the organization."""

    request_type = RequestType.GET

    def _request(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
        include_members: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        List groups in the organization.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter groups
            include_members: Optional parameter to include members in the group details

        Returns:
            Dict[str, Any]
        """
        if page_size is None:
            page_size = 100
        parameters = {
            k: str(v) for k, v in {
                'page': page,
                'pageSize': page_size,
                'searchQuery': search_query,
                'includeMembers': include_members
            }.items() if v is not None
        }

        formatted_path = "/api/v1/org/groups"
        response_data = self.lightdash_client.call(self.request_type, formatted_path, parameters=parameters)
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> ListGroupsInOrganizationV1Response:
        return ListGroupsInOrganizationV1Response(**response_data)
